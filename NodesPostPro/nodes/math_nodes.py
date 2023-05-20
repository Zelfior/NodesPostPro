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

        self.add_combo_menu('Operation', 'Operation', ["Absolute", "Square", "Sqrt", "Ln", "Log", "Exp", "Inverse", "Sign"])
                               
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
        elif operation == "Absolute":
            output_dict["Output"] = abs(input_dict["Input"])
        elif operation == "Sign":
            if input_dict["Input"] >= 0:
                output_dict["Output"] = 1
            else:
                output_dict["Output"] = -1
        elif operation == "Inverse":
            output_dict["Output"] = 1./input_dict["Input"]
        else:
            raise NotImplementedError("Operation "+operation+" not implemented in one number math node.")

        output_dict["__message__Information"] = "Output: "+str(output_dict["Output"])

        return output_dict
        







class OneMathNode(GenericNode):
    # unique node identifier.
    __identifier__ = 'Math'
    # initial default node name.
    NODE_NAME = 'Trigonometry'

    def __init__(self):
        super(OneMathNode, self).__init__()

        # create input & output ports
        self.add_custom_input('Input', PortValueType.NUMBER)
        self.add_custom_output('Output', PortValueType.NUMBER)

        self.add_combo_menu('Operation', 'Operation', ["Sin", "Cos", "Tan", "Asin", "Acos", "Atan"])
                               
        self.add_label("Information")
        
    
    def check_function(self, input_dict, first = False):
        if (not "Input" in input_dict) or (type(input_dict["Input"]) == str):
            return False, "Input not valid", "Information"
        
        if self.get_property("Operation") in ["Asin", "Acos"] and (input_dict["Input"] < 1. or input_dict["Input"] > 1.):
            return False, "Input should be between -1. and 1..", "Information"
        
        if self.get_property("Operation") == "Tan" and ((input_dict["Input"] + math.pi/2)%math.pi == 0.):
            return False, "tan(Input) impossible.", "Information"
        
        return True, "", "Information"

    def update_function(self, input_dict, first = False):
        output_dict = {}


        operation = self.get_property("Operation")
        if operation == "Sin":
            output_dict["Output"] = math.sin(input_dict["Input"])
        elif operation == "Cos":
            output_dict["Output"] = math.cos(input_dict["Input"])
        elif operation == "Tan":
            output_dict["Output"] = math.tan(input_dict["Input"])
        elif operation == "Asin":
            output_dict["Output"] = math.asin(input_dict["Input"])
        elif operation == "Acos":
            output_dict["Output"] = math.acos(input_dict["Input"])
        elif operation == "Atan":
            output_dict["Output"] = math.atan(input_dict["Input"])
        else:
            raise NotImplementedError("Operation "+operation+" not implemented in trigonometry math node.")

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

        self.add_combo_menu('Operation', 'Operation', ["Add", "Subtract", "Multiply", "Divide", "Power", "Modulo", "Round"])
                               
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

        if self.get_property("Operation") == "Modulo" and input_dict["Input 2"] == 0.:
            return False, "Cannot divide by 0.", "Information"

        if self.get_property("Operation") == "Round" and (int(input_dict["Input 2"]) != input_dict["Input 2"]):
            return False, "Input 2 invalid.", "Information"
        
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
        elif operation == "Modulo":
            output_dict["Output"] = input_dict["Input 1"]%input_dict["Input 2"]
        elif operation == "Round":
            output_dict["Output"] = round(input_dict["Input 1"], int(input_dict["Input 2"]))
        else:
            raise NotImplementedError("Operation "+operation+" not implemented in two numbers math node.")

        output_dict["__message__Information"] = "Output: "+str(output_dict["Output"])

        return output_dict
        