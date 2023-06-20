from NodesPostPro.nodes.generic_node import GenericNode, PortValueType

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
        self.add_custom_output('Columns names', PortValueType.LIST)

        #   create QLineEdit text input widget for the file path
        self.button = self.add_button_widget("Browse file")
        self.button.set_link(self.get_file_name)

        file_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        example_path = os.path.join(file_path, 'example_files', 'test.csv')
        self.add_twin_input('Filename', PortValueType.STRING, default = example_path)
        self.add_twin_input('Separator', PortValueType.STRING, default =  ',')

        self.add_label("Information")

        self.is_iterated_compatible = True

        self.update_values()

        
    def check_function(self, input_dict, first=False):
        if (not "Filename" in input_dict) or ("is not defined" in input_dict["Filename"]):
            return False, "Filename is not valid", "Information"
        
        if not os.path.isfile(input_dict["Filename"]):
            return False, "No file at the given path", "Information"

        return True, "", "Information"

    
    def update_function(self, input_dict, first=False):
        if "Separator" in input_dict:
            output_dict = {'Output DataFrame': pd.read_csv(input_dict["Filename"], sep=input_dict["Separator"])}
        else:
            output_dict = {'Output DataFrame': pd.read_csv(input_dict["Filename"])}

        output_dict["Columns names"] = list(output_dict['Output DataFrame'].columns)
        
        column_count = len(output_dict["Columns names"])
        lines_count = len(output_dict["Output DataFrame"])
        
        output_dict["__message__Information"] = "Columns : "+str(column_count)+", lines : "+str(lines_count)

        return output_dict








        

class GetColumnSelectorNode(GenericNode):
    """
    An example of a node with a embedded QLineEdit.
    """

    # unique node identifier.
    __identifier__ = 'Pandas'

    # initial default node name.
    NODE_NAME = 'Get column selector'

    def __init__(self):
        super(GetColumnSelectorNode, self).__init__()

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

        self.is_iterated_compatible = True


    def check_function(self, input_dict, first=False):
        if (not "Input DataFrame" in input_dict) or (type(input_dict["Input DataFrame"]) == str):
            return False, "Input DataFrame is not valid", "Information"
        
        return True, "", "Information"

    
    def update_function(self, input_dict, first=False):
        if first:
            if list(input_dict["Input DataFrame"].columns) != self.view.widgets["Column name"].all_items():
                self.view.widgets["Column name"].clear()
                self.view.widgets["Column name"].add_items(list(input_dict["Input DataFrame"].columns))
            
        output_dict = {}

        
        if "Column name" not in input_dict or not (input_dict["Column name"] in input_dict["Input DataFrame"]):
            if list(input_dict["Input DataFrame"].columns) != self.view.widgets["Column name"].all_items():
                self.view.widgets["Column name"].clear()
                self.view.widgets["Column name"].add_items(list(input_dict["Input DataFrame"].columns))

            input_dict["Column name"] = input_dict["Input DataFrame"].columns[0]

        if "Column name" in input_dict:
            output_dict['Output DataFrame'] = input_dict["Input DataFrame"][input_dict["Column name"]].to_frame()
            output_dict['Selected column name'] = input_dict["Column name"]
        
        output_dict["__message__Information"] = "Lines : "+str(len(input_dict['Input DataFrame']))

        return output_dict

    
    def reset_outputs(self):
        super(GetColumnSelectorNode, self).reset_outputs()

        #   If this node is reseted, the combo widget also needs to be cleared
        self.view.widgets["Column name"].clear()
        self.view.widgets["Column name"].add_items([])







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
        self.add_twin_input('Column name', PortValueType.STRING)

        #   Create output ports for :
        #       The output dataframe corresponding to the given column
        #       The selected column name
        self.add_custom_output('Output DataFrame', PortValueType.PD_DATAFRAME)

        self.add_label("Information")
        self.change_label("Information", "No information", False)

        self.is_iterated_compatible = True
        
    def check_function(self, input_dict, first=False):
        if (not "Input DataFrame" in input_dict) or (type(input_dict["Input DataFrame"]) == str):
            return False, "Input DataFrame is not valid", "Information"
        
        if (not "Column name" in input_dict) or ("is not defined" in input_dict["Column name"]):
            return False, "Column name is not valid", "Information"
        
        if not input_dict["Column name"] in input_dict["Input DataFrame"].columns:
            return False, "Column name given is not valid", "Information"
        
        return True, "", "Information"

    
    def update_function(self, input_dict, first=False):
        output_dict = {'Output DataFrame': input_dict["Input DataFrame"][input_dict["Column name"]].to_frame()}
        
        output_dict["__message__Information"] = "Output shape : "+str(output_dict["Output DataFrame"].shape)

        return output_dict





class MultiplyNode(GenericNode):
    """
    A node class with 2 inputs and 2 outputs.
    """

    # unique node identifier.
    __identifier__ = 'Pandas'

    # initial default node name.
    NODE_NAME = 'DF Multiply float'

    def __init__(self):
        super(MultiplyNode, self).__init__()

        # create input & output ports
        self.add_custom_input('Input Dataframe', PortValueType.PD_DATAFRAME)
        self.add_twin_input('Input float', PortValueType.FLOAT)
        self.add_custom_output('Output Dataframe', PortValueType.PD_DATAFRAME)
        
        self.add_label("Information")

        self.is_iterated_compatible = True

        
    def check_function(self, input_dict, first=False):
        if (not "Input DataFrame" in input_dict) or (type(input_dict["Input DataFrame"]) == str):
            return False, "Input Dataframe 1 is not valid", "Information"
        if (not "Input Float" in input_dict) or (type(input_dict["Input Float"]) == str):
            return False, "Input Float is not valid", "Information"
        
        return True, "", "Information"

    
    def update_function(self, input_dict, first=False):
        output_dict = {'Output Dataframe': input_dict["Input Dataframe"] * input_dict["Input Float"]}
        
        output_dict["__message__Information"] = "Output shape : "+str(output_dict["Output Dataframe"].shape)

        return output_dict



class GetAverageNode(GenericNode):
    """
    A node class with 2 inputs and 2 outputs.
    """

    # unique node identifier.
    __identifier__ = 'Pandas'

    # initial default node name.
    NODE_NAME = 'DF average'

    def __init__(self):
        super(GetAverageNode, self).__init__()

        # create input & output ports
        self.add_custom_input('Input Dataframe', PortValueType.PD_DATAFRAME)
        self.add_custom_output('Output Float', PortValueType.FLOAT)
        
        self.add_label("Information")

        self.is_iterated_compatible = True
        
    def check_function(self, input_dict, first=False):
        if (not "Input DataFrame" in input_dict) or (type(input_dict["Input DataFrame"]) == str):
            return False, "Input Dataframe 1 is not valid", "Information"
        
        return True, "", "Information"

    
    def update_function(self, input_dict, first=False):
        output_dict = {'Output Dataframe': input_dict["Input Dataframe"].mean()}
        
        output_dict["__message__Information"] = "Output shape : "+str(output_dict["Output Dataframe"].shape)

        return output_dict

