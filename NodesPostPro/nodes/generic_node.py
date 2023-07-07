from NodeGraphQt import BaseNode
from NodesPostPro.nodes.custom_widgets import *

from NodesPostPro.nodes.container import *

import functools

from Qt import QtCore, QtGui

import random

import os

from NodeGraphQt.widgets.dialogs import FileDialog
from NodeGraphQt.widgets.node_widgets import _NodeGroupBox



def check_cast_type_from_string(name:str, enum_type:PortValueType):
    if enum_type == PortValueType.FLOAT:
        try:
            float(name)
            return True
        except ValueError:
            return False
    elif enum_type == PortValueType.INTEGER:
        return name.lstrip("-").isdigit()
    elif enum_type == PortValueType.BOOL:
        return name.lower().replace(" ", "") in ['yes', 'true', '1', "1.", 'no', 'false', '0', '0.']
    elif enum_type == PortValueType.STRING:
        return True
    else:
        raise ValueError("Given enum type was not implemented : "+str(enum_type))

def draw_triangle_port(color, painter, rect, info):
    """
    Custom paint function for drawing a Triangle shaped port.

    Args:
        painter (QtGui.QPainter): painter object.
        rect (QtCore.QRectF): port rect used to describe parameters
                              needed to draw.
        info (dict): information describing the ports current state.
            {
                'port_type': 'in',
                'color': (0, 0, 0),
                'border_color': (255, 255, 255),
                'multi_connection': False,
                'connected': False,
                'hovered': False,
            }
    """
    painter.save()

    size = int(rect.height() / 2)
    triangle = QtGui.QPolygonF()
    triangle.append(QtCore.QPointF(-size, size))
    triangle.append(QtCore.QPointF(0.0, -size))
    triangle.append(QtCore.QPointF(size, size))

    transform = QtGui.QTransform()
    transform.translate(rect.center().x(), rect.center().y())
    port_poly = transform.map(triangle)

    # mouse over port color.
    if info['hovered']:
        color = QtGui.QColor(*info['color'])
        border_color = QtGui.QColor(136, 255, 35)
    # port connected color.
    elif info['connected']:
        color = QtGui.QColor(*info['color'])
        border_color = QtGui.QColor(200, 130, 70)
    # default port color
    else:
        color = QtGui.QColor(*info['color'])
        border_color = QtGui.QColor(*info['border_color'])

    pen = QtGui.QPen(border_color, 1.8)
    pen.setJoinStyle(QtCore.Qt.MiterJoin)

    painter.setPen(pen)
    painter.setBrush(color)
    painter.drawPolygon(port_poly)

    painter.restore()

def draw_square_port(color, painter, rect, info):
    """
    Custom paint function for drawing a Square shaped port.

    Args:
        painter (QtGui.QPainter): painter object.
        rect (QtCore.QRectF): port rect used to describe parameters
                              needed to draw.
        info (dict): information describing the ports current state.
            {
                'port_type': 'in',
                'color': (0, 0, 0),
                'border_color': (255, 255, 255),
                'multi_connection': False,
                'connected': False,
                'hovered': False,
            }
    """
    painter.save()
    #color = QtGui.QColor(color)

    info['color'] = color
    # mouse over port color.
    if info['hovered']:
        color = QtGui.QColor(*info['color'])
        border_color = QtGui.QColor(136, 255, 35, 255)
    # port connected color.
    elif info['connected']:
        color = QtGui.QColor(*info['color'])
        border_color = QtGui.QColor(200, 130, 70)
    # default port color
    else:
        color = QtGui.QColor(*info['color'])
        border_color = QtGui.QColor(*info['border_color'])

    pen = QtGui.QPen(border_color, 1.8)
    pen.setJoinStyle(QtCore.Qt.MiterJoin)

    painter.setPen(pen)
    painter.setBrush(color)
    painter.drawRect(rect)

    painter.restore()


"""
    Generic node class that embed the value transmission functions
"""
class GenericNode(BaseNode):
    def __init__(self, to_update = False):
        super(GenericNode, self).__init__()

        self.output_type_list = {"is_valid": PortValueType.BOOL}

        self.create_property("is_valid", False)

        self.property_to_update = []

        self.to_update = True

        self.output_properties = {}
        self.input_properties = {}
        self.widget_properties = {}
        
        self.label_list = {}
        self.twin_inputs = []

        self.int_selectors = []

        self.check_seed = -1

        self.is_iterated_compatible = False
        self.has_iterators = False
        self.iterator_length = -1
        self.requires_compatible_iterator = False
        

    def is_input_valid(self, input_name):
        if input_name in self.input_properties:
            value = self.get_value_from_port(input_name)
            if value is not None:
                input_property_type = self.input_properties[input_name].get_property_type()
        else:
            property = self.get_property(input_name)
            value = Container(self.widget_properties[input_name])
            value.set_property(property)
            input_property_type = self.widget_properties[input_name]

        if value is not None:
            is_iterated = value.is_iterated()
        else:
            is_iterated = False
        
        if is_iterated:
            is_valid = value is not None \
                            and value.is_defined() \
                                and check_type(value.get_iterated_property()[0], input_property_type)

        else:
            is_valid = value is not None \
                            and value.is_defined() \
                                and check_type(value.get_property(), input_property_type)

        message = ""

        if value is None:
            message = input_name+" is not defined."

        elif not value.is_defined():
            message = input_name+" is not defined."

        elif not is_iterated and not check_type(value.get_property(), input_property_type):
            message = input_name+" is not of the right type."

        elif is_iterated and not check_type(value.get_iterated_property()[0], input_property_type):
            message = input_name+" iterator is not of the right type."

        return is_valid, message     

    def add_label(self, label_name, label = False):
        if label_name in self.label_list:
            raise ValueError("Label name already exists")
        else:
            self.label_list[label_name] = InputLabelWidget(self.view, name = label_name, label=label)
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
            raise ValueError("Label "+label_name+" doesn't exists")

    """
        BaseNode set_property overload:
            Starts the node output property update process when a property is changed if the property is not "is_valid" and if the node is not resetting (prevents infinite loops)
    """
    def set_property(self, name, value, push_undo=True):
        super(GenericNode, self).set_property(name, value, push_undo=push_undo)

        if name in self.property_to_update:
            self.update_values()

        
    """
        BaseNode set_property overload:
            Starts the node output property update process when an input port is plugged
    """
    def on_input_connected(self, in_port, out_port):
        super(GenericNode, self).on_input_connected(in_port, out_port)

        new_seed = random.randint(0, 500000)
        while new_seed == self.check_seed:
            new_seed = random.randint(0, 500000)

        self.check_seed = new_seed

        self.update_values()

    """
        BaseNode set_property overload:
            Starts the node output property update process when an input port is unplugged
    """
    def on_input_disconnected(self, in_port, out_port):
        super(GenericNode, self).on_input_disconnected(in_port, out_port)

        new_seed = random.randint(0, 500000)
        while new_seed == self.check_seed:
            new_seed = random.randint(0, 500000)

        self.check_seed = new_seed
        
        self.update_values()

    def repaint_ports(self):
        for property_name in self.input_properties:
            for port in self.view.inputs: 
                if port.name == property_name:
                    if self.input_properties[port.name].is_iterated():
                        port.set_painter(functools.partial(draw_triangle_port, get_color_from_enum(self.input_properties[port.name].get_property_type())))
                    else:
                        port.set_painter(functools.partial(draw_square_port, get_color_from_enum(self.input_properties[port.name].get_property_type())))
                    
        for property_name in self.output_properties:
            for port in self.view.outputs: 
                if port.name == property_name:
                    if self.output_properties[port.name].is_iterated():
                        port.set_painter(functools.partial(draw_triangle_port, get_color_from_enum(self.output_properties[port.name].get_property_type())))
                    else:
                        port.set_painter(functools.partial(draw_square_port, get_color_from_enum(self.output_properties[port.name].get_property_type())))
                    

    def check_iterators(self):
        self.has_iterators = False
        self.iterator_length = -1
        
        for input_ in self.input_properties:
            if self.get_value_from_port(input_) is not None:
                self.has_iterators |= self.get_value_from_port(input_).is_iterated()


        if self.has_iterators and not self.is_iterated_compatible:
            self.set_property("is_valid", False)

            if "Information" in self.label_list:
                self.change_label("Information", self.NODE_NAME+" node is not iterator compatible.", True)
            else:
                if len(list(self.label_list.keys())) > 0:
                    self.change_label(list(self.label_list.keys())[0], self.NODE_NAME+" node is not iterator compatible.", True) 

        elif self.has_iterators:
            for input_ in self.input_properties:
                if self.get_value_from_port(input_) is not None:
                    if self.get_value_from_port(input_).is_iterated():
                        if self.iterator_length == -1:
                            self.iterator_length = len(self.get_value_from_port(input_).get_iterated_property())
                        elif len(self.get_value_from_port(input_).get_iterated_property()) != self.iterator_length:
                            self.set_property("is_valid", False)
                            
                            if "Information" in self.label_list:
                                self.change_label("Information", "Given iterators have different length", True)
                            else:
                                if len(list(self.label_list.keys())) > 0:
                                    self.change_label(list(self.label_list.keys())[0], "Given iterators have different length", True) 

                            break

            
    """
        Node output property update process:
            Checks the inputs to know if they match the expectation to compute the outputs. The result is stored in the property "is_valid".

            If True:
                -   call the update_from_input function, that will compute the outputs
            Else:
                -   Resets the node outputs
    """
    def update_values(self, propagate = True):
        if self.to_update:
            
            print("Updating node "+self._view.name)
            self.set_property("is_valid", True)

            self.check_iterators()

            if self.get_property("is_valid"):
                self.check_inputs()

            self.check_children_loop(self.check_seed)

            if self.get_property("is_valid"):
                self.set_valid_color()

                self.update_from_input()

                self.repaint_ports()

            else:
                self.set_invalid_color()
                self.reset_outputs()

            self.view.draw_node()
            self.view.update()
            self.update()
            self.update_twin_inputs()

            if propagate:
                self.propagate()
            
            if self.get_property("is_valid"):
                for port in self.view.inputs:
                    for pipe in port._pipes:
                        pipe._color = get_color_from_enum(self.input_properties[port.name].get_property_type())


    """
        TODO : change length with iterators
        Get the value associated to the port to which the given input port is connected
    """
    def get_value_from_port(self, port_name, multiple = False) -> Container:
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


    def make_input_dict(self, i, error_messages = False):
        input_dict = {}
        
        for input in self.input_properties:
            if input in self.twin_inputs:
                valid, message = self.is_twin_input_valid(input)
                if valid:
                    input_container = self.get_twin_input(input)
            else:
                valid, message = self.is_input_valid(input)
                if valid:
                    input_container = self.get_value_from_port(input)

            if valid:
                if input_container.is_iterated():
                    input_dict[input] = input_container.get_iterated_property()[i]
                else:
                    input_dict[input] = input_container.get_property()
            else:
                if error_messages:
                    input_dict[input] = "Error_"+message


        for input in self.property_to_update:
            if input in self.twin_inputs:
                valid, message = self.is_twin_input_valid(input)
                if valid:
                    input_container = self.get_twin_input(input)
            else:
                valid, message = self.is_input_valid(input)
                if valid:
                    input_container = Container(self.widget_properties[input])
                    input_container.set_property(self.get_property(input))

            if valid:
                if input_container.is_iterated():
                    input_dict[input] = input_container.get_iterated_property()[i]
                else:
                    input_dict[input] = input_container.get_property()
            else:
                if error_messages:
                    input_dict[input] = "Error_"+message

        return input_dict


    """
        Generic function that checks the input values based on a node defined operation function "check_function".
        Set in the "is_defined" property if the inputs match the expectations to compute the outputs.
    """
    def check_inputs(self):
        if self.has_iterators:
            is_valid = True
            message = ""
            label_name = ""

            for i in range(self.iterator_length):
                input_dict = self.make_input_dict(i, error_messages=True)

                valid, message, label_name = self.check_function(input_dict)

                is_valid &= valid
                
                if not is_valid:
                    break
    
            self.set_property("is_valid", is_valid)

            if (not is_valid) and label_name != "":
                self.change_label(label_name, message, True)
            elif label_name != "":
                self.change_label(label_name, "", False)
        else:

            input_dict = self.make_input_dict(0, error_messages=True)
                        
            valid, message, label_name = self.check_function(input_dict, first=True)

            self.set_property("is_valid", valid)

            if (not valid) and label_name != "":
                self.change_label(label_name, message, True)
            elif label_name != "":
                self.change_label(label_name, "", False)
                

    """
        Generic function that updates the outputs based on a node defined operation function "update_function".
        Compute the outputs and store them in their containers.
    """
    def update_from_input(self):
        if self.has_iterators:
            output_dicts = []

            for i in range(self.iterator_length):
                input_dict = self.make_input_dict(i)

                output_dicts.append(self.update_function(input_dict, first = (i == 0)))

            if len(output_dicts) > 0:
                for output in output_dicts[0]:
                    if not output.startswith("__message__"):
                        self.set_output_property(output, [output_dicts[i][output] for i in range(self.iterator_length)], True)
                    else:
                        self.change_label(output.replace("__message__",""), str(output_dicts[0][output])+" x "+str(self.iterator_length), False)
 

        else:
            input_dict = self.make_input_dict(0)

            output_dict = self.update_function(input_dict, first=True)

            for output in output_dict:
                if not output.startswith("__message__"):
                    self.set_output_property(output, output_dict[output], False)
                else:
                    self.change_label(output.replace("__message__",""), output_dict[output], False)
            
    
    def update_function(self, input_dict, first = False):
        raise NotImplementedError("Neither update_from_input nor update_function defined for node : \""+self.NODE_NAME+"\"")

    def check_function(self, input_dict, first = False):
        raise NotImplementedError("Neither check_inputs nor check_function defined for node : \""+self.NODE_NAME+"\"")

    """
        Calls the update_values function of all of the node children
    """
    def propagate(self):
        #   Getting children in order to update
        import NodesPostPro.nodes.node_heritage as node_heritage

        update_order_names = node_heritage.get_propagation_order(self)
        children_list = node_heritage.get_children_dict(self)

        del update_order_names[0]

        while len(update_order_names) > 0:
            children_list[update_order_names[0]].update_values(propagate = False)
            del update_order_names[0]


    """
        Resets all of the outputs containers.

        Can be overloaded depending on the used widgets
    """
    def reset_outputs(self):
        for output_name in self.outputs():
            self.output_properties[output_name].reset()
    
        self.has_iterators = False
        self.iterator_length = -1

        self.repaint_ports()


    """
        Add an input node and create its empty container
    """
    def add_custom_input(self, input_name, type_enum, multi_input=False):
        self.create_input_property(input_name, type_enum)
        self.add_input(input_name, color=get_color_from_enum(type_enum), multi_input=multi_input, painter_func=functools.partial(draw_square_port, get_color_from_enum(self.input_properties[input_name].get_property_type())))

        
    """
        Add an output node and create its empty container
    """
    def add_custom_output(self, output_name, type_enum):
        self.create_output_property(output_name, type_enum)
        self.add_output(output_name, color=get_color_from_enum(type_enum), painter_func=functools.partial(draw_square_port, get_color_from_enum(self.output_properties[output_name].get_property_type())))

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
    def get_output_property(self, output_name) -> Container:
        if output_name in self.output_properties:
            return self.output_properties[output_name]
        else:
            raise ValueError("Given output property doesn't exist: "+str(output_name))

    """
        Updates the output container value if the given port name exists
    """
    def set_output_property(self, output_name, value, iterated):
        if output_name in self.output_properties:
            if iterated:
                self.output_properties[output_name].set_iterated_property(value, check_comparable = self.requires_compatible_iterator)
            else:
                self.output_properties[output_name].set_property(value)
        else:
            raise ValueError("Given output property doesn't exist: "+str(output_name))

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

    """
        Tells if the current is to update
    """
    def set_to_update(self, value:bool):
        self.to_update = value




    def add_table_input(self, name, label):
        table_selector = InputTableWidget(self.view, name=name)
        self.create_property(name, 0)

        table_selector.value_changed.connect(lambda k, v: self.set_property(k, v))

        self.view.add_widget(table_selector)
        self.view.draw_node()

        self.widget_properties[name] = PortValueType.LIST
        # self.property_to_update.append(name)

        return table_selector

    def add_combo_menu(self, name, label, items=[]):
        super(GenericNode, self).add_combo_menu(name, label, items=items)
        self.widget_properties[name] = PortValueType.STRING
        self.property_to_update.append(name)

    def add_text_input(self, name, label, default, tab = None, text_type=PortValueType.STRING):
        super(GenericNode, self).add_text_input(name, label, default, tab = tab)
        self.widget_properties[name] = text_type
        self.property_to_update.append(name)


    def add_int_selector(self, name, label):

        int_selector = IntSelector_Widget(self.view, name=name, label=label)
        self.widget_properties[name] = PortValueType.INTEGER

        self.create_property(name, 0)

        int_selector.value_changed.connect(lambda k, v: self.set_property(k, v))

        self.view.add_widget(int_selector)
        self.view.draw_node()

        self.property_to_update.append(name)

        self.int_selectors.append(int_selector)

        return int_selector

    def add_button_widget(self, name):

        button = ButtonNodeWidget(self.view, name=name)
        self.create_property(name, 0)

        self.view.add_widget(button)
        self.view.draw_node()

        return button

    def add_checkbox(self, name, text=''):
        super(GenericNode, self).add_checkbox(name, text=text)
        self.widget_properties[name] = PortValueType.BOOL
        self.property_to_update.append(name)

    """
        widget_type : "TEXT", "INT_SELECTOR"
    """
    def add_twin_input(self, name:str, type_enum:PortValueType, widget_type:str='TEXT', default = ""):

        if not type_enum in [PortValueType.BOOL,
                                PortValueType.INTEGER,
                                PortValueType.FLOAT,
                                PortValueType.STRING]:
            raise ValueError("Given twin input must be castable from string, received type: "+str(type_enum))

        self.add_custom_input(name, type_enum)
        if widget_type == "TEXT":
            self.add_text_input(name, name, default, text_type=type_enum)
        elif widget_type == "INT_SELECTOR":
            self.add_int_selector(name, name)


        self.add_label(name+"_label")

        self.label_list[name+"_label"].setVisible(False)

        self.twin_inputs.append(name)


    def is_twin_input_valid(self, name:str):
        if not name in self.twin_inputs:
            raise ValueError(name+" is not in the twin inputs list.")

        is_port_valid, message = self.is_input_valid(name)

        if is_port_valid:
            return is_port_valid, message

        else:
            if check_cast_type_from_string(self.get_property(name), self.input_properties[name].get_property_type()):
                return True, ""
            else:
                return False, "Input "+ name + " is not valid."

    def get_twin_input(self, name:str) -> Container:
        if not name in self.twin_inputs:
            raise ValueError(name+" is not in the twin inputs list.")
        
        is_port_valid, message = self.is_input_valid(name)

        if is_port_valid:
            return self.get_value_from_port(name)
        else:
            container = Container(self.input_properties[name].get_property_type())

            if self.input_properties[name].get_property_type() == PortValueType.INTEGER:
                container.set_property(int(self.get_property(name)))
            elif self.input_properties[name].get_property_type() == PortValueType.FLOAT:
                container.set_property(float(self.get_property(name)))
            elif self.input_properties[name].get_property_type() == PortValueType.BOOL:
                container.set_property(bool(self.get_property(name)))
            else:
                container.set_property(self.get_property(name))

            if self.has_iterators:
                contained_value = container.get_property()
                container.set_iterated_property([contained_value]*self.iterator_length, check_comparable=self.requires_compatible_iterator)

            return container

    def update_twin_inputs(self):
        for name in self.twin_inputs:
            is_port_valid, message = self.is_input_valid(name)

            if is_port_valid:
                self.get_widget(name).setVisible(False)
                self.label_list[name+"_label"].setVisible(True)
                if self.has_iterators:
                    self.change_label(name+"_label", name+" : "+str(self.get_value_from_port(name).get_iterated_property()[0]), False)
                else:
                    self.change_label(name+"_label", name+" : "+str(self.get_value_from_port(name).get_property()), False)
            else:
                self.get_widget(name).setVisible(True)
                self.label_list[name+"_label"].setVisible(False)


        

        


    """
        Checks if there is a loop in the graph, untested as NodeGraphQt seems to be loop proof.
    
    """
    def check_children_loop(self, seed_id):

        list_children = []

        if self.check_seed != seed_id:
            self.check_seed = seed_id

            
            for output_id in self.output_type_list:
                for connected_id in range(len(self.output(output_id).connected_ports())):
                    found_children = self.output(output_id).connected_ports()[connected_id].node().check_children_loop()

                    for child in found_children:
                        if not child in list_children:
                            list_children.append(child)

            if self.name in list_children:
                self.set_property("is_valid", False)

                if "Information" in self.label_list:
                    self.change_label("Information", "Nodes link loop found.", True)
                else:
                    if len(list(self.label_list.keys())) > 0:
                        self.change_label(list(self.label_list.keys())[0], "Nodes link loop found.", True)               
                
                self.output(output_id).connected_ports()[connected_id].node().check_children_loop()

        return list_children

        
    def get_file_name(self, ext=None):
        ext = '*{} '.format(ext) if ext else ''
        ext_filter = ';;'.join([
            'CSV file ({}*csv)'.format(ext), 'All Files (*)'
        ])

        current_dir = os.getcwd()
        file_dlg = FileDialog.getOpenFileName(
            None, 'Open File', current_dir, ext_filter)
        file = file_dlg[0] or None

        self.set_property("Filename", file)

    def get_layout(self):
        return _NodeGroupBox(self._label).layout()
