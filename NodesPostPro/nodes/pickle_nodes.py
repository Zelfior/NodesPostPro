from NodesPostPro.nodes.generic_node import GenericNode, PortValueType

import pandas as pd
import numpy as np
import os
import pickle
import sys
from NodesPostPro.nodes.container import check_type


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

        self.button = self.add_button_widget("Browse file")
        self.button.set_link(self.get_file_name)

        #   create QLineEdit text input widget for the file path
        file_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        example_path = os.path.join(file_path, 'example_files','example.pkl')
        self.add_twin_input('Filename', PortValueType.STRING, default = example_path)

        self.add_label("Information")
        self.change_label("Information", "Load file to display size", False)

        self.add_label("Python version", label=True)
        self.change_label("Python version", str(sys.version).split("(")[0], False)
        self.add_label("Numpy version", label=True)
        self.change_label("Numpy version", str(np.__version__), False)
        self.add_label("Pickle version", label=True)
        self.change_label("Pickle version", str(pickle.format_version), False)

        self.update_values()

        self.is_iterated_compatible = True
        

    def check_function(self, input_dict, first=False):
        if (not "Filename" in input_dict) or ("is not defined" in input_dict["Filename"]):
            return False, "Filename is not valid", "Information"
        
        if not os.path.isfile(self.get_property("Filename")):
            return False, "No file at given path", "Information"
        
        try :
            self.data = pickle.load(open(self.get_property("Filename"), "rb"))

            if not check_type(self.data, PortValueType.NP_ARRAY):
                return False, "Loaded data is not a numpy array", "Information"
        except:
            return False, "Found file is not valid", "Information"
        
        return True, "", "Information"

    
    def update_function(self, input_dict, first=False):
        output_dict = {'Output Array': self.data}
        
        output_dict["__message__Information"] = "Output shape : "+str(output_dict["Output Array"].shape)

        return output_dict



    

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
        self.add_custom_output('Columns names', PortValueType.LIST)

        #   create QLineEdit text input widget for the file path
        self.button = self.add_button_widget("Browse file")
        self.button.set_link(self.get_file_name)

        file_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        example_path = os.path.join(file_path, 'example_files','example.pkl')
        self.add_twin_input('Filename', PortValueType.STRING, default = example_path)

        self.add_label("Information")
        self.change_label("Information", "Load file to display size", False)

        self.add_label("Python version", label=True)
        self.change_label("Python version", str(sys.version).split("(")[0], False)
        self.add_label("Pandas version", label=True)
        self.change_label("Pandas version", str(pd.__version__), False)
        self.add_label("Pickle version", label=True)
        self.change_label("Pickle version", str(pickle.format_version), False)

        self.is_iterated_compatible = True

        self.update_values()

    def check_function(self, input_dict, first=False):
        if (not "Filename" in input_dict) or ("is not defined" in input_dict["Filename"]):
            return False, "Filename is not valid", "Information"
        
        if not os.path.isfile(self.get_property("Filename")):
            return False, "No file at given path", "Information"
        
        try :
            self.data = pickle.load(open(self.get_property("Filename"), "rb"))

            if not check_type(self.data, PortValueType.PD_DATAFRAME):
                return False, "Loaded data is not a pandas dataframe", "Information"
        except:
            return False, "Found file is not valid", "Information"
        
        return True, "", "Information"

    
    def update_function(self, input_dict, first=False):
        output_dict = {'Output DataFrame': self.data}
        
        column_count = len(self.data.columns)
        lines_count = len(self.data)

        output_dict["__message__Information"] = "Output shape : "+str(output_dict["Output Array"].shape)

        return output_dict

