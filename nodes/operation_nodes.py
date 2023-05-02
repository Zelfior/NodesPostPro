from NodeGraphQt import BaseNode
from nodes.generic_node import GenericNode, PortValueType


class MultiplyNode(GenericNode):
    """
    A node class with 2 inputs and 2 outputs.
    """

    # unique node identifier.
    __identifier__ = 'nodes.multiply'

    # initial default node name.
    NODE_NAME = 'node Multiply'

    def __init__(self):
        super(MultiplyNode, self).__init__()

        # create input & output ports
        self.add_custom_input('Input Array', PortValueType.PD_DATAFRAME)
        self.add_custom_input('Input float', PortValueType.FLOAT)
        self.add_custom_output('Output Array', PortValueType.PD_DATAFRAME)
        
        # create the QComboBox menu.
        self.add_text_input('Value', 'Multiply by', '1', tab='widgets')

        

    def check_inputs(self):
        input_given = self.get_value_from_port("Input Array")
        
        self.set_property("is_valid", input_given is not None \
                                            and input_given.is_defined() \
                                                and input_given.get_property_type() == PortValueType.PD_DATAFRAME
                                                and ((self.get_value_from_port('Input float') is not None and self.get_value_from_port('Input float').is_defined())
                                                or self.get_property("Value").lstrip("-").isdigit()))
    


    def update_from_input(self):
        if self.get_value_from_port('Input float') is not None and self.get_value_from_port('Input float').is_defined():
            value_to_multiply_by = self.get_value_from_port('Input float').get_property()
            #self.view.widgets['Value'].setEditable()
        elif self.get_property("Value").lstrip("-").isdigit():
            value_to_multiply_by = float(self.get_property("Value"))


        self.set_output_property('Output Array', self.get_value_from_port("Input Array").get_property() * value_to_multiply_by)

        #self.view.widget['Value'].clear()


class GetAverageNode(GenericNode):
    """
    A node class with 2 inputs and 2 outputs.
    """

    # unique node identifier.
    __identifier__ = 'nodes.multiply'

    # initial default node name.
    NODE_NAME = 'node average'

    def __init__(self):
        super(GetAverageNode, self).__init__()

        # create input & output ports
        self.add_custom_input('Input Array', PortValueType.PD_DATAFRAME)
        self.add_custom_output('Output Float', PortValueType.FLOAT)
        

    def check_inputs(self):
        input_given = self.get_value_from_port("Input Array")
        
        self.set_property("is_valid", input_given is not None \
                                            and input_given.is_defined() \
                                                and input_given.get_property_type() == PortValueType.PD_DATAFRAME)
    

    def update_from_input(self):
        self.set_output_property('Output Float', float(self.get_value_from_port("Input Array").get_property().mean()))

        #self.view.widget['Value'].clear()