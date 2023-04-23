from nodes.generic_node import GenericNode, PortValueType
from nodes.custom_widgets import IntSelector_Widget

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

        self.axis_widget = IntSelector_Widget(self.view, name="Axis", label='Axis to set')
        self.value_widget = IntSelector_Widget(self.view, name="Value", label='Axis value')

        self.create_property("Axis", 0)
        self.create_property("Value", 0)

        self.axis_widget.value_changed.connect(lambda k, v: self.set_property(k, v))
        self.value_widget.value_changed.connect(lambda k, v: self.set_property(k, v))

        self.view.add_widget(self.axis_widget)
        self.view.draw_node()
        self.view.add_widget(self.value_widget)
        self.view.draw_node()

        self.add_label("Information")


    def check_inputs(self):
        
        is_valid, message = self.is_input_valid("Input Array")

        self.set_property("is_valid", is_valid)

        if not is_valid:
            self.change_label("Information", message, True)
    
    def update_from_input(self):
        if self.axis_widget.get_range()[-1] != len(self.get_value_from_port("Input Array").get_property().shape) - 1:
            self.axis_widget.set_range(0, len(self.get_value_from_port("Input Array").get_property().shape) - 1)

            
        if self.value_widget.get_range()[-1] != self.get_value_from_port("Input Array").get_property().shape[self.axis_widget.get_value()] - 1:
            self.value_widget.set_range(0, self.get_value_from_port("Input Array").get_property().shape[self.axis_widget.get_value()] - 1)

        self.set_output_property('Output Array', np.take(self.get_value_from_port("Input Array").get_property(), self.value_widget.get_value(), self.axis_widget.get_value()))
        
        self.change_label("Information", "Output shape : "+str(self.get_output_property("Output Array").get_property().shape), False)

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


    def check_inputs(self):
        input_given_1 = self.get_value_from_port("Input Array 1")
        input_given_2 = self.get_value_from_port("Input Array 2")
        
        
        is_valid_1, message_1 = self.is_input_valid("Input Array 1")
        is_valid_2, message_2 = self.is_input_valid("Input Array 2")

        self.set_property("is_valid", is_valid_1 and is_valid_2 and input_given_1.get_property().shape == input_given_2.get_property().shape)

        if not is_valid_1:
            self.change_label("Information", message_1, True)
        elif not is_valid_2:
            self.change_label("Information", message_2, True)
        elif not input_given_1.get_property().shape == input_given_2.get_property().shape:
            self.change_label("Information", "Input arrays shapes are different.", True)

    
    def update_from_input(self):
        self.set_output_property('Output Array', self.get_value_from_port("Input Array 1").get_property() + self.get_value_from_port("Input Array 1").get_property())
        
        self.change_label("Information", "Output shape : "+str(self.get_output_property("Output Array").get_property().shape), False)


        
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
        self.add_custom_input('Input float', PortValueType.FLOAT)

        #   Create output ports for :
        #       The output array corresponding to the given axis value
        self.add_custom_output('Output Array', PortValueType.NP_ARRAY)

        self.add_label("Information")


    def check_inputs(self):        
        is_valid_1, message_1 = self.is_input_valid("Input Array")
        is_valid_2, message_2 = self.is_input_valid("Input float")

        self.set_property("is_valid", is_valid_1 and is_valid_2)

        if not is_valid_1:
            self.change_label("Information", message_1, True)
        elif not is_valid_2:
            self.change_label("Information", message_2, True)


    def update_from_input(self):
        self.set_output_property('Output Array', self.get_value_from_port("Input Array").get_property() * float(self.get_value_from_port("Input float").get_property()))
        
        self.change_label("Information", "Output shape : "+str(self.get_output_property("Output Array").get_property().shape), False)
        








class NP_Squeeze(GenericNode):
    """
    An example of a node with a embedded QLineEdit.
    """

    # unique node identifier.
    __identifier__ = 'Numpy'

    # initial default node name.
    NODE_NAME = 'Squeeze'

    def __init__(self):
        super(NP_Squeeze, self).__init__()

        #   Create input port for input array
        self.add_custom_input('Input Array', PortValueType.NP_ARRAY)

        #   Create output ports for :
        #       The output array corresponding to the given axis value
        self.add_custom_output('Output Array', PortValueType.NP_ARRAY)

        self.add_label("Information")


    def check_inputs(self):        
        is_valid_1, message_1 = self.is_input_valid("Input Array")

        self.set_property("is_valid", is_valid_1)

        if not is_valid_1:
            self.change_label("Information", message_1, True)


    def update_from_input(self):
        self.set_output_property('Output Array', np.squeeze(self.get_value_from_port("Input Array").get_property()))
        
        self.change_label("Information", "Output shape : "+str(self.get_output_property("Output Array").get_property().shape), False)