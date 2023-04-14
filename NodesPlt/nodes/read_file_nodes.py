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


    def check_inputs(self):
        print("File found", os.path.isfile(self.get_property("Filename")))
        self.set_property("is_valid", os.path.isfile(self.get_property("Filename")))
    

    def update_from_input(self):
        self.get_output_property("Output DataFrame").set_property(pd.read_csv(self.get_property("Filename"), sep = ","))