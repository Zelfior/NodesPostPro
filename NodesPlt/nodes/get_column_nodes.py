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


    def check_inputs(self):
        input_given = self.get_value_from_port("Input DataFrame")
        
        self.set_property("is_valid", input_given is not None \
                                            and input_given.is_defined() \
                                                and input_given.get_property_type() == PortValueType.PD_DATAFRAME)
    
    def update_from_input(self):
        if list(self.get_value_from_port("Input DataFrame").get_property().columns) != self.view.widgets["Column name"].all_items():
            self.view.widgets["Column name"].clear()
            self.view.widgets["Column name"].add_items(list(self.get_value_from_port("Input DataFrame").get_property().columns))

        self.set_output_property('Output Array', self.get_value_from_port("Input DataFrame").get_property()[self.get_property("Column name")].to_frame())

    def reset_outputs(self):
        super(GetColumnNode, self).reset_outputs()

        self.view.widgets["Column name"].clear()
        self.view.widgets["Column name"].add_items([])

