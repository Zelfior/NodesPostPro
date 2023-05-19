from NodesPostPro.nodes.generic_node import GenericNode, PortValueType

import math

        

class OneMathNode(GenericNode):
    # unique node identifier.
    __identifier__ = 'Math'
    # initial default node name.
    NODE_NAME = 'One number'

    def __init__(self):
        super(OneMathNode, self).__init__()

        # create input & output ports
        self.add_custom_input('Input', PortValueType.NUMBER)
        self.add_custom_output('Output', PortValueType.NUMBER)

        self.add_combo_menu('Operation', 'Operation', ["Square", "Sqrt", "Ln", "Log", "Exp", "Inverse"])
                               
        self.add_label("Information")
        
    
    def check_function(self, input_dict, first = False):
        if (not "Input" in input_dict) or (type(input_dict["Input"]) == str):
            return False, "Input not valid", "Information"
        
        if self.get_property("Operation") == "Sqrt" and input_dict["Input"] < 0.:
            return False, "Input cannot be negative.", "Information"
        
        if self.get_property("Operation") == "Ln" and input_dict["Input"] <= 0.:
            return False, "Input cannot be negative or 0.", "Information"
        
        if self.get_property("Operation") == "Log" and input_dict["Input"] <= 0.:
            return False, "Input cannot be negative or 0.", "Information"
        
        if self.get_property("Operation") == "Inverse" and input_dict["Input"] == 0.:
            return False, "Input cannot be 0.", "Information"
        
        return True, "", "Information"

    def update_function(self, input_dict, first = False):
        output_dict = {}


        operation = self.get_property("Operation")
        if operation == "Sqrt":
            output_dict["Output"] = math.sqrt(input_dict["Input"])
        elif operation == "Square":
            output_dict["Output"] = math.pow(input_dict["Input"], 2)
        elif operation == "Ln":
            output_dict["Output"] = math.log(input_dict["Input"])
        elif operation == "Log":
            output_dict["Output"] = math.log10(input_dict["Input"])
        elif operation == "Exp":
            output_dict["Output"] = math.exp(input_dict["Input"])
        elif operation == "Inverse":
            output_dict["Output"] = 1./input_dict["Input"]
        else:
            raise NotImplementedError("Operation "+operation+" not implemented in one number math node.")

        output_dict["__message__Information"] = "Output: "+str(output_dict["Output"])

        return output_dict
        

class TwoMathNode(GenericNode):
    # unique node identifier.
    __identifier__ = 'Math'
    # initial default node name.
    NODE_NAME = 'Two numbers'

    def __init__(self):
        super(TwoMathNode, self).__init__()

        # create input & output ports
        self.add_custom_input('Input 1', PortValueType.NUMBER)
        self.add_custom_input('Input 2', PortValueType.NUMBER)
        self.add_custom_output('Output', PortValueType.NUMBER)

        self.add_combo_menu('Operation', 'Operation', ["Add", "Subtract", "Multiply", "Divide", "Power"])
                               
        self.add_label("Information")
        
    
    def check_function(self, input_dict, first = False):
        if (not "Input 1" in input_dict) or (type(input_dict["Input 1"]) == str):
            return False, "Input 1 not valid", "Information"
        
        if (not "Input 2" in input_dict) or (type(input_dict["Input 2"]) == str):
            return False, "Input 2 not valid", "Information"
        
        if self.get_property("Operation") == "Divide" and input_dict["Input 2"] == 0.:
            return False, "Cannot divide by 0.", "Information"
        
        if self.get_property("Operation") == "Power" and (input_dict["Input 1"] == 0. and input_dict["Input 2"] == 0.\
                                                            or input_dict["Input 1"] < 0. and int(input_dict["Input 2"]) != input_dict["Input 2"]):
            return False, "Input 1 and 2 are not compatible.", "Information"

        return True, "", "Information"
        

    def update_function(self, input_dict, first = False):
        output_dict = {}

        operation = self.get_property("Operation")
        if operation == "Add":
            output_dict["Output"] = input_dict["Input 1"] + input_dict["Input 2"]
        elif operation == "Subtract":
            output_dict["Output"] = input_dict["Input 1"] - input_dict["Input 2"]
        elif operation == "Multiply":
            output_dict["Output"] = input_dict["Input 1"] * input_dict["Input 2"]
        elif operation == "Divide":
            output_dict["Output"] = input_dict["Input 1"] / input_dict["Input 2"]
        elif operation == "Power":
            output_dict["Output"] = math.pow(input_dict["Input 1"], input_dict["Input 2"])
        else:
            raise NotImplementedError("Operation "+operation+" not implemented in two numbers math node.")

        output_dict["__message__Information"] = "Output: "+str(output_dict["Output"])

        return output_dict
        