from NodeGraphQt import BaseNode
from nodes.generic_node import GenericNode, PortValueType

import numpy as np
import pandas as pd

class GenericCastNode(GenericNode):
    # unique node identifier.
    __identifier__ = 'Cast Variables'

    # initial default node name.
    # NODE_NAME = 'node Multiply'

    def __init__(self):
        super(GenericCastNode, self).__init__()

    def cast_function(self, input):
        raise NotImplementedError
    
    
    def check_inputs(self):
        input_given = self.get_value_from_port("Input")
        
        self.set_property("is_valid", input_given is not None \
                                            and input_given.is_defined() \
                                                and input_given.get_property_type() == self.input_properties["Input"].get_property_type())
    
        if input_given is None or not input_given.is_defined():
            self.change_label("Information", "Input not plugged to valid output.", True)

        elif not input_given.get_property_type() == self.input_properties["Input"].get_property_type():
            self.change_label("Information", "Plugged port is not of the right type.", True)


    def update_from_input(self):
        raise NotImplementedError













class FloatToIntegerCastNode(GenericCastNode):
    # initial default node name.
    NODE_NAME = 'Float to Integer'

    def __init__(self):
        super(FloatToIntegerCastNode, self).__init__()

        # create input & output ports
        self.add_custom_input('Input', PortValueType.FLOAT)
        self.add_custom_output('Output', PortValueType.INTEGER)
                               
        self.add_label("Information")
        
    def update_from_input(self):
        output_value = int(self.get_value_from_port("Input").get_property())
        self.set_output_property('Output', output_value)

        self.change_label("Information", str(output_value), False)
        
class FloatToStringCastNode(GenericCastNode):
    # initial default node name.
    NODE_NAME = 'Float to String'

    def __init__(self):
        super(FloatToStringCastNode, self).__init__()

        # create input & output ports
        self.add_custom_input('Input', PortValueType.FLOAT)
        self.add_custom_output('Output', PortValueType.STRING)
                               
        self.add_label("Information")
        
    def update_from_input(self):
        output_value = str(self.get_value_from_port("Input").get_property())
        self.set_output_property('Output', output_value)

        self.change_label("Information", str(output_value), False)
        
class FloatToBooleanCastNode(GenericCastNode):
    # initial default node name.
    NODE_NAME = 'Float to Boolean'

    def __init__(self):
        super(FloatToBooleanCastNode, self).__init__()

        # create input & output ports
        self.add_custom_input('Input', PortValueType.FLOAT)
        self.add_custom_output('Output', PortValueType.BOOL)
        
        self.add_label("Information")
        
    def update_from_input(self):
        output_value = bool(self.get_value_from_port("Input").get_property())
        self.set_output_property('Output', output_value)

        self.change_label("Information", str(output_value), False)

        













class IntegerToFloatCastNode(GenericCastNode):
    # initial default node name.
    NODE_NAME = 'Integer to Float'

    def __init__(self):
        super(IntegerToFloatCastNode, self).__init__()

        # create input & output ports
        self.add_custom_input('Input', PortValueType.INTEGER)
        self.add_custom_output('Output', PortValueType.FLOAT)
                               
        self.add_label("Information")
        
    def update_from_input(self):
        output_value = float(self.get_value_from_port("Input").get_property())
        self.set_output_property('Output', output_value)

        self.change_label("Information", str(output_value), False)
        
class IntegerToStringCastNode(GenericCastNode):
    # initial default node name.
    NODE_NAME = 'Integer to String'

    def __init__(self):
        super(IntegerToStringCastNode, self).__init__()

        # create input & output ports
        self.add_custom_input('Input', PortValueType.INTEGER)
        self.add_custom_output('Output', PortValueType.STRING)
                               
        self.add_label("Information")
        
    def update_from_input(self):
        output_value = str(self.get_value_from_port("Input").get_property())
        self.set_output_property('Output', output_value)

        self.change_label("Information", str(output_value), False)
        
class IntegerToBooleanCastNode(GenericCastNode):
    # initial default node name.
    NODE_NAME = 'Integer to Boolean'

    def __init__(self):
        super(IntegerToBooleanCastNode, self).__init__()

        # create input & output ports
        self.add_custom_input('Input', PortValueType.INTEGER)
        self.add_custom_output('Output', PortValueType.BOOL)
        
        self.add_label("Information")
        
    def update_from_input(self):
        output_value = bool(self.get_value_from_port("Input").get_property())
        self.set_output_property('Output', output_value)

        self.change_label("Information", str(output_value), False)












class StringToFloatCastNode(GenericCastNode):
    # initial default node name.
    NODE_NAME = 'String to Float'

    def __init__(self):
        super(StringToFloatCastNode, self).__init__()

        # create input & output ports
        self.add_custom_input('Input', PortValueType.STRING)
        self.add_custom_output('Output', PortValueType.FLOAT)
                               
        self.add_label("Information")
        
    
    def check_inputs(self):
        super(StringToFloatCastNode, self).check_inputs()

        if self.get_property("is_valid"):
            self.set_property("is_valid",  self.input_properties["Input"].get_property().lstrip("-").isdigit())
    
    def update_from_input(self):
        output_value = float(self.get_value_from_port("Input").get_property())
        self.set_output_property('Output', output_value)

        self.change_label("Information", str(output_value), False)
        
class StringToIntegerCastNode(GenericCastNode):
    # initial default node name.
    NODE_NAME = 'String to Integer'

    def __init__(self):
        super(StringToIntegerCastNode, self).__init__()

        # create input & output ports
        self.add_custom_input('Input', PortValueType.STRING)
        self.add_custom_output('Output', PortValueType.INTEGER)
                               
        self.add_label("Information")
        
    
    def check_inputs(self):
        super(StringToFloatCastNode, self).check_inputs()

        if self.get_property("is_valid"):
            self.set_property("is_valid",  self.input_properties["Input"].get_property().lstrip("-").isdigit())

    def update_from_input(self):
        output_value = int(self.get_value_from_port("Input").get_property())
        self.set_output_property('Output', output_value)

        self.change_label("Information", str(output_value), False)
        
class StringToBooleanCastNode(GenericCastNode):
    # initial default node name.
    NODE_NAME = 'String to Boolean'

    def __init__(self):
        super(StringToBooleanCastNode, self).__init__()

        # create input & output ports
        self.add_custom_input('Input', PortValueType.STRING)
        self.add_custom_output('Output', PortValueType.BOOL)
        
        self.add_label("Information")
        
    
    def check_inputs(self):
        super(StringToFloatCastNode, self).check_inputs()

        if self.get_property("is_valid"):
            self.set_property("is_valid",  self.input_properties["Input"].get_property() in ['yes', 'true', '1', "1.", 'no', 'false', '0', '0.'])

    def update_from_input(self):
        output_value = bool(self.get_value_from_port("Input").get_property())
        self.set_output_property('Output', output_value)

        self.change_label("Information", str(output_value), False)















class BooleanToFloatCastNode(GenericCastNode):
    # initial default node name.
    NODE_NAME = 'Boolean to Float'

    def __init__(self):
        super(BooleanToFloatCastNode, self).__init__()

        # create input & output ports
        self.add_custom_input('Input', PortValueType.BOOL)
        self.add_custom_output('Output', PortValueType.FLOAT)
                               
        self.add_label("Information")
        
    def update_from_input(self):
        output_value = float(self.get_value_from_port("Input").get_property())
        self.set_output_property('Output', output_value)

        self.change_label("Information", str(output_value), False)
        
class BooleanToStringCastNode(GenericCastNode):
    # initial default node name.
    NODE_NAME = 'Boolean to String'

    def __init__(self):
        super(BooleanToStringCastNode, self).__init__()

        # create input & output ports
        self.add_custom_input('Input', PortValueType.BOOL)
        self.add_custom_output('Output', PortValueType.STRING)
                               
        self.add_label("Information")
        
    def update_from_input(self):
        output_value = str(self.get_value_from_port("Input").get_property())
        self.set_output_property('Output', output_value)

        self.change_label("Information", str(output_value), False)
        
class BooleanToIntegerCastNode(GenericCastNode):
    # initial default node name.
    NODE_NAME = 'Boolean to Integer'

    def __init__(self):
        super(BooleanToIntegerCastNode, self).__init__()

        # create input & output ports
        self.add_custom_input('Input', PortValueType.BOOL)
        self.add_custom_output('Output', PortValueType.INTEGER)
        
        self.add_label("Information")
        
    def update_from_input(self):
        output_value = bool(self.get_value_from_port("Input").get_property())
        self.set_output_property('Output', output_value)

        self.change_label("Information", str(output_value), False)








class DataFrameToArrayCastNode(GenericCastNode):
    # initial default node name.
    NODE_NAME = 'DataFrame to Array'

    def __init__(self):
        super(DataFrameToArrayCastNode, self).__init__()

        # create input & output ports
        self.add_custom_input('Input', PortValueType.PD_DATAFRAME)
        self.add_custom_output('Output', PortValueType.NP_ARRAY)
                               
        self.add_label("Information")
        
    def update_from_input(self):
        output_value = self.get_value_from_port("Input").get_property().to_numpy()
        self.set_output_property('Output', output_value)

        self.change_label("Information", str(output_value), False)
        
        

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
        
    
    def check_inputs(self):
        super(StringToFloatCastNode, self).check_inputs()

        if self.get_property("is_valid"):

            column_list = self.input_properties["Columns Names"].get_property()

            is_valid = True

            for element in column_list:
                if type(element) != str:
                    is_valid = False
            
            if len(column_list) != len(self.input_properties["Input"].get_property().columns):
                is_valid = False


            self.set_property("is_valid",  is_valid)

    def update_from_input(self):
        output_value = float(pd.DataFrame(self.get_value_from_port("Input"), columns=self.input_properties["Columns Names"].get_property()))
        self.set_output_property('Output', output_value)

        self.change_label("Information", str(output_value), False)
        