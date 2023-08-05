from NodesPostPro.nodes.generic_node import GenericNode, PortValueType
from NodesPostPro.nodes.container import check_type

class PrintNode(GenericNode):
    """
    An example of a node with a embedded QLineEdit.
    """

    # unique node identifier.
    __identifier__ = 'Tools'

    # initial default node name.
    NODE_NAME = 'Print'

    def __init__(self):
        super(PrintNode, self).__init__()

        #   create output port for the read dataframe
        self.add_custom_input('Input', PortValueType.ANY)

        self.add_label("Information")

        self.is_iterated_compatible = True

        
    def check_function(self, input_dict, first=False):
        if (not "Input" in input_dict) or (check_type(input_dict["Input"], PortValueType.STRING) and "is not defined" in input_dict["Input"]):
            return False, "Input is not valid", "Information"
        
        return True, "", "Information"

    
    def update_function(self, input_dict, first=False):
        
        output_dict = {}
        output_dict["__message__Information"] = str(input_dict["Input"])
        if check_type(input_dict["Input"], PortValueType.DICT):
            output_dict["__message__Information"] = output_dict["__message__Information"].replace(", \'", ",\n\'")

        return output_dict



class IntSelectionNode(GenericNode):
    """
    An example of a node with a embedded QLineEdit.
    """

    # unique node identifier.
    __identifier__ = 'Tools'

    # initial default node name.
    NODE_NAME = 'Int Slider'

    def __init__(self):
        super(IntSelectionNode, self).__init__()

        #   create output port for the read dataframe
        self.add_twin_input('Min', PortValueType.INTEGER, default="0")
        self.add_twin_input('Max', PortValueType.INTEGER, default="10")

        self.add_custom_output('Output', PortValueType.INTEGER)

        self.slider = self.add_slider("int_selector")
        self.add_label("Information")
                        
        # self.is_iterated_compatible = True

    
        
    def check_function(self, input_dict, first=False):
        if (not "Min" in input_dict) or (check_type(input_dict["Min"], PortValueType.STRING) and "is not defined" in input_dict["Min"]):
            return False, "Min is not valid", "Information"
        
        if (not "Max" in input_dict) or (check_type(input_dict["Max"], PortValueType.STRING) and "is not defined" in input_dict["Max"]):
            return False, "Min is not valid", "Information"
        
        return True, "", "Information"

    
    def update_function(self, input_dict, first=False):
        self.slider.set_range(input_dict["Min"], input_dict["Max"])

        output_dict = {}
        output_dict["Output"] = input_dict["Min"] + input_dict["int_selector"]

        output_dict["__message__Information"] = str(output_dict["Output"])

        return output_dict


