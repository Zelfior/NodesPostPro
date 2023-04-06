from NodeGraphQt import BaseNode, BaseNodeCircle
from functools import wraps

import pandas as pd
import os


class GetColumnNode(BaseNode):
    """
    An example of a node with a embedded QLineEdit.
    """

    # unique node identifier.
    __identifier__ = 'nodes.Pandas'

    # initial default node name.
    NODE_NAME = 'Get column from name'

    def __init__(self):
        super(GetColumnNode, self).__init__()

        # create input & output ports
        self.add_input('Input Dataframe', color=(0, 0, 255))

        self.add_output('Output Array', color=(0, 255, 0))
        self.add_output('Selected column name', color=(255, 0, 0))

        self.input_data_frame = None
        self.columns = None
        self.plugged_input_port = None
        self.is_defined = False

        self.output_string = None
        self.output_array = None


        # create the QComboBox menu.
        self.add_combo_menu('Column name', 'Column name', items=self.columns)

        print(self.model.properties.keys())
        print("view", self.view)

    def update_model(self):
        super(GetColumnNode, self).update_model()

        print("update_model")
    
    def update(self):
        super(GetColumnNode, self).update()

        print("update")

    def set_model(self, model):
        super(GetColumnNode, self).set_model()

        print("set_model")

    def set_property(self, name, value, push_undo=True):
        super(GetColumnNode, self).set_property(name, value, push_undo=push_undo)

        if self.is_defined:
            print(self.model.get_property("Column name"))
            self.output_string = self.get_property(name)
            print("output_string_value:", self.output_string)
            self.output_array = self.input_data_frame[self.output_string]

        self.update_from_input()

        # self.update_from_input()
        print("Set property called")
        
    def on_input_connected(self, in_port, out_port):
        super(GetColumnNode, self).on_input_connected(in_port, out_port)

        self.plugged_input_port = out_port
        # print(type(out_port))

        # print(out_port.node)
        # print(out_port.node())
        # print(out_port.node().output_data_frame)

        self.update_from_input()
        # print(self.model.get_property("Column name"))

        print("on_input_connected", in_port, out_port, self._model.name)
        
    

    def on_input_disconnected(self, in_port, out_port):
        super(GetColumnNode, self).on_input_disconnected(in_port, out_port)

        print("on_input_disconnected", in_port, out_port, self._model.name)

    def update_from_input(self):
        print("Curent columns names: ",self.view.widgets["Column name"].all_items())

        if self.plugged_input_port == None:
            pass
        else:
            if self.plugged_input_port.node().has_loaded_data_frame:
                if self.columns != self.view.widgets["Column name"].all_items():
                    self.is_defined = True
                    self.input_data_frame = self.plugged_input_port.node().output_data_frame
                    self.columns = list(self.input_data_frame.columns)

                    self.view.widgets["Column name"].clear()
                    self.view.widgets["Column name"].add_items(self.columns)

        if self.is_defined:
            print("Found property:", self.output_string)
            self.output_array = self.input_data_frame[self.output_string]
            print("Output array :", self.output_array)


        for output_id in range(len(self.outputs())):
            for connected_id in range(len(self.output(output_id).connected_ports())):
                self.output(output_id).connected_ports()[connected_id].node().update_from_input()