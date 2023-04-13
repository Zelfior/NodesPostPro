from NodeGraphQt import BaseNode, BaseNodeCircle
from functools import wraps
from nodes.generic_node import GenericNode, PortValueType, get_reset_value_from_enum

import pandas as pd
import os


class LoadFileNode(GenericNode):
    """
    An example of a node with a embedded QLineEdit.
    """

    # unique node identifier.
    __identifier__ = 'nodes.Pandas'

    # initial default node name.
    NODE_NAME = 'Read CSV file'

    def __init__(self):
        super(LoadFileNode, self).__init__()

        # create input & output ports
        self.add_custom_output('Output DataFrame', PortValueType.PD_DATAFRAME)

        # create QLineEdit text input widget.
        self.add_text_input('Filename', 'File name', tab='widgets')

        self.output_data_frame = pd.DataFrame()


    def check_inputs(self):
        print("File found", os.path.isfile(self.get_property("Filename")))
        self.set_property("is_valid", os.path.isfile(self.get_property("Filename")))
    

    def update_from_input(self):
        self.output_data_frame = pd.read_csv(self.get_property("Filename"), sep = ",")

    def get_property(self, name):
        if name == 'Output DataFrame':
            return self.output_data_frame

        return super().get_property(name)
    
    def set_property(self, name, value, push_undo=True):
        if name == 'Output DataFrame':
            return
        else:
            return super().set_property(name, value, push_undo)
        
        
    def is_output_port_defined(self, port_name):
        if port_name == 'Output DataFrame':
            print("______port defined______", not self.output_data_frame.empty)
            return not self.output_data_frame.empty
        else:
            return self.get_property(port_name) != get_reset_value_from_enum(self.output_type_list[port_name])