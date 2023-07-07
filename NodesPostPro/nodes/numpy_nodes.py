from NodesPostPro.nodes.generic_node import GenericNode, PortValueType
from NodesPostPro.nodes.custom_widgets import IntSelector_Widget

import numpy as np




class SetAxisNode(GenericNode):
    """
    An example of a node with a embedded QLineEdit.
    """

    # unique node identifier.
    __identifier__ = 'Numpy'

    # initial default node name.
    NODE_NAME = 'Set axis'

    def __init__(self):
        super(SetAxisNode, self).__init__()

        #   Create input port for input array
        self.add_custom_input('Input Array', PortValueType.NP_ARRAY)

        #   Create output ports for :
        #       The output array corresponding to the given axis value
        self.add_custom_output('Output Array', PortValueType.NP_ARRAY)

        #   Create the QComboBox menu to select the desired column.

        self.axis_widget = self.add_int_selector("Axis", 'Axis to set')
        self.value_widget = self.add_int_selector("Value",'Axis value')

        self.add_label("Information")

        self.is_iterated_compatible = True


    def check_function(self, input_dict, first=False):
        if (not "Input Array" in input_dict) or (type(input_dict["Input Array"]) == str):
            return False, "Input Array is not valid", "Information"
        return True, "", "Information"

    def update_function(self, input_dict, first=False):
        if first:
            if self.axis_widget.get_range()[-1] != len(input_dict["Input Array"].shape) - 1:
                self.axis_widget.set_range(0, len(input_dict["Input Array"].shape) - 1)

            if self.value_widget.get_range()[-1] != input_dict["Input Array"].shape[self.axis_widget.get_value()] - 1:
                self.value_widget.set_range(0, input_dict["Input Array"].shape[self.axis_widget.get_value()] - 1)

        output_dict = {'Output Array': np.take(input_dict["Input Array"], self.value_widget.get_value(), self.axis_widget.get_value())}
        output_dict["__message__Information"] = "Output shape : "+str(output_dict["Output Array"].shape)
        return output_dict


    def reset_outputs(self):
        super(SetAxisNode, self).reset_outputs()

        self.axis_widget.set_range(0, 0)
        self.value_widget.set_range(0, 0)








        
class NP_AddNode(GenericNode):
    """
    An example of a node with a embedded QLineEdit.
    """

    # unique node identifier.
    __identifier__ = 'Numpy'

    # initial default node name.
    NODE_NAME = 'Add'

    def __init__(self):
        super(NP_AddNode, self).__init__()

        #   Create input port for input array
        self.add_custom_input('Input Array 1', PortValueType.NP_ARRAY)
        self.add_custom_input('Input Array 2', PortValueType.NP_ARRAY)

        #   Create output ports for :
        #       The output array corresponding to the given axis value
        self.add_custom_output('Output Array', PortValueType.NP_ARRAY)

        self.add_label("Information")

        self.is_iterated_compatible = True



    def check_function(self, input_dict, first=False):
        if (not "Input Array 1" in input_dict) or (type(input_dict["Input Array 1"]) == str):
            return False, "Input Array 1 is not valid", "Information"
        
        if (not "Input Array 2" in input_dict) or (type(input_dict["Input Array 2"]) == str):
            return False, "Input Array 2 is not valid", "Information"
        
        if input_dict["Input Array 1"].shape != input_dict["Input Array 2"].shape:
            return False, "Input arrays shapes are different.", "Information"

        
        return True, "", "Information"


    def update_function(self, input_dict, first=False):
        output_dict = {'Output Array': input_dict["Input Array 1"] + input_dict["Input Array 2"]}
        
        output_dict["__message__Information"] = "Output shape : "+str(output_dict["Output Array"].shape)

        return output_dict



        
class NP_MultiplyFloatNode(GenericNode):
    """
    An example of a node with a embedded QLineEdit.
    """

    # unique node identifier.
    __identifier__ = 'Numpy'

    # initial default node name.
    NODE_NAME = 'Multiply float'

    def __init__(self):
        super(NP_MultiplyFloatNode, self).__init__()

        #   Create input port for input array
        self.add_custom_input('Input Array', PortValueType.NP_ARRAY)
        self.add_twin_input('Input float', PortValueType.FLOAT)

        #   Create output ports for :
        #       The output array corresponding to the given axis value
        self.add_custom_output('Output Array', PortValueType.NP_ARRAY)

        self.add_label("Information")

        self.is_iterated_compatible = True


    def check_function(self, input_dict, first=False):
        if (not "Input Array" in input_dict) or (type(input_dict["Input Array"]) == str):
            return False, "Input Array is not valid", "Information"
        
        if not "Input float" in input_dict:
            return False, "Input float is not valid", "Information"
        
        return True, "", "Information"


    def update_function(self, input_dict, first=False):
        output_dict = {'Output Array': input_dict["Input Array"] * input_dict["Input float"]}
        
        output_dict["__message__Information"] = "Output shape : "+str(output_dict["Output Array"].shape)

        return output_dict






class NP_SqueezeNode(GenericNode):
    """
    An example of a node with a embedded QLineEdit.
    """

    # unique node identifier.
    __identifier__ = 'Numpy'

    # initial default node name.
    NODE_NAME = 'Squeeze'

    def __init__(self):
        super(NP_SqueezeNode, self).__init__()

        #   Create input port for input array
        self.add_custom_input('Input Array', PortValueType.NP_ARRAY)

        #   Create output ports for :
        #       The output array corresponding to the given axis value
        self.add_custom_output('Output Array', PortValueType.NP_ARRAY)

        self.add_label("Information")

        self.is_iterated_compatible = True


    def check_function(self, input_dict, first=False):
        if (not "Input Array" in input_dict) or (type(input_dict["Input Array"]) == str):
            return False, "Input Array is not valid", "Information"
        return True, "", "Information"
        

    def update_function(self, input_dict, first=False):
        output_dict = {'Output Array': np.squeeze(input_dict["Input Array"])} 
        output_dict["__message__Information"] = "Output shape : "+str(output_dict["Output Array"].shape)
        return output_dict
    
        
class NP_FlattenNode(GenericNode):
    """
    An example of a node with a embedded QLineEdit.
    """

    # unique node identifier.
    __identifier__ = 'Numpy'

    # initial default node name.
    NODE_NAME = 'Flatten'

    def __init__(self):
        super(NP_FlattenNode, self).__init__()

        #   Create input port for input array
        self.add_custom_input('Input Array', PortValueType.NP_ARRAY)

        #   Create output ports for :
        #       The output array corresponding to the given axis value
        self.add_custom_output('Output Array', PortValueType.NP_ARRAY)

        self.is_iterated_compatible = True

        self.add_label("Information")



    def check_function(self, input_dict, first=False):
        if (not "Input Array" in input_dict) or (type(input_dict["Input Array"]) == str):
            return False, "Input Array is not valid", "Information"
        return True, "", "Information"
        
        
    def update_function(self, input_dict, first=False):
        output_dict = {'Output Array': input_dict["Input Array"].flatten()} 
        output_dict["__message__Information"] = "Output shape : "+str(output_dict["Output Array"].shape)
        return output_dict