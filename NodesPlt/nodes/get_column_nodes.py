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

        #   Create input port for input dataframe
        self.add_custom_input('Input DataFrame', PortValueType.PD_DATAFRAME)

        #   Create output ports for :
        #       The output dataframe corresponding to the given column
        #       The selected column name
        self.add_custom_output('Output Array', PortValueType.PD_DATAFRAME)
        self.add_custom_output('Selected column name', PortValueType.STRING)

        #   Create the QComboBox menu to select the desired column.
        self.add_combo_menu('Column name', 'Column name', items=[])


    def check_inputs(self):
        input_given = self.get_value_from_port("Input DataFrame")
        
        #   Checks if the Input DataFrame is:
        #       -   plugged
        #       -   defined (if the previous node has its outputs defined)
        #       -   is a pandas DataFrame
        self.set_property("is_valid", input_given is not None \
                                            and input_given.is_defined() \
                                                and input_given.get_property_type() == PortValueType.PD_DATAFRAME)
    
    def update_from_input(self):
        #   Called only if check_inputs returned True:
        #       -   If the combo widget labels are different from the DataFrame columns, we update the combo widget
        #       -   The "Output Array" output becomes the column asked as a DataFrame
        if list(self.get_value_from_port("Input DataFrame").get_property().columns) != self.view.widgets["Column name"].all_items():
            self.view.widgets["Column name"].clear()
            self.view.widgets["Column name"].add_items(list(self.get_value_from_port("Input DataFrame").get_property().columns))

        self.set_output_property('Output Array', self.get_value_from_port("Input DataFrame").get_property()[self.get_property("Column name")].to_frame())

    def reset_outputs(self):
        super(GetColumnNode, self).reset_outputs()

        #   If this node is reseted, the combo widget also needs to be cleared
        self.view.widgets["Column name"].clear()
        self.view.widgets["Column name"].add_items([])

