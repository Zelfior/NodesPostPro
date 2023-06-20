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




