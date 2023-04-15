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
    __identifier__ = 'Pandas'

    # initial default node name.
    NODE_NAME = 'Get column from name'

    def __init__(self):
        super(GetColumnNode, self).__init__()

        #   Create input port for input dataframe
        self.add_custom_input('Input DataFrame', PortValueType.PD_DATAFRAME)

        #   Create output ports for :
        #       The output dataframe corresponding to the given column
        #       The selected column name
        self.add_custom_output('Output DataFrame', PortValueType.PD_DATAFRAME)
        self.add_custom_output('Selected column name', PortValueType.STRING)

        #   Create the QComboBox menu to select the desired column.
        self.add_combo_menu('Column name', 'Column name', items=[])

        self.add_label("Information")
        self.change_label("Information", "No information", False)


    def check_inputs(self):
        input_given = self.get_value_from_port("Input DataFrame")
        
        #   Checks if the Input DataFrame is:
        #       -   plugged
        #       -   defined (if the previous node has its outputs defined)
        #       -   is a pandas DataFrame
        self.set_property("is_valid", input_given is not None \
                                            and input_given.is_defined() \
                                                and input_given.get_property_type() == PortValueType.PD_DATAFRAME)
        
        if input_given is None or not input_given.is_defined():
            self.change_label("Information", "Input not plugged to valid DataFrame.", True)
        elif not input_given.get_property_type() == PortValueType.PD_DATAFRAME:
            self.change_label("Information", "Plugged port is not a DataFrame.", True)
    
    def update_from_input(self):
        #   Called only if check_inputs returned True:
        #       -   If the combo widget labels are different from the DataFrame columns, we update the combo widget
        #       -   The "Output DataFrame" output becomes the column asked as a DataFrame
        if list(self.get_value_from_port("Input DataFrame").get_property().columns) != self.view.widgets["Column name"].all_items():
            self.view.widgets["Column name"].clear()
            self.view.widgets["Column name"].add_items(list(self.get_value_from_port("Input DataFrame").get_property().columns))

        self.set_output_property('Output DataFrame', self.get_value_from_port("Input DataFrame").get_property()[self.get_property("Column name")].to_frame())
        
        self.change_label("Information", "Lines : "+str(len(self.get_output_property("Output DataFrame").get_property())), False)

    def reset_outputs(self):
        super(GetColumnNode, self).reset_outputs()

        #   If this node is reseted, the combo widget also needs to be cleared
        self.view.widgets["Column name"].clear()
        self.view.widgets["Column name"].add_items([])

