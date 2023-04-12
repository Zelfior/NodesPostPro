from NodeGraphQt import BaseNode, BaseNodeCircle
from functools import wraps
from nodes.generic_node import GenericNode, PortValueType

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
        self.add_custom_input('Input Dataframe', PortValueType.PD_DATAFRAME)

        self.add_custom_output('Output Array', PortValueType.PD_DATAFRAME)
        self.add_custom_output('Selected column name', PortValueType.STRING)

        # create the QComboBox menu.
        self.add_combo_menu('Column name', 'Column name', items=[])


    def check_inputs(self):
        self.set_property("is_valid", type(self.get_value_from_port("Input DataFrame")) == pd.DataFrame and \
                                                self.get_property("Column name") in self.get_value_from_port("Input DataFrame").columns)
    
    def update_from_input(self):

        self.set_property('Input Dataframe', self.get_value_from_port("Input Dataframe"))

        if self.get_property('Input Dataframe').columns != self.view.widgets["Column name"].all_items():
            self.view.widgets["Column name"].clear()
            self.view.widgets["Column name"].add_items(list(self.get_property('Input Dataframe').columns))

        self.output_array = self.get_property('Input Dataframe')[self.get_property("Column name")]
