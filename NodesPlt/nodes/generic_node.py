from NodeGraphQt import BaseNode
from enum import Enum
import pandas as pd
import numpy as np
from nodes.custom_widgets import InformationLabelWidget
import matplotlib.pyplot as plt

"""
    All value type that can be exchanged between nodes
"""
class PortValueType(Enum):
    FLOAT = 1
    INTEGER = 2
    STRING = 3
    BOOL = 4
    LIST = 5
    NP_ARRAY = 6
    PD_DATAFRAME = 7
    PLOTTABLE = 8
    DICT = 9
    FIGURE = 9

"""
    Color association with the port type enum
"""
def get_color_from_enum(enum_value):
    if enum_value == PortValueType.FLOAT:
        return (255, 0, 0)
    elif enum_value == PortValueType.INTEGER:
        return (0, 255, 0)
    elif enum_value == PortValueType.STRING:
        return (0, 0, 255)
    elif enum_value == PortValueType.LIST:
        return (100, 0, 255)
    elif enum_value == PortValueType.NP_ARRAY:
        return (0, 100, 255)
    elif enum_value == PortValueType.PD_DATAFRAME:
        return (100, 100, 255)
    elif enum_value == PortValueType.BOOL:
        return (255, 255, 255)
    elif enum_value == PortValueType.PLOTTABLE:
        return (255, 50, 50)
    elif enum_value == PortValueType.DICT:
        return (150, 150, 50)
    elif enum_value == PortValueType.FIGURE:
        return (0, 0, 0)
    
    
"""
    Checks if the given value type corresponds to the enum.
"""
def check_type(value, enum_value):
    if enum_value == PortValueType.FLOAT:
        return type(value) == float
    elif enum_value == PortValueType.INTEGER:
        return type(value) == int
    elif enum_value == PortValueType.STRING:
        return type(value) == str
    elif enum_value == PortValueType.LIST:
        return type(value) == list
    elif enum_value == PortValueType.NP_ARRAY:
        return type(value) == np.ndarray
    elif enum_value == PortValueType.PD_DATAFRAME:
        return type(value) == pd.DataFrame
    elif enum_value == PortValueType.BOOL:
        return type(value) == bool
    elif enum_value == PortValueType.PLOTTABLE:
        return type(value) in [list, np.ndarray, pd.DataFrame]
    elif enum_value == PortValueType.DICT:
        return type(value) == dict
    elif enum_value == PortValueType.FIGURE:
        return type(value) in [plt.Figure, plt.axis]
    else:
        raise ValueError
    

class Container():
    """
        The countainer is initialized empty and undefined
    """
    def __init__(self, enum_value:PortValueType):
        self.countained_value = None
        self.enum_value = enum_value
        self.defined = False
        self.name = ""

    """
        Sets the contained value as none, and sets as not defined
    """
    def reset(self):
        self.countained_value = None
        self.defined = False
        self.name = ""

    """
        If the given value type correspond to the container enum, the value is updated and is set as defined
    """
    def set_property(self, value):
        if check_type(value, self.enum_value):
            self.countained_value = value
            self.defined = True
        else:
            raise TypeError

    """
        Returns the contained value
    """
    def get_property(self):
        return self.countained_value

    """
        Returns if the container is defined
    """
    def is_defined(self):
        return self.defined

    """
        Returns the container type enum
    """
    def get_property_type(self):
        return self.enum_value



"""
    Generic node class that embed the value transmission functions
"""
class GenericNode(BaseNode):
    def __init__(self):
        super(GenericNode, self).__init__()

        self.output_type_list = {"is_valid": PortValueType.BOOL}

        self.create_property("is_valid", False)

        self.is_reseting = False

        self.output_properties = {}
        self.input_properties = {}
        self.label_list = {}


    def is_input_valid(self, input_name):
        value = self.get_value_from_port(input_name)

        is_valid = value is not None \
                        and value.is_defined() \
                            and check_type(value.get_property(), self.input_properties[input_name].get_property_type())

        message = ""

        if value is None:
            message = input_name+" is not defined."

        elif not value.is_defined():
            message = input_name+" is not defined."

        elif not check_type(value.get_property(), self.input_properties[input_name].get_property_type()):
            message = input_name+" is not of the right type."

        return is_valid, message     

    def add_label(self, label_name, label = False):
        if label_name in self.label_list:
            raise ValueError("Label name already exists")
        else:
            self.label_list[label_name] = InformationLabelWidget(self.view, name = label_name, label=label)
            # self.add_custom_widget(self.label_list[label_name])
            self.view.add_widget(self.label_list[label_name])
            self.view.draw_node()

            self.create_property(label_name, "")


    def change_label(self, label_name, label_value, error):
        if label_name in self.label_list:
            self.set_property(label_name, label_value)
            if error:
                self.label_list[label_name].set_text(label_value, 'red')
            else:
                self.label_list[label_name].set_text(label_value, 'white')

        else:
            raise ValueError("Label name doesn't exists")

    """
        BaseNode set_property overload:
            Starts the node output property update process when a property is changed if the property is not "is_valid" and if the node is not resetting (prevents infinite loops)
    """
    def set_property(self, name, value, push_undo=True):
        if name in ["is_valid", "color"] or name in self.label_list:
            super(GenericNode, self).set_property(name, value, push_undo=push_undo)
        elif ( not name in self.output_type_list ) or ( check_type(value, self.output_type_list[name]) ):
            super(GenericNode, self).set_property(name, value, push_undo=push_undo)

            if not self.is_reseting:
                self.update_values()

        
    """
        BaseNode set_property overload:
            Starts the node output property update process when an input port is plugged
    """
    def on_input_connected(self, in_port, out_port):
        super(GenericNode, self).on_input_connected(in_port, out_port)

        self.update_values()


    """
        BaseNode set_property overload:
            Starts the node output property update process when an input port is unplugged
    """
    def on_input_disconnected(self, in_port, out_port):
        super(GenericNode, self).on_input_disconnected(in_port, out_port)

        self.update_values()


    """
        Node output property update process:
            Checks the inputs to know if they match the expectation to compute the outputs. The result is stored in the property "is_valid".

            If True:
                -   call the update_from_input function, that will compute the outputs
            Else:
                -   Resets the node outputs
    """
    def update_values(self):

        self.check_inputs()

        if self.get_property("is_valid"):
            self.is_reseting = True
            self.set_valid_color()
            self.is_reseting = False

            self.update_from_input()
        else:
            self.is_reseting = True
            self.set_invalid_color()
            self.reset_outputs()
            self.is_reseting = False

        self.view.draw_node()
        self.update()
        self.propagate()


    """
        Get the value associated to the port to which the given input port is connected
    """
    def get_value_from_port(self, port_name, multiple = False):
        #   If the given port name is not correct, raises an error.
        if port_name in self.inputs().keys():
            #   If the port is not plugged, returns None
            if len(self.inputs()[port_name].connected_ports()) > 0:
                # Checks if the port to which the port is connected container is defined. If yes, returns its property, returns None otherwise
                #   If multiple is at True, it will return the values of each connected ports.
                if multiple:
                    outputs = []
                    for connected_port in range(len(self.inputs()[port_name].connected_ports())):
                        connected_port_name = self.inputs()[port_name].connected_ports()[connected_port].name()
                        if self.inputs()[port_name].connected_ports()[connected_port].node().get_output_property(connected_port_name).is_defined():
                            outputs.append(self.inputs()[port_name].connected_ports()[connected_port].node().get_output_property(connected_port_name))
                    return outputs
                else:
                    connected_port_name = self.inputs()[port_name].connected_ports()[0].name()
                    if self.inputs()[port_name].connected_ports()[0].node().get_output_property(connected_port_name).is_defined():
                        return self.inputs()[port_name].connected_ports()[0].node().get_output_property(connected_port_name)
            return None
        else:
            raise ValueError("Wrong port name given:", port_name)


    """
        Function to be overloaded.
        Set in the "is_defined" property if the inputs match the expectations to compute the outputs.
    """
    def check_inputs(self):
        raise NotImplementedError
    

    """
        Function to be overloaded.
        Compute the outputs and store them in their containers.
    """
    def update_from_input(self):
        raise NotImplementedError
    

    """
        Calls the update_values function of all of the node children
    """
    def propagate(self):
        #   Loop on outputs
        for output_id in range(len(self.outputs())):
            #   Loop on each ports to which the output is connected
            for connected_id in range(len(self.output(output_id).connected_ports())):
                #   Call the update_values function of the connected node
                self.output(output_id).connected_ports()[connected_id].node().update_values()
    

    """
        Resets all of the outputs containers.

        Can be overloaded depending on the used widgets
    """
    def reset_outputs(self):
        for output_name in self.outputs():
            self.output_properties[output_name].reset()
    
    
    """
        Add an input node and create its empty container
    """
    def add_custom_input(self, input_name, type_enum, multi_input=False):
        self.create_input_property(input_name, type_enum)
        self.add_input(input_name, color=get_color_from_enum(type_enum), multi_input=multi_input)

        
    """
        Add an output node and create its empty container
    """
    def add_custom_output(self, output_name, type_enum):
        self.create_output_property(output_name, type_enum)
        self.add_output(output_name, color=get_color_from_enum(type_enum))

        self.output_type_list[output_name] = type_enum

    """
        Creates an output empty container associated to the given enum
    """
    def create_output_property(self, output_name, type_enum):
        self.output_properties[output_name] = Container(type_enum)

    """
        Creates an input empty container associated to the given enum
    """
    def create_input_property(self, output_name, type_enum):
        self.input_properties[output_name] = Container(type_enum)
    
    """
        Returns if the output container if the given port name exists
    """
    def get_output_property(self, output_name):
        if output_name in self.output_properties:
            return self.output_properties[output_name]
        else:
            raise ValueError

    """
        Updates the output container value if the given port name exists
    """
    def set_output_property(self, output_name, value):
        if output_name in self.output_properties:
            self.output_properties[output_name].set_property(value)
        else:
            raise ValueError

    """
        Changes the node to red as its inputs are invalid
    """
    def set_invalid_color(self):
        self.set_property ('color', (40, 0, 0, 255))

    """
        Changes the node to gray as its inputs are valid
    """
    def set_valid_color(self):
        self.set_property('color', (13, 18, 23, 255))