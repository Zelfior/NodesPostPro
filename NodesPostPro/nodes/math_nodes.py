from NodesPostPro.nodes.generic_node import GenericNode, PortValueType
from NodesPostPro.nodes.container import check_type, are_comparable

import math
import numpy as np
import pandas as pd

def apply_function(value, function):
    if check_type(value, PortValueType.PD_DATAFRAME):
        return value.apply(function)
    elif check_type(value, PortValueType.FLOAT):
        return float(function(value))
    elif check_type(value, PortValueType.INTEGER):
        return int(function(value))
    elif check_type(value, PortValueType.NP_ARRAY):
        return function(value)
    else:
        raise ValueError("Wrong type given in apply_function : "+str(type(value)))
        
def apply_twin_function(value1, value2, function):
    if check_type(value1, PortValueType.PD_DATAFRAME):
        return function(value1, value2) # Works considering value 2 is a float as a condition in check_function
    elif check_type(value1, PortValueType.NP_ARRAY):
        return function(value1, value2)
    else:
        raise ValueError("Wrong type given in apply_twin_function : "+str(type(value1)))

def object_clone(value_to_clone, target_value):
    if check_type(target_value, PortValueType.PD_DATAFRAME):
        return target_value*0 + value_to_clone
    elif check_type(target_value, PortValueType.NP_ARRAY):
        return target_value*0 + value_to_clone
    elif check_type(target_value, PortValueType.LIST):
        return [target_value for i in range(len(target_value))]
    else:
        raise ValueError("Function object_clone not implemented for type : "+str(type(target_value)))


class OneMathNode(GenericNode):
    # unique node identifier.
    __identifier__ = 'Math'
    # initial default node name.
    NODE_NAME = 'One element'

    def __init__(self):
        super(OneMathNode, self).__init__()

        # create input & output ports
        self.add_custom_input('Input', PortValueType.MATH_COMPATIBLE)
        self.add_custom_output('Output', PortValueType.MATH_COMPATIBLE)

        self.add_combo_menu('Operation', 'Operation', ["Absolute", "Square", "Sqrt", "Ln", "Log", "Exp", "Inverse", "Sign"])
                               
        self.add_label("Information")

        self.is_iterated_compatible = True
        
    
    def check_function(self, input_dict, first = False):
        if (not "Input" in input_dict) or (type(input_dict["Input"]) == str):
            return False, "Input not valid", "Information"
        
        if self.get_property("Operation") == "Sqrt" and check_type(input_dict["Input"], PortValueType.NUMBER) and input_dict["Input"] < 0.:
            return False, "Input cannot be negative.", "Information"
        
        if self.get_property("Operation") == "Ln" and check_type(input_dict["Input"], PortValueType.NUMBER) and input_dict["Input"] <= 0.:
            return False, "Input cannot be negative or 0.", "Information"
        
        if self.get_property("Operation") == "Log" and check_type(input_dict["Input"], PortValueType.NUMBER) and input_dict["Input"] <= 0.:
            return False, "Input cannot be negative or 0.", "Information"
        
        if self.get_property("Operation") == "Inverse" and check_type(input_dict["Input"], PortValueType.NUMBER) and input_dict["Input"] == 0.:
            return False, "Input cannot be 0.", "Information"
        
        return True, "", "Information"

    def update_function(self, input_dict, first = False):
        output_dict = {}


        operation = self.get_property("Operation")
        if operation == "Sqrt":
            output_dict["Output"] = apply_function(input_dict["Input"], np.sqrt)
        elif operation == "Square":
            output_dict["Output"] = apply_function(input_dict["Input"], np.square)
        elif operation == "Ln":
            output_dict["Output"] = apply_function(input_dict["Input"], np.log)
        elif operation == "Log":
            output_dict["Output"] = apply_function(input_dict["Input"], np.log10)
        elif operation == "Exp":
            output_dict["Output"] = apply_function(input_dict["Input"], np.exp)
        elif operation == "Absolute":
            output_dict["Output"] = apply_function(input_dict["Input"], np.abs)
        elif operation == "Sign":
            output_dict["Output"] = apply_function(input_dict["Input"], np.sign)
        elif operation == "Inverse":
            output_dict["Output"] = apply_function(input_dict["Input"], np.reciprocal)
        else:
            raise NotImplementedError("Operation "+operation+" not implemented in one number math node.")

        if check_type(output_dict["Output"], PortValueType.NUMBER):
            output_dict["__message__Information"] = "Output: "+str(output_dict["Output"])
        elif check_type(output_dict["Output"], PortValueType.NP_ARRAY):
            output_dict["__message__Information"] = "Output shape: "+str(output_dict["Output"].shape)
        elif check_type(output_dict["Output"], PortValueType.PD_DATAFRAME):
            output_dict["__message__Information"] = "Columns : "+str(len(output_dict["Output"].columns))+", lines : "+str(len(output_dict["Output"]))

        return output_dict
        







class TrigonometryNode(GenericNode):
    # unique node identifier.
    __identifier__ = 'Math'
    # initial default node name.
    NODE_NAME = 'Trigonometry'

    def __init__(self):
        super(TrigonometryNode, self).__init__()

        # create input & output ports
        self.add_custom_input('Input', PortValueType.MATH_COMPATIBLE)
        self.add_custom_output('Output', PortValueType.MATH_COMPATIBLE)

        self.add_combo_menu('Operation', 'Operation', ["Sin", "Cos", "Tan", "Asin", "Acos", "Atan", "Atan2"])
                               
        self.add_label("Information")
        
        self.is_iterated_compatible = True
        
    
    def check_function(self, input_dict, first = False):
        if (not "Input" in input_dict) or (type(input_dict["Input"]) == str):
            return False, "Input not valid", "Information"
        
        if self.get_property("Operation") in ["Asin", "Acos"] and check_type(input_dict["Input"], PortValueType.NUMBER) and (input_dict["Input"] < 1. or input_dict["Input"] > 1.):
            return False, "Input should be between -1. and 1..", "Information"
        
        if self.get_property("Operation") == "Tan" and check_type(input_dict["Input"], PortValueType.NUMBER) and ((input_dict["Input"] + math.pi/2)%math.pi == 0.):
            return False, "tan(Input) impossible.", "Information"
        
        return True, "", "Information"

    def update_function(self, input_dict, first = False):
        output_dict = {}


        operation = self.get_property("Operation")
        if operation == "Sin":
            output_dict["Output"] = apply_function(input_dict["Input"], np.sin)
        elif operation == "Cos":
            output_dict["Output"] = apply_function(input_dict["Input"], np.cos)
        elif operation == "Tan":
            output_dict["Output"] = apply_function(input_dict["Input"], np.tan)
        elif operation == "Asin":
            output_dict["Output"] = apply_function(input_dict["Input"], np.arcsin)
        elif operation == "Acos":
            output_dict["Output"] = apply_function(input_dict["Input"], np.arccos)
        elif operation == "Atan":
            output_dict["Output"] = apply_function(input_dict["Input"], np.arctan)
        elif operation == "Atan2":
            output_dict["Output"] = apply_function(input_dict["Input"], np.arctan2)
        else:
            raise NotImplementedError("Operation "+operation+" not implemented in trigonometry math node.")

        output_dict["__message__Information"] = "Output: "+str(output_dict["Output"])

        return output_dict
        













class TwoMathNode(GenericNode):
    # unique node identifier.
    __identifier__ = 'Math'
    # initial default node name.
    NODE_NAME = 'Two elements (element wise)'

    def __init__(self):
        super(TwoMathNode, self).__init__()

        # create input & output ports
        self.add_custom_input('Input 1', PortValueType.MATH_COMPATIBLE)
        self.add_custom_input('Input 2', PortValueType.MATH_COMPATIBLE)
        self.add_custom_output('Output', PortValueType.MATH_COMPATIBLE)

        self.add_combo_menu('Operation', 'Operation', ["Add", "Subtract", "Multiply", "Divide", "Power", "Modulo", "Round"])
                               
        self.add_label("Information")
        
        self.is_iterated_compatible = True
        
    
    def check_function(self, input_dict, first = False):
        if (not "Input 1" in input_dict) or (type(input_dict["Input 1"]) == str):
            return False, "Input 1 not valid", "Information"
        
        if (not "Input 2" in input_dict) or (type(input_dict["Input 2"]) == str):
            return False, "Input 2 not valid", "Information"
        
        if not are_comparable(input_dict["Input 1"], input_dict["Input 2"], PortValueType.MATH_COMPATIBLE):
            return False, "Inputs are not compatible.", "Information"

        if check_type(input_dict["Input 1"], PortValueType.NUMBER) and \
            check_type(input_dict["Input 2"], PortValueType.NUMBER):
        
            if self.get_property("Operation") == "Power" and (input_dict["Input 1"] == 0. and input_dict["Input 2"] == 0.\
                                                                or input_dict["Input 1"] < 0. and int(input_dict["Input 2"]) != input_dict["Input 2"]):
                return False, "Input 1 and 2 are not compatible.", "Information"

            if self.get_property("Operation") in ["Modulo", "Round"] and not check_type(input_dict["Input 2"], PortValueType.INTEGER):
                return False, "Input 2 is not an integer.", "Information"

            if self.get_property("Operation") == "Divide" and input_dict["Input 2"] == 0.:
                return False, "Cannot divide by 0.", "Information"

            if self.get_property("Operation") == "Modulo" and input_dict["Input 2"] == 0.:
                return False, "Cannot divide by 0.", "Information"

            if self.get_property("Operation") == "Round" and (int(input_dict["Input 2"]) != input_dict["Input 2"]):
                return False, "Input 2 invalid.", "Information"
        
        ###     Si on a un nombre seulement
        elif not (check_type(input_dict["Input 1"], PortValueType.PLOTTABLE) and check_type(input_dict["Input 2"], PortValueType.PLOTTABLE)):
            if self.get_property("Operation") in ["Modulo", "Round", "Power"] and not check_type(input_dict["Input 2"], PortValueType.NUMBER):
                return False, "Inputs type couple incompatible.", "Information"

        ###     Si deux objets, alors are comparable a fait le travail.
        
        return True, "", "Information"
        

    def update_function(self, input_dict, first = False):
        output_dict = {}

        operation = self.get_property("Operation")
        
        if check_type(input_dict["Input 1"], PortValueType.NUMBER) and \
            check_type(input_dict["Input 2"], PortValueType.NUMBER):
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

        else:
            if (check_type(input_dict["Input 1"], PortValueType.PLOTTABLE) and check_type(input_dict["Input 2"], PortValueType.PLOTTABLE)):
                input_1 = input_dict["Input 1"]
                input_2 = input_dict["Input 2"]
            elif check_type(input_dict["Input 1"], PortValueType.PLOTTABLE):
                input_1 = input_dict["Input 1"]
                input_2 = object_clone(input_dict["Input 2"], input_1)
            else:
                input_2 = input_dict["Input 2"]
                input_1 = object_clone(input_dict["Input 1"], input_2)

                
            if operation == "Add":
                output_dict["Output"] = input_1 + input_2
            elif operation == "Subtract":
                output_dict["Output"] = input_1 - input_2

            elif operation == "Multiply":
                output_dict["Output"] = input_1 * input_2
            elif operation == "Divide":
                output_dict["Output"] = input_1 / input_2

            elif operation == "Power":
                output_dict["Output"] = apply_twin_function(input_1, input_2, np.power)
            elif operation == "Modulo":
                output_dict["Output"] = apply_twin_function(input_1, input_2, np.mod)
            elif operation == "Round":
                output_dict["Output"] = apply_twin_function(input_1, input_2, np.round)
            else:
                raise NotImplementedError("Operation "+operation+" not implemented for two matrixes.")

        if check_type(output_dict["Output"], PortValueType.NUMBER):
            output_dict["__message__Information"] = "Output: "+str(output_dict["Output"])
        elif check_type(output_dict["Output"], PortValueType.NP_ARRAY):
            output_dict["__message__Information"] = "Output array shape: "+str(output_dict["Output"].shape)
        elif check_type(output_dict["Output"], PortValueType.LIST):
            output_dict["__message__Information"] = "Output list length: "+str(len(output_dict["Output"]))
        elif check_type(output_dict["Output"], PortValueType.PD_DATAFRAME):
            output_dict["__message__Information"] = "Output dataframe shape: "+str(len(output_dict["Output"].columns))+" columns, "+str(len(output_dict["Output"]))+" lines"

        return output_dict
        