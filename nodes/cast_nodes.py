from NodeGraphQt import BaseNode
from nodes.generic_node import GenericNode, PortValueType

import numpy as np
import pandas as pd

def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False
    




class GenericCastNode(GenericNode):
    # unique node identifier.
    __identifier__ = 'Cast Variables'

    # initial default node name.
    # NODE_NAME = 'node Multiply'

    def __init__(self):
        super(GenericCastNode, self).__init__()

        self.is_iterated_compatible = True

    def check_function(self, input_dict):
        
        is_valid, message = self.is_input_valid("Input")

        return is_valid, message, "Information"











class FloatToIntegerCastNode(GenericCastNode):
    # initial default node name.
    NODE_NAME = 'Float to Integer'

    def __init__(self):
        super(FloatToIntegerCastNode, self).__init__()

        # create input & output ports
        self.add_custom_input('Input', PortValueType.FLOAT)
        self.add_custom_output('Output', PortValueType.INTEGER)
                               
        self.add_label("Information")
        
    def update_function(self, input_dict):
        output_dict = {}
        output_dict["Output"] = int(input_dict["Input"])
        

        output_dict["__message__Information"] = str(output_dict["Output"])

        return output_dict
        
class FloatToStringCastNode(GenericCastNode):
    # initial default node name.
    NODE_NAME = 'Float to String'

    def __init__(self):
        super(FloatToStringCastNode, self).__init__()

        # create input & output ports
        self.add_custom_input('Input', PortValueType.FLOAT)
        self.add_custom_output('Output', PortValueType.STRING)
                               
        self.add_label("Information")
        
    def update_function(self, input_dict):
        output_dict = {}
        output_dict["Output"] = str(input_dict["Input"])
        

        output_dict["__message__Information"] = str(output_dict["Output"])

        return output_dict
        
class FloatToBooleanCastNode(GenericCastNode):
    # initial default node name.
    NODE_NAME = 'Float to Boolean'

    def __init__(self):
        super(FloatToBooleanCastNode, self).__init__()

        # create input & output ports
        self.add_custom_input('Input', PortValueType.FLOAT)
        self.add_custom_output('Output', PortValueType.BOOL)
        
        self.add_label("Information")
        
    def update_function(self, input_dict):
        output_dict = {}
        output_dict["Output"] = bool(input_dict["Input"])
        

        output_dict["__message__Information"] = str(output_dict["Output"])

        return output_dict

        


    def check_function(self, input_dict):
        is_valid, message, label_name = super(FloatToBooleanCastNode, self).check_function(input_dict)

        if is_valid:
            if not str(input_dict["Input"]) in ['yes', 'true', '1', "1.", 'no', 'false', '0', '0.']:
                is_valid = False
                message = "Input is not a boolean."

        return is_valid, message, label_name














class IntegerToFloatCastNode(GenericCastNode):
    # initial default node name.
    NODE_NAME = 'Integer to Float'

    def __init__(self):
        super(IntegerToFloatCastNode, self).__init__()

        # create input & output ports
        self.add_custom_input('Input', PortValueType.INTEGER)
        self.add_custom_output('Output', PortValueType.FLOAT)
                               
        self.add_label("Information")

        self.is_iterated_compatible = True
        
    def update_function(self, input_dict):
        output_dict = {}
        
        output_dict["Output"] = float(input_dict["Input"])

        output_dict["__message__Information"] = str(output_dict["Output"])

        return output_dict

        
class IntegerToStringCastNode(GenericCastNode):
    # initial default node name.
    NODE_NAME = 'Integer to String'

    def __init__(self):
        super(IntegerToStringCastNode, self).__init__()

        # create input & output ports
        self.add_custom_input('Input', PortValueType.INTEGER)
        self.add_custom_output('Output', PortValueType.STRING)
                               
        self.add_label("Information")
        
    def update_function(self, input_dict):
        output_dict = {}
        output_dict["Output"] = str(input_dict["Input"])
        

        output_dict["__message__Information"] = str(output_dict["Output"])

        return output_dict
        
class IntegerToBooleanCastNode(GenericCastNode):
    # initial default node name.
    NODE_NAME = 'Integer to Boolean'

    def __init__(self):
        super(IntegerToBooleanCastNode, self).__init__()

        # create input & output ports
        self.add_custom_input('Input', PortValueType.INTEGER)
        self.add_custom_output('Output', PortValueType.BOOL)
        
        self.add_label("Information")
        
    def update_function(self, input_dict):
        output_dict = {}
        output_dict["Output"] = bool(input_dict["Input"])
        

        output_dict["__message__Information"] = str(output_dict["Output"])

        return output_dict




    
    def check_function(self, input_dict):
        is_valid, message, label_name = super(IntegerToBooleanCastNode, self).check_function(input_dict)

        if is_valid:
            if not str(input_dict["Input"]) in ['yes', 'true', '1', "1.", 'no', 'false', '0', '0.']:
                is_valid = False
                message = "Input is not a boolean."

        return is_valid, message, label_name








class StringToFloatCastNode(GenericCastNode):
    # initial default node name.
    NODE_NAME = 'String to Float'

    def __init__(self):
        super(StringToFloatCastNode, self).__init__()

        # create input & output ports
        self.add_custom_input('Input', PortValueType.STRING)
        self.add_custom_output('Output', PortValueType.FLOAT)
                               
        self.add_label("Information")
        
    
    def check_function(self, input_dict):
        is_valid, message, label_name = super(StringToFloatCastNode, self).check_inputs(input_dict)

        if is_valid:
            if not is_float(input_dict("Input")):
                is_valid = False
                message = "Input is not a float."

        return is_valid, message, label_name
    
    def update_function(self, input_dict):
        output_dict = {}
        output_dict["Output"] = float(input_dict["Input"])
        

        output_dict["__message__Information"] = str(output_dict["Output"])

        return output_dict
        
class StringToIntegerCastNode(GenericCastNode):
    # initial default node name.
    NODE_NAME = 'String to Integer'

    def __init__(self):
        super(StringToIntegerCastNode, self).__init__()

        # create input & output ports
        self.add_custom_input('Input', PortValueType.STRING)
        self.add_custom_output('Output', PortValueType.INTEGER)
                               
        self.add_label("Information")
        
    
    def check_function(self, input_dict):
        is_valid, message, label_name = super(StringToIntegerCastNode, self).check_function(input_dict)

        if is_valid:
            if not input_dict["Input"].lstrip("-").isdigit():
                is_valid = False
                message = "Input is not an integer."

        return is_valid, message, label_name

    def update_function(self, input_dict):
        output_dict = {}
        output_dict["Output"] = int(input_dict["Input"])
        

        output_dict["__message__Information"] = str(output_dict["Output"])

        return output_dict
        
class StringToBooleanCastNode(GenericCastNode):
    # initial default node name.
    NODE_NAME = 'String to Boolean'

    def __init__(self):
        super(StringToBooleanCastNode, self).__init__()

        # create input & output ports
        self.add_custom_input('Input', PortValueType.STRING)
        self.add_custom_output('Output', PortValueType.BOOL)
        
        self.add_label("Information")
        
    
    def check_function(self, input_dict):
        is_valid, message, label_name = super(StringToBooleanCastNode, self).check_function(input_dict)

        if is_valid:
            if not input_dict["Input"] in ['yes', 'true', '1', "1.", 'no', 'false', '0', '0.']:
                is_valid = False
                message = "Input is not a boolean."

        return is_valid, message, label_name

    def update_function(self, input_dict):
        output_dict = {}
        output_dict["Output"] = bool(input_dict["Input"])
        

        output_dict["__message__Information"] = str(output_dict["Output"])

        return output_dict















class BooleanToFloatCastNode(GenericCastNode):
    # initial default node name.
    NODE_NAME = 'Boolean to Float'

    def __init__(self):
        super(BooleanToFloatCastNode, self).__init__()

        # create input & output ports
        self.add_custom_input('Input', PortValueType.BOOL)
        self.add_custom_output('Output', PortValueType.FLOAT)
                               
        self.add_label("Information")
        
    def update_function(self, input_dict):
        output_dict = {}
        output_dict["Output"] = float(input_dict["Input"])

        output_dict["__message__Information"] = str(output_dict["Output"])

        return output_dict
        
class BooleanToStringCastNode(GenericCastNode):
    # initial default node name.
    NODE_NAME = 'Boolean to String'

    def __init__(self):
        super(BooleanToStringCastNode, self).__init__()

        # create input & output ports
        self.add_custom_input('Input', PortValueType.BOOL)
        self.add_custom_output('Output', PortValueType.STRING)
                               
        self.add_label("Information")
        
    def update_function(self, input_dict):
        output_dict = {}
        output_dict["Output"] = str(input_dict["Input"])
        
        output_dict["__message__Information"] = str(output_dict["Output"])

        return output_dict
        
class BooleanToIntegerCastNode(GenericCastNode):
    # initial default node name.
    NODE_NAME = 'Boolean to Integer'

    def __init__(self):
        super(BooleanToIntegerCastNode, self).__init__()

        # create input & output ports
        self.add_custom_input('Input', PortValueType.BOOL)
        self.add_custom_output('Output', PortValueType.INTEGER)
        
        self.add_label("Information")
        
    def update_function(self, input_dict):
        output_dict = {}
        output_dict["Output"] = bool(input_dict["Input"])
        

        output_dict["__message__Information"] = str(output_dict["Output"])

        return output_dict








class DataFrameToArrayCastNode(GenericCastNode):
    # initial default node name.
    NODE_NAME = 'DataFrame to Array'

    def __init__(self):
        super(DataFrameToArrayCastNode, self).__init__()

        # create input & output ports
        self.add_custom_input('Input', PortValueType.PD_DATAFRAME)
        self.add_custom_output('Output', PortValueType.NP_ARRAY)
                               
        self.add_label("Information")
        
    def update_function(self, input_dict):
        output_dict = {}
        output_dict["Output"] = input_dict["Input"].to_numpy()
        

        self.change_label("Information", str(output_dict["Output"].shape), False)

        
        

class ArrayToDataFrameCastNode(GenericCastNode):
    # initial default node name.
    NODE_NAME = 'Array to DataFrame'

    def __init__(self):
        super(ArrayToDataFrameCastNode, self).__init__()

        # create input & output ports
        self.add_custom_input('Input', PortValueType.NP_ARRAY)
        self.add_custom_input('Columns Names', PortValueType.LIST)

        self.add_custom_output('Output', PortValueType.PD_DATAFRAME)
                               
        self.add_label("Information")
        
    
    def check_function(self, input_dict):
        is_valid, message, label_name = super(ArrayToDataFrameCastNode, self).check_function(input_dict)

        if is_valid:

            column_list = input_dict["Columns Names"]

            for element in column_list:
                if type(element) != str:
                    is_valid = False
                    message = "Columns Names input does not contain floats."
            
            if len(column_list) != len(input_dict["Input"].columns):
                is_valid = False
                message = "Inputs dimensions don't match."

        return is_valid, message, label_name

    def update_function(self, input_dict):
        output_dict = {}
        output_dict["Output"] = float(pd.DataFrame(self.get_value_from_port("Input"), columns=input_dict["Columns Names"]))
        

        output_dict["__message__Information"] = "Dataframe size "+str(len(output_dict["Output"]))+" for "+str(len(input_dict["Columns Names"]))+" columns"

        return output_dict
        