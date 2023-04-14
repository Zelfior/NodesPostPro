from nodes.generic_node import GenericNode, PortValueType

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

        #   create output port for the read dataframe
        self.add_custom_output('Output DataFrame', PortValueType.PD_DATAFRAME)

        #   create QLineEdit text input widget for the file path
        self.add_text_input('Filename', 'File name', tab='widgets')


    def check_inputs(self):
        print("File found", os.path.isfile(self.get_property("Filename")))

        #   we set in the "is_valid" property a boolean saying if a file is present at the given path
        self.set_property("is_valid", os.path.isfile(self.get_property("Filename")))
    

    def update_from_input(self):
        #   Called only if check_inputs returned True:
        #       we set in the "Output DataFrame" output the dataframe associated to the given path
        self.get_output_property("Output DataFrame").set_property(pd.read_csv(self.get_property("Filename"), sep = ","))