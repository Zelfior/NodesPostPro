from nodes.generic_node import GenericNode, PortValueType

import pandas as pd
import os


class LoadFileNode(GenericNode):
    """
    An example of a node with a embedded QLineEdit.
    """

    # unique node identifier.
    __identifier__ = 'Pandas'

    # initial default node name.
    NODE_NAME = 'Read CSV file'

    def __init__(self):
        super(LoadFileNode, self).__init__()

        #   create output port for the read dataframe
        self.add_custom_output('Output DataFrame', PortValueType.PD_DATAFRAME)

        #   create QLineEdit text input widget for the file path
        self.add_text_input('Filename', 'File name', 'test.csv', tab='widgets')

        self.add_label("Information")

        self.property_to_update.append("Filename")


    def check_inputs(self):
        print("File found", os.path.isfile(self.get_property("Filename")))

        #   we set in the "is_valid" property a boolean saying if a file is present at the given path
        if os.path.isfile(self.get_property("Filename")):
            self.set_property("is_valid", True)
        else:
            self.set_property("is_valid", False)
            self.change_label("Information", "No file at the given path.", True)

    

    def update_from_input(self):
        #   Called only if check_inputs returned True:
        #       we set in the "Output DataFrame" output the dataframe associated to the given path
        self.get_output_property("Output DataFrame").set_property(pd.read_csv(self.get_property("Filename"), sep = ","))

        column_count = len(self.get_output_property("Output DataFrame").get_property().columns)
        lines_count = len(self.get_output_property("Output DataFrame").get_property())
        
        self.change_label("Information", "Columns : "+str(column_count)+", lines : "+str(lines_count), False)