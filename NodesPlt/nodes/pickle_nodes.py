from nodes.generic_node import GenericNode, PortValueType

import pandas as pd
import numpy as np
import os
import pickle


class LoadNumpyNode(GenericNode):
    """
    An example of a node with a embedded QLineEdit.
    """

    # unique node identifier.
    __identifier__ = 'Pickle'

    # initial default node name.
    NODE_NAME = 'Load Numpy array'

    def __init__(self):
        super(LoadNumpyNode, self).__init__()

        #   create output port for the read dataframe
        self.add_custom_output('Output Array', PortValueType.NP_ARRAY)

        #   create QLineEdit text input widget for the file path
        self.add_text_input('Filename', 'File name', 'example.pkl', tab='widgets')

        self.add_label("Information")


    def check_inputs(self):
        #   we set in the "is_valid" property a boolean saying if a file is present at the given path
        if os.path.isfile(self.get_property("Filename")):
            try :
                self.data = pickle.load(open(self.get_property("Filename"), "rb"))
            except:
                self.set_property("is_valid", False)
                self.change_label("Information", "File found not valid.", True)
                return

            if type(self.data) == np.ndarray:
                self.set_property("is_valid", True)
            else:
                self.change_label("Information", "Loaded data is not a numpy array.", True)

        else:
            self.set_property("is_valid", False)
            self.change_label("Information", "No file at the given path.", True)

    

    def update_from_input(self):
        #   Called only if check_inputs returned True:
        #       we set in the "Output Array" output the array associated to the given path
        self.get_output_property("Output Array").set_property(self.data)
        
        self.change_label("Information", "Array shape : "+str(self.data.shape), False)

    

class LoadPandasNode(GenericNode):
    """
    An example of a node with a embedded QLineEdit.
    """

    # unique node identifier.
    __identifier__ = 'Pickle'

    # initial default node name.
    NODE_NAME = 'Load Pandas array'

    def __init__(self):
        super(LoadPandasNode, self).__init__()

        #   create output port for the read dataframe
        self.add_custom_output('Output DataFrame', PortValueType.PD_DATAFRAME)

        #   create QLineEdit text input widget for the file path
        self.add_text_input('Filename', 'File name', 'example.pkl', tab='widgets')

        self.add_label("Information")

        self.check_inputs()


    def check_inputs(self):
        #   we set in the "is_valid" property a boolean saying if a file is present at the given path
        if os.path.isfile(self.get_property("Filename")):
            try :
                self.data = pickle.load(open(self.get_property("Filename"), "rb"))
            except:
                self.set_property("is_valid", False)
                self.change_label("Information", "File found not valid.", True)
                return

            if type(self.data) == pd.DataFrame:
                self.set_property("is_valid", True)
            else:
                self.change_label("Information", "Loaded data is not a pandas dataframe.", True)

        else:
            self.set_property("is_valid", False)
            self.change_label("Information", "No file at the given path.", True)

    

    def update_from_input(self):
        #   Called only if check_inputs returned True:
        #       we set in the "Output DataFrame" output the dataframe associated to the given path
        self.get_output_property("Output DataFrame").set_property(self.data)
        
        column_count = len(self.get_output_property("Output DataFrame").get_property().columns)
        lines_count = len(self.get_output_property("Output DataFrame").get_property())
        
        self.change_label("Information", "Columns : "+str(column_count)+", lines : "+str(lines_count), False)