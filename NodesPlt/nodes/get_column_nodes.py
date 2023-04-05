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

        self.add_output('Column', color=(0, 255, 0))

        self.input_data_frame = None
        self.columns = None

        # create the QComboBox menu.
        self.add_combo_menu('Column name', 'Column name', items=self.columns)

        print(self.model.properties.keys())
        print(self.view)

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

        given_path = self.get_property(name)

        if os.path.isfile(given_path):
            df_data = pd.read_csv(given_path)

            print(df_data.columns)

            print(self.get_output('Output Array'))

        # F:/Documents/NodeEditor/NodeGraphQt-master/test.csv

        print("Set property called")
        
    def on_input_connected(self, in_port, out_port):
        super(GetColumnNode, self).on_input_connected(in_port, out_port)

        print(type(out_port))

        print(out_port.node)
        print(out_port.node())
        print(out_port.node().output_data_frame)

        self.input_data_frame = out_port.node().output_data_frame
        self.columns = self.input_data_frame.columns

        print(self.model.get_property("Column name"))

        print("on_input_connected", in_port, out_port, self._model.name)
    

    def on_input_disconnected(self, in_port, out_port):
        super(GetColumnNode, self).on_input_disconnected(in_port, out_port)

        print("on_input_disconnected", in_port, out_port, self._model.name)