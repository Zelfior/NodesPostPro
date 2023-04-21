from NodeGraphQt import NodeBaseWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from Qt import QtWidgets

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

from nodes.generic_node import GenericNode, PortValueType, check_type

class PltCanvasWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(PltCanvasWidget, self).__init__(parent)
        self.fig = Figure(figsize=(5, 5), dpi=100)
        self.canvas = FigureCanvasQTAgg(self.fig)
        self.axes = self.fig.add_subplot(111)

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.canvas)


    def get_value(self):
        widget = self.get_custom_widget()
        return ''




class pltWidget(NodeBaseWidget):
    def __init__(self, parent=None, name=''):
        super(pltWidget, self).__init__(parent)

        # set the name for node property.
        self.set_name('my_widget')

        # set the label above the widget.
        self.set_label('Custom Widget')

        self.canvas = PltCanvasWidget()
        # set the custom widget.
        self.set_custom_widget(self.canvas)

        self.input_arrays = []

        self.plot_parameters= {"legend": False, "x_log":False, "y_log":False, "color_bar":False}

        self.title = ""

    def update_plot(self, legend = False):
        self.canvas.axes.cla()  # clear the axes content

        for element in self.input_arrays:
            if element['element_type'] == "plot":
                kwargs_dict = {key:element[key] for key in element if key not in ["X", "Y", "element_type"]}
                self.canvas.axes.plot(element['X'], element['Y'], **kwargs_dict)
                
            if element['element_type'] == "scatter":
                kwargs_dict = {key:element[key] for key in element if key not in ["X", "Y", "element_type", "Color", "Color array"]}

                if "Color array" in element:
                    if type(element["Color array"]) == pd.DataFrame:
                        kwargs_dict["c"] = element["Color array"].values.tolist()
                    else:
                        kwargs_dict["c"] = list(element["Color array"])

                    print(kwargs_dict["c"])

                    if not "cmap" in kwargs_dict:
                        kwargs_dict["cmap"] = "viridis"
                elif "Color" in element:
                    kwargs_dict["c"] = element["Color"]

                self.canvas.axes.scatter(element['X'], element['Y'], **kwargs_dict)

        if not self.title == "":
            self.canvas.title = self.title

        if self.plot_parameters["legend"]:
            self.canvas.axes.legend()

        if self.plot_parameters["color_bar"]:
            self.canvas.fig.colorbar()
            
        if self.plot_parameters["x_log"]:
            self.canvas.axes.set_xscale('log')
        else:   
            self.canvas.axes.set_xscale('linear')
            
        if self.plot_parameters["y_log"]:
            self.canvas.axes.set_yscale('log')
        else:   
            self.canvas.axes.set_yscale('linear')

        self.canvas.canvas.draw()  # actually draw the new content



    def update_plot_list(self, array, plot_parameters):
        self.input_arrays = array
        self.plot_parameters = plot_parameters

        self.update_plot()



    def get_value(self):
        widget = self.get_custom_widget()
        return ''











class PltElementNode(GenericNode):

    def __init__(self):
        super(PltElementNode, self).__init__()

        self.element_type = "undefined"

    def update_from_input(self):
        properties_dict = {"element_type": self.element_type}

        for input in self.input_properties:
            input_value = self.get_value_from_port(input)

            if input_value is not None:
                properties_dict[input] = input_value.get_property()

        if not "X" in properties_dict:
            properties_dict["X"] = list(range(len(properties_dict["Y"])))

        self.set_output_property("Element", properties_dict)

        self.change_label("Information", "", True)


class PlotNode(PltElementNode):
    # unique node identifier.
    __identifier__ = 'Matplotlib'

    # initial default node name.
    NODE_NAME = 'Plt Plot'

    def __init__(self):
        super(PlotNode, self).__init__()

        self.add_custom_input('X', PortValueType.PLOTTABLE)
        self.add_custom_input('Y', PortValueType.PLOTTABLE)

        self.add_custom_input('label', PortValueType.STRING)

        self.add_custom_input('color', PortValueType.STRING)

        self.add_custom_input('linestyle', PortValueType.STRING)
        self.add_custom_input('linewidth ', PortValueType.FLOAT)
        
        self.add_custom_input('marker', PortValueType.STRING)
        self.add_custom_input('markersize', PortValueType.FLOAT)

        self.add_custom_input('alpha', PortValueType.FLOAT)

        self.add_custom_output('Element', PortValueType.DICT)

        self.add_label("Information")

        self.element_type = "plot"

    def check_inputs(self):
        input_Y = self.get_value_from_port("Y")

        self.set_property("is_valid", input_Y is not None \
                                            and input_Y.is_defined() \
                                                and check_type(input_Y.get_property(), PortValueType.PLOTTABLE))

        if input_Y is None:
            self.change_label("Information", "Input Y is not defined.", True)
        elif not input_Y.is_defined():
            self.change_label("Information", "Input Y is not defined.", True)
        elif not check_type(input_Y.get_property(), PortValueType.PLOTTABLE):
            self.change_label("Information", "Input Y is not of the right type.", True)

                    

        for input in self.input_properties:
            if not input == "Y":

                input_value = self.get_value_from_port(input)

                if input_value is not None:
                    self.set_property("is_valid", input_value.is_defined() \
                                                        and check_type(input_value.get_property(), self.input_properties[input].get_property_type()))

                    if not input_value.is_defined():
                        self.change_label("Information", "Input "+input+" is not defined.", True)
                    elif not check_type(input_value.get_property(), self.input_properties[input].get_property_type()):
                        self.change_label("Information", "Input "+input+" is not of the right type.", True)

                    

class ScatterNode(PltElementNode):
    # unique node identifier.
    __identifier__ = 'Matplotlib'

    # initial default node name.
    NODE_NAME = 'Plt Scatter'

    def __init__(self):
        super(ScatterNode, self).__init__()

        self.add_custom_input('X', PortValueType.PLOTTABLE)
        self.add_custom_input('Y', PortValueType.PLOTTABLE)

        self.add_custom_input('label', PortValueType.STRING)

        self.add_custom_input('Color', PortValueType.STRING)
        
        self.add_custom_input('Color array', PortValueType.PLOTTABLE)
        
        self.add_custom_input('cmap', PortValueType.STRING)

        self.add_custom_input('linestyle', PortValueType.STRING)
        self.add_custom_input('linewidth ', PortValueType.FLOAT)
        
        self.add_custom_input('marker', PortValueType.STRING)
        self.add_custom_input('markersize', PortValueType.FLOAT)

        self.add_custom_output('Element', PortValueType.DICT)

        self.add_label("Information")

        self.element_type = "scatter"

    def check_inputs(self):
        input_Y = self.get_value_from_port("Y")

        self.set_property("is_valid", input_Y is not None \
                                            and input_Y.is_defined() \
                                                and check_type(input_Y.get_property(), PortValueType.PLOTTABLE))

        if input_Y is None:
            self.change_label("Information", "Input Y is not defined.", True)
        elif not input_Y.is_defined():
            self.change_label("Information", "Input Y is not defined.", True)
        elif not check_type(input_Y.get_property(), PortValueType.PLOTTABLE):
            self.change_label("Information", "Input Y is not of the right type.", True)

                    

        for input in self.input_properties:
            if not input == "Y":

                input_value = self.get_value_from_port(input)

                if input_value is not None:
                    self.set_property("is_valid", input_value.is_defined() \
                                                        and check_type(input_value.get_property(), self.input_properties[input].get_property_type()))

                    if not input_value.is_defined():
                        self.change_label("Information", "Input "+input+" is not defined.", True)
                    elif not check_type(input_value.get_property(), self.input_properties[input].get_property_type()):
                        self.change_label("Information", "Input "+input+" is not of the right type.", True)




class PltShowNode(GenericNode):

    # unique node identifier.
    __identifier__ = 'Matplotlib'

    # initial default node name.
    NODE_NAME = 'Show Plot'

    def __init__(self):
        super(PltShowNode, self).__init__()

        # create input & output ports
        self.add_custom_input('Input Plottable', PortValueType.DICT, multi_input=True)
        
        self.add_custom_input('Title', PortValueType.STRING)
        
        self.add_custom_input('X_min', PortValueType.FLOAT)
        self.add_custom_input('X_max', PortValueType.FLOAT)
        
        self.add_custom_input('Y_min', PortValueType.FLOAT)
        self.add_custom_input('Y_max', PortValueType.FLOAT)
        
        self.add_checkbox("x_log", text='X log scale')
        self.add_checkbox("y_log", text='Y log scale')
        self.add_checkbox("legend", text='Legend')
        self.add_checkbox("color_bar", text='Color bar')

        self.plot_widget = pltWidget(self.view, name="plot")

        self.view.add_widget(self.plot_widget)
        self.view.draw_node()

        self.plot_widget.update_plot()
        
        self.add_label("Information")

    def update_from_input(self):
        if not self.get_value_from_port("Input Plottable") == None:
            self.input_arrays = [element.get_property() for element in self.get_value_from_port("Input Plottable", multiple=True)]

            plot_parameters = {"legend":self.get_property("legend"),
                                    "x_log":self.get_property("x_log"),
                                    "y_log":self.get_property("y_log"),
                                    "color_bar":self.get_property("y_log")}

            self.plot_widget.update_plot_list(self.input_arrays, plot_parameters)


    def check_inputs(self):
        input_given = self.get_value_from_port("Input Plottable")
        
        self.set_property("is_valid", input_given is not None \
                                            and input_given.is_defined() \
                                                and check_type(input_given.get_property(), PortValueType.DICT))
        
        if input_given is None or not input_given.is_defined():
                self.change_label("Information", "Input not plugged to a defined plottable.", True)
        elif not check_type(input_given.get_property(), PortValueType.PLOTTABLE):
                self.change_label("Information", "Plugged is not valid plottable.", True)

    def reset_outputs(self):
        super(PltShowNode, self).reset_outputs()

        self.plot_widget.update_plot_list([], {"legend": False, "x_log":False, "y_log":False, "color_bar":False})
        self.change_label("Information", "", False)

