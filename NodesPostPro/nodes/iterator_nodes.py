from NodeGraphQt import BaseNode
from NodesPostPro.nodes.generic_node import GenericNode, PortValueType
from NodesPostPro.nodes.custom_widgets import ButtonNodeWidget

import numpy as np
import pandas as pd




class ExternalNode(GenericNode):
    # unique node identifier.
    __identifier__ = 'Iterator'

    # initial default node name.
    NODE_NAME = 'External'


    def __init__(self):
        super(ExternalNode, self).__init__()

        self.add_text_input("Min", "Min", "0")
        self.add_text_input("Max", "Max", "5")
        self.add_text_input("Step", "Step", "1")

        self.add_custom_output('i', PortValueType.INTEGER)

        self.button = self.add_button_widget(name="Execute")
        self.button.set_link(self.clicked_function)

        self.add_label("Information")
        self.change_label("Information", "No information", False)


    def check_inputs(self):
        
        if not self.get_property("Min").isdigit():
            self.set_property("is_valid", False)
            self.change_label("Information", "Given minimum should be an integer.", True)
        
        elif not self.get_property("Max").isdigit():
            self.set_property("is_valid", False)
            self.change_label("Information", "Given maximum should be an integer.", True)
        
        elif not self.get_property("Step").isdigit():
            self.set_property("is_valid", False)
            self.change_label("Information", "Given step should be an integer.", True)

        elif int(self.get_property("Min")) > int(self.get_property("Max")):
            self.set_property("is_valid", False)
            self.change_label("Information", "Min should be lower than max.", True)

        else:
            self.set_property("is_valid", True)
    
    def update_from_input(self):
        self.set_output_property('i', int(self.get_property("Min")), False)
        
        self.change_label("Information", "Values count: "+str(len(list(range(int(self.get_property("Min")), int(self.get_property("Max")), int(self.get_property("Step")))))), False)

    def clicked_function(self):
        for i in range(int(self.get_property("Min")), int(self.get_property("Max")), int(self.get_property("Step"))):
            self.set_output_property('i', i)
            self.propagate()

        self.set_output_property('i', int(self.get_property("Min")), False)



        


class InternalNode(GenericNode):
    # unique node identifier.
    __identifier__ = 'Iterator'

    # initial default node name.
    NODE_NAME = 'Internal'


    def __init__(self):
        super(InternalNode, self).__init__()

        self.add_text_input("Min", "Min", "0")
        self.add_text_input("Max", "Max", "5")
        self.add_text_input("Step", "Step", "1")

        self.add_custom_output('i', PortValueType.INTEGER)

        self.add_label("Information")
        self.change_label("Information", "No information", False)

        self.update_values()

    def check_inputs(self):
        if not self.get_property("Min").isdigit():
            self.set_property("is_valid", False)
            self.change_label("Information", "Given minimum should be an integer.", True)
        
        elif not self.get_property("Max").isdigit():
            self.set_property("is_valid", False)
            self.change_label("Information", "Given maximum should be an integer.", True)
        
        elif not self.get_property("Step").isdigit():
            self.set_property("is_valid", False)
            self.change_label("Information", "Given step should be an integer.", True)

        elif int(self.get_property("Min")) > int(self.get_property("Max")):
            self.set_property("is_valid", False)
            self.change_label("Information", "Min should be lower than max.", True)

        else:
            self.set_property("is_valid", True)
    
    def update_from_input(self):
        self.set_output_property('i', list(range(int(self.get_property("Min")), int(self.get_property("Max")), int(self.get_property("Step")))), True)
        
        self.change_label("Information", "Values count: "+str(len(list(range(int(self.get_property("Min")), int(self.get_property("Max")), int(self.get_property("Step")))))), False)
        

        
class InteratorListNode(GenericNode):
    # unique node identifier.
    __identifier__ = 'Iterator'

    # initial default node name.
    NODE_NAME = 'Iterated to list'


    def __init__(self):
        super(InteratorListNode, self).__init__()
        self.add_custom_input("Input", PortValueType.ANY)

        self.add_custom_output('Output', PortValueType.LIST)

        self.add_label("Information")
        self.change_label("Information", "No information", False)

        self.update_values()
        self.is_iterated_compatible = True

    def check_inputs(self):
        
        value = self.get_value_from_port("Input")

        if value is not None:
            is_iterated = value.is_iterated()

            if is_iterated:
                if value.is_defined():
                    self.set_property("is_valid", True)
                    self.change_label("Information", "", True)

                else:
                    self.set_property("is_valid", False)
                    self.change_label("Information", "Plugged input is not defined.", True)

            else:
                self.set_property("is_valid", False)
                self.change_label("Information", "Plugged input is not iterated.", True)

        else:
            self.set_property("is_valid", False)
            self.change_label("Information", "Plugged input is not defined.", True)
            return

    
    def update_from_input(self):
        self.set_output_property('Output', self.get_value_from_port("Input").get_iterated_property(), False)
        
        if len(self.get_output_property("Output").get_property()) == 0:
            self.change_label("Information", "List length: "+str(len(self.get_output_property("Output").get_property())), False)
        else:
            self.change_label("Information", "List length: "+str(len(self.get_output_property("Output").get_property()))+"\nType: "+str(self.get_output_property("Output").get_property()[0].__class__.__name__), False)
        