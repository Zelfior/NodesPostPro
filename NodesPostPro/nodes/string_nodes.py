from NodesPostPro.nodes.generic_node import GenericNode, PortValueType
        

class ReplaceNode(GenericNode):
    # unique node identifier.
    __identifier__ = 'String'
    # initial default node name.
    NODE_NAME = 'Replace'

    def __init__(self):
        super(ReplaceNode, self).__init__()

        # create input & output ports
        self.add_custom_input('Input', PortValueType.STRING)
        self.add_twin_input("From", PortValueType.STRING)
        self.add_twin_input("To", PortValueType.STRING)
        self.add_custom_output('Output', PortValueType.STRING)

        self.add_label("Information")
        
        self.is_iterated_compatible = True
        
    
    def check_function(self, input_dict, first = False):
        if (not "Input" in input_dict) or ("is not defined" in input_dict["Input"]):
            return False, "Input not valid", "Information"
        
        if (not "From" in input_dict) or ("is not defined" in input_dict["From"]):
            return False, "Input \'From\' not valid", "Information"
            
        if (not "To" in input_dict) or ("is not defined" in input_dict["To"]):
            return False, "Input \'To\' not valid", "Information"
        
        return True, "", "Information"

    def update_function(self, input_dict, first = False):
        output_dict = {}

        output_dict["Output"] = input_dict["Input"].replace(input_dict["From"], input_dict["To"])

        output_dict["__message__Information"] = "Output: "+str(output_dict["Output"])

        return output_dict
        





