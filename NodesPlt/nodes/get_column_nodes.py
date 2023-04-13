from NodeGraphQt import BaseNode, BaseNodeCircle
from functools import wraps
from nodes.generic_node import GenericNode, PortValueType, get_reset_value_from_enum

import pandas as pd
import os


class GetColumnNode(GenericNode):
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
        self.add_custom_input('Input DataFrame', PortValueType.PD_DATAFRAME)

        self.add_custom_output('Output Array', PortValueType.PD_DATAFRAME)
        self.add_custom_output('Selected column name', PortValueType.STRING)

        # create the QComboBox menu.
        self.add_combo_menu('Column name', 'Column name', items=[])

        self.input_data_frame = pd.DataFrame()
        self.output_array = pd.DataFrame()


    def check_inputs(self):
        print("=========== checking inputs =========")
        input_given = self.get_value_from_port("Input DataFrame")
        print("returned input:", input_given)
        self.set_property("is_valid", type(self.get_value_from_port("Input DataFrame")) == pd.DataFrame)# and \
                                                # self.get_property("Column name") in self.get_value_from_port("Input DataFrame").columns)
    
    def update_from_input(self):
        print("___________update_from_input, df got, ",self.get_value_from_port("Input DataFrame"))
        self.set_property('Input DataFrame', self.get_value_from_port("Input DataFrame"))

        print(self.get_property('Input DataFrame').columns)
        print(self.view.widgets["Column name"].all_items())

        if list(self.get_property('Input DataFrame').columns) != self.view.widgets["Column name"].all_items():
            self.view.widgets["Column name"].clear()
            self.view.widgets["Column name"].add_items(list(self.get_property('Input DataFrame').columns))

        self.output_array = self.get_property('Input DataFrame')[self.get_property("Column name")]

    def get_property(self, name):
        if name == 'Output Array':
            return self.output_array
        
        if name == 'Input DataFrame':
            return self.input_data_frame

        return super().get_property(name)
    
    def set_property(self, name, value, push_undo=True):
        if name == 'Output Array':
            self.output_array = value
            
            # if not self.is_reseting:
            #     self.update_values()
                
        elif name == 'Input DataFrame':
            self.input_data_frame = value
            
            # if not self.is_reseting:
            #     self.update_values()

            return self.input_data_frame
        else:
            return super().set_property(name, value, push_undo)
        
        
    def is_output_port_defined(self, port_name):
        if port_name == 'Output Array':
            return not self.output_array.empty
        else:
            return self.get_property(port_name) != get_reset_value_from_enum(self.output_type_list[port_name])