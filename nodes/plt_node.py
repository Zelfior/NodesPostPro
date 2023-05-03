from NodeGraphQt import NodeBaseWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from Qt import QtWidgets

from NodeGraphQt.widgets.node_widgets import _NodeGroupBox

import pandas as pd
import numpy as np
import os

from nodes.generic_node import GenericNode, PortValueType, check_type
from nodes.custom_widgets import IntSelector_Widget
from nodes.cast_nodes import is_float
from nodes.container import PltContainer


def plot_element_on_axis(figure : Figure, axis : Axes, element):

    if element['element_type'] == "plot":
        kwargs_dict = {key:element[key] for key in element if key not in ["X", "Y", "element_type", "priority"]}
        return axis.plot(element['X'], element['Y'], **kwargs_dict)
        
    elif element['element_type'] == "fill_between":
        kwargs_dict = {key:element[key] for key in element if key not in ["X", "Y1", "Y2", "element_type", "priority"]}
        return axis.fill_between(element['X'], element['Y1'], element['Y2'], **kwargs_dict)
        
    elif element['element_type'] == "imshow":
        kwargs_dict = {key:element[key] for key in element if key not in ["X", "Y", "element_type", "priority"]}
        kwargs_dict["aspect"] = "auto"
        return axis.imshow(element['Y'], **kwargs_dict)

    elif element['element_type'] == "scatter":
        kwargs_dict = {key:element[key] for key in element if key not in ["X", "Y", "element_type", "Color", "Color array", "priority"]}

        if "Color array" in element:
            if type(element["Color array"]) == pd.DataFrame:
                kwargs_dict["c"] = element["Color array"].values.tolist()
            else:
                kwargs_dict["c"] = list(element["Color array"])

            if not "cmap" in kwargs_dict:
                kwargs_dict["cmap"] = "viridis"
        elif "Color" in element:
            kwargs_dict["c"] = element["Color"]

        return axis.scatter(element['X'], element['Y'], **kwargs_dict)

    elif element['element_type'] == "hist":
        kwargs_dict = {key:element[key] for key in element if key not in ["X", "element_type", "priority"]}
        return axis.hist(element['X'], **kwargs_dict)
                


class PltCanvasWidget(QtWidgets.QWidget):
    def __init__(self, width = 6, height = 6, parent=None):
        super(PltCanvasWidget, self).__init__(parent)
        self.fig = Figure(figsize=(width, height))
        self.canvas = FigureCanvasQTAgg(self.fig)
        self.axes = self.fig.add_subplot(111)
        self.twinx_axes = None

        self.layout_ = QtWidgets.QHBoxLayout(self)
        self.layout_.setContentsMargins(-5, -5, -5, -5)
        self.layout_.addWidget(self.canvas)


    def get_value(self):
        return ''
    
    def update_figure(self, width, height):
        self.fig.clear()
        self.axes = self.fig.add_subplot(111)
        self.twinx_axes = None

        self.fig.set_figwidth(width)
        self.fig.set_figheight(height)

        self.canvas.adjustSize()





class pltWidget(NodeBaseWidget):
    def __init__(self, parent=None, name=''):
        super(pltWidget, self).__init__(parent)

        # set the name for node property.
        self.set_name('Plot_Widget')

        self.canvas = PltCanvasWidget()
        # set the custom widget.
        self.set_custom_widget(self.canvas)

        self.input_arrays_1 = []
        self.input_arrays_2 = []

        self.plot_parameters= {"legend": False, "x_log":False, "y_log":False, "color_bar":False}

        self.title = ""

    def sort_by_priority(self, array):
        if array == None:
            return None
        
        new_array = []

        for element in array:
            if len(new_array) == 0:
                new_array.append(element)
            else:
                i = 0
                while i < len(new_array) and new_array[i]["priority"] < element["priority"]:
                    i += 1 
                new_array.insert(i, element)

        return new_array


    def update_plot(self):

        
        if "width" in self.plot_parameters:
            self.canvas.update_figure(int(self.plot_parameters["width"]), int(self.plot_parameters["height"]))

            #   On reset le custom widget du canvas pour qu'il prenne en compte la nouvelle taille
            group = _NodeGroupBox(self._label)
            group.add_node_widget(self.canvas)
            self.setWidget(group)

        else:
            self.canvas.fig.clear()  # clear the axes content

            self.canvas.axes = self.canvas.fig.add_subplot(111)
            self.canvas.twinx_axes = None

        self.input_arrays_1 = self.sort_by_priority(self.input_arrays_1)
        self.input_arrays_2 = self.sort_by_priority(self.input_arrays_2)

        mappables= []

        if self.input_arrays_1 is not None:
            for element in self.input_arrays_1:
                el = plot_element_on_axis(self.canvas.fig, self.canvas.axes, element)

                if element['element_type'] == "imshow":
                    mappables.append(el)
                
        if self.input_arrays_2 is not None:
            self.canvas.twinx_axes = self.canvas.axes.twinx()

            for element in self.input_arrays_2:
                el = plot_element_on_axis(self.canvas.fig, self.canvas.twinx_axes, element)

                if element['element_type'] == "imshow":
                    mappables.append(el)
                

        if "Title" in self.plot_parameters:
            self.canvas.axes.set_title(self.plot_parameters["Title"])

        if "X_min" in self.plot_parameters:
            if "X_max" in self.plot_parameters:
                self.canvas.axes.set_xlim((self.plot_parameters["X_min"], self.plot_parameters["X_max"]))
            else:
                self.canvas.axes.set_xlim((self.plot_parameters["X_min"], None))
        elif "X_max" in self.plot_parameters:
            self.canvas.axes.set_xlim((None, self.plot_parameters["X_max"]))

        if "Y_min" in self.plot_parameters:
            if "Y_max" in self.plot_parameters:
                self.canvas.axes.set_ylim((self.plot_parameters["Y_min"], self.plot_parameters["Y_max"]))
            else:
                self.canvas.axes.set_ylim((self.plot_parameters["Y_min"], None))
        elif "Y_max" in self.plot_parameters:
            self.canvas.axes.set_ylim((None, self.plot_parameters["Y_max"]))


        if "X label" in self.plot_parameters:
            self.canvas.axes.set_xlabel(self.plot_parameters["X label"])
            
        if "Y label 1" in self.plot_parameters:
            if self.input_arrays_1 is not None:
                self.canvas.axes.set_ylabel(self.plot_parameters["Y label 1"])
            
        if "Y label 2" in self.plot_parameters:
            if self.canvas.twinx_axes is not None:
                self.canvas.twinx_axes.set_ylabel(self.plot_parameters["Y label 2"])



        if self.plot_parameters["legend"]:
            if self.canvas.twinx_axes != None:
                h1, l1 = self.canvas.axes.get_legend_handles_labels()
                h2, l2 = self.canvas.twinx_axes.get_legend_handles_labels()
                self.canvas.axes.legend(handles=h1+h2, labels=l1+l2)
            else:
                self.canvas.axes.legend()

        if self.plot_parameters["color_bar"]:
            if len(mappables) > 0:
                self.canvas.fig.colorbar(mappables[0])
            
        if self.plot_parameters["x_log"]:
            self.canvas.axes.set_xscale('log')
        else:   
            self.canvas.axes.set_xscale('linear')
            
        if self.plot_parameters["y_log"]:
            self.canvas.axes.set_yscale('log')
        else:   
            self.canvas.axes.set_yscale('linear')

        self.canvas.fig.tight_layout()
        self.canvas.canvas.draw()  # actually draw the new content




    def update_plot_list(self, array_1, array_2, plot_parameters):
        self.input_arrays_1 = array_1
        self.input_arrays_2 = array_2
        self.plot_parameters = plot_parameters

        self.update_plot()



    def get_value(self):
        return ''

    def set_value(self, value):
        pass



def are_plottable_compatible(plot1, plot2):
    plot1 = np.squeeze(np.array(plot1))
    plot2 = np.squeeze(np.array(plot2))

    return plot1.shape == plot2.shape















class ImShowNode(GenericNode):
    # unique node identifier.
    __identifier__ = 'Matplotlib'

    # initial default node name.
    NODE_NAME = 'ImShow'

    def __init__(self):
        super(ImShowNode, self).__init__()

        # X, cmap=None, norm=None
        # self.add_custom_input('X', PortValueType.PLOTTABLE)
        self.add_custom_input('Y', PortValueType.PLOTTABLE)

        self.add_custom_input('label', PortValueType.STRING)

        self.add_combo_menu('norm', 'norm', items=["linear", "log", "symlog", "logit"])
        
        self.priority_widget = IntSelector_Widget(self.view, name="Priority", label='Priority')
        self.create_property("Priority", 0)
        self.priority_widget.value_changed.connect(lambda k, v: self.set_property(k, v))
        self.view.add_widget(self.priority_widget)
        self.view.draw_node()
        
        self.priority_widget.set_range(0, 50)

        self.add_custom_input('alpha', PortValueType.FLOAT)

        self.add_custom_output('Element', PortValueType.DICT)

        self.add_label("Information")

        self.element_type = "imshow"

        self.property_to_update.append("norm")
        self.property_to_update.append("Priority")

    def check_inputs(self):
        is_valid, message = self.is_input_valid("Y")

        self.set_property("is_valid", is_valid)

        if not is_valid:
            self.change_label("Information", message, True)
        else:
            if len(self.get_value_from_port("Y").get_property().shape) != 2:
                self.change_label("Information", "Y input should have 2 dimensions.", True)
                self.set_property("is_valid", False)

        for input in self.input_properties:
            if not input == "Y":

                input_value = self.get_value_from_port(input)

                if input_value is not None:
                    is_valid, message = self.is_input_valid(input)

                    self.set_property("is_valid", is_valid and self.get_property("is_valid"))

                    if not is_valid:
                        self.change_label("Information", message, True)

                   
    def update_from_input(self):
        
        properties_dict = {"element_type": self.element_type}

        for input in self.input_properties:
            input_value = self.get_value_from_port(input)

            if input_value is not None:
                properties_dict[input] = input_value.get_property()

        properties_dict['norm'] = self.get_property('norm')

        properties_dict['priority'] = int(self.priority_widget.get_value())

        self.set_output_property("Element", properties_dict)

        self.change_label("Information", "", True)












class PltElementNode(GenericNode):

    def __init__(self):
        super(PltElementNode, self).__init__()

        self.element_type = "undefined"
        self.y_name = 'Y'

    def update_from_input(self):
        properties_dict = {"element_type": self.element_type}

        for input in self.input_properties:
            input_value = self.get_value_from_port(input)

            if input_value is not None:
                properties_dict[input] = input_value.get_property()

        if not "X" in properties_dict:
            properties_dict["X"] = list(range(len(properties_dict[self.y_name])))

        self.set_output_property("Element", properties_dict)

        self.change_label("Information", "", True)

    def add_linestyle_combo(self):
        self.add_combo_menu('linestyle', 'linestyle', items=['solid', 'dotted', 'dashed', 'dashdot'])













class PlotNode(PltElementNode):
    # unique node identifier.
    __identifier__ = 'Matplotlib'

    # initial default node name.
    NODE_NAME = 'Plot'

    def __init__(self):
        super(PlotNode, self).__init__()

        self.add_custom_input('X', PortValueType.PLOTTABLE)
        self.add_custom_input('Y', PortValueType.PLOTTABLE)

        self.add_custom_input('label', PortValueType.STRING)

        self.add_custom_input('color', PortValueType.STRING)
        
        self.add_linestyle_combo()

        self.add_custom_input('linewidth', PortValueType.FLOAT)
        
        self.priority_widget = IntSelector_Widget(self.view, name="Priority", label='Priority')
        self.create_property("Priority", 0)
        self.priority_widget.value_changed.connect(lambda k, v: self.set_property(k, v))
        self.view.add_widget(self.priority_widget)
        self.view.draw_node()
        
        self.priority_widget.set_range(0, 50)

        self.add_combo_menu('marker', 'marker', items=["None", ".", ",", "o", "s", "D"])

        self.add_custom_input('markersize', PortValueType.FLOAT)

        self.add_custom_input('alpha', PortValueType.FLOAT)


        self.add_custom_output('Element', PortValueType.DICT)

        self.add_label("Information")

        self.element_type = "plot"

        self.property_to_update.append("Priority")
        self.property_to_update.append("marker")
        self.property_to_update.append("linestyle")

    def check_inputs(self):
        is_valid, message = self.is_input_valid("Y")

        self.set_property("is_valid", is_valid)

        if not is_valid:
            self.change_label("Information", message, True)
                    

        for input in self.input_properties:
            if not input == "Y":

                input_value = self.get_value_from_port(input)

                if input_value is not None:
                    is_valid, message = self.is_input_valid(input)

                    self.set_property("is_valid", is_valid and self.get_property("is_valid"))

                    if not is_valid:
                        self.change_label("Information", message, True)

                   
    def update_from_input(self):
        super(PlotNode, self).update_from_input()

        properties_dict = self.get_output_property("Element").get_property()

        properties_dict['linestyle'] = self.get_property('linestyle')

        if self.get_property('marker') != "None":
            properties_dict['marker'] = self.get_property('marker')

        properties_dict['priority'] = int(self.priority_widget.get_value())

        self.set_output_property("Element", properties_dict)












class FillBetweenNode(PltElementNode):
    # unique node identifier.
    __identifier__ = 'Matplotlib'

    # initial default node name.
    NODE_NAME = 'Fill Between'

    def __init__(self):
        super(FillBetweenNode, self).__init__()

        self.add_custom_input('X', PortValueType.PLOTTABLE)
        self.add_custom_input('Y1', PortValueType.PLOTTABLE)
        self.add_custom_input('Y2', PortValueType.PLOTTABLE)
        self.add_custom_input('Where', PortValueType.PLOTTABLE)

        self.add_custom_input('label', PortValueType.STRING)

        self.add_custom_input('color', PortValueType.STRING)

        # self.add_linestyle_combo()
        
        self.priority_widget = IntSelector_Widget(self.view, name="Priority", label='Priority')
        self.create_property("Priority", 0)
        self.priority_widget.value_changed.connect(lambda k, v: self.set_property(k, v))
        self.view.add_widget(self.priority_widget)
        self.view.draw_node()
        
        self.priority_widget.set_range(0, 50)

        self.add_custom_input('alpha', PortValueType.FLOAT)

        self.add_custom_output('Element', PortValueType.DICT)

        self.add_label("Information")

        self.element_type = "fill_between"
        self.y_name = 'Y1'

        self.property_to_update.append("Priority")

    def check_inputs(self):
        is_valid_x, message_x = self.is_input_valid("X")
        is_valid_y1, message_y1 = self.is_input_valid("Y1")
        is_valid_y2, message_y2 = self.is_input_valid("Y2")

        self.set_property("is_valid", is_valid_x and is_valid_y1 and is_valid_y2)

        if not is_valid_x:
            self.change_label("Information", message_x, True)
        elif not is_valid_y1:
            self.change_label("Information", message_y1, True)
        elif not is_valid_y2:
            self.change_label("Information", message_y2, True)
                    

        if self.get_property("is_valid"):
            if not are_plottable_compatible(self.get_value_from_port("X").get_property(), self.get_value_from_port("Y1").get_property()):
                self.change_label("Information", "Inputs X and Y1 are not compatible", True)
                self.set_property("is_valid", False)
                
            elif not are_plottable_compatible(self.get_value_from_port("X").get_property(), self.get_value_from_port("Y2").get_property()):
                self.change_label("Information", "Inputs X and Y2 are not compatible", True)
                self.set_property("is_valid", False)

            elif self.get_value_from_port("Where") is not None:
                if self.is_input_valid("Where")[0]:
                    if not are_plottable_compatible(self.get_value_from_port("X").get_property(), self.get_value_from_port("Where").get_property()):
                        self.change_label("Information", "Inputs X and Where are not compatible", True)
                        self.set_property("is_valid", False)
                    elif len(np.squeeze(np.array(self.get_value_from_port("X").get_property())).shape) > 1:
                        self.change_label("Information", "Inputs X should be 1D", True)
                        self.set_property("is_valid", False)
                else:
                    self.change_label("Information", self.is_input_valid("Where")[1], True)

            elif len(np.squeeze(np.array(self.get_value_from_port("X").get_property())).shape) > 1:
                self.change_label("Information", "Inputs X should be 1D", True)
                self.set_property("is_valid", False)
            elif len(np.squeeze(np.array(self.get_value_from_port("Y1").get_property())).shape) > 1:
                self.change_label("Information", "Inputs Y1 should be 1D", True)
                self.set_property("is_valid", False)
            elif len(np.squeeze(np.array(self.get_value_from_port("Y2").get_property())).shape) > 1:
                self.change_label("Information", "Inputs Y2 should be 1D", True)
                self.set_property("is_valid", False)


        for input in self.input_properties:
            if not input in ["X", "Y2", "Y1", "Where"]:

                input_value = self.get_value_from_port(input)

                if input_value is not None:
                    is_valid, message = self.is_input_valid(input)

                    self.set_property("is_valid", is_valid and self.get_property("is_valid"))

                    if not is_valid:
                        self.change_label("Information", message, True)

                   
    def update_from_input(self):
        super(FillBetweenNode, self).update_from_input()

        properties_dict = self.get_output_property("Element").get_property()

        for key in ["X", "Y1", "Y2"]:
            properties_dict[key] = np.squeeze(np.array(properties_dict[key]))

        if "Where" in properties_dict:
            properties_dict["where"] = np.squeeze(np.array(properties_dict["Where"]))
            del properties_dict["Where"]

        properties_dict['priority'] = int(self.priority_widget.get_value())

        self.set_output_property("Element", properties_dict)











class ScatterNode(PltElementNode):
    # unique node identifier.
    __identifier__ = 'Matplotlib'

    # initial default node name.
    NODE_NAME = 'Scatter'

    def __init__(self):
        super(ScatterNode, self).__init__()

        self.add_custom_input('X', PortValueType.PLOTTABLE)
        self.add_custom_input('Y', PortValueType.PLOTTABLE)

        self.add_custom_input('label', PortValueType.STRING)

        self.add_custom_input('Color', PortValueType.STRING)
        
        self.add_custom_input('Color array', PortValueType.PLOTTABLE)
        
        self.add_custom_input('cmap', PortValueType.STRING)

        self.add_custom_input('linewidth ', PortValueType.FLOAT)
        
        self.priority_widget = IntSelector_Widget(self.view, name="Priority", label='Priority')
        self.create_property("Priority", 0)
        self.priority_widget.value_changed.connect(lambda k, v: self.set_property(k, v))
        self.view.add_widget(self.priority_widget)
        self.view.draw_node()
        
        self.priority_widget.set_range(0, 50)

        self.add_combo_menu('marker', 'marker', items=["None", ".", ",", "o", "s", "D"])
        
        self.add_custom_input('markersize', PortValueType.FLOAT)

        self.add_custom_output('Element', PortValueType.DICT)

        self.add_label("Information")

        self.element_type = "scatter"

        self.property_to_update.append("Priority")
        self.property_to_update.append("marker")


    def check_inputs(self):
        is_valid, message = self.is_input_valid("Y")

        self.set_property("is_valid", is_valid)

        if not is_valid:
            self.change_label("Information", message, True)
                    

        for input in self.input_properties:
            if not input == "Y":

                input_value = self.get_value_from_port(input)

                if input_value is not None:
                    is_valid, message = self.is_input_valid(input)

                    self.set_property("is_valid", is_valid and self.get_property("is_valid"))

                    if not is_valid:
                        self.change_label("Information", message, True)


    def update_from_input(self):
        super(ScatterNode, self).update_from_input()

        properties_dict = self.get_output_property("Element").get_property()

        if self.get_property('marker') != "None":
            properties_dict['marker'] = self.get_property('marker')

        properties_dict['priority'] = int(self.priority_widget.get_value())

        self.set_output_property("Element", properties_dict)

















class HistNode(GenericNode):
    # unique node identifier.
    __identifier__ = 'Matplotlib'

    # initial default node name.
    NODE_NAME = 'Hist'

    def __init__(self):
        super(HistNode, self).__init__()

        # X, cmap=None, norm=None
        # self.add_custom_input('X', PortValueType.PLOTTABLE)
        self.add_custom_input('X', PortValueType.PLOTTABLE)
        self.add_custom_input('Bins', PortValueType.INTEGER)
        self.add_custom_input('Weight', PortValueType.PLOTTABLE)

        self.add_custom_input('X min', PortValueType.FLOAT)
        self.add_custom_input('X max', PortValueType.FLOAT)

        self.add_custom_input('color', PortValueType.STRING)

        self.add_checkbox("density", text='Density')
        self.add_checkbox("cumulative", text='Cumulative')
        self.add_checkbox("log", text='Log')

        self.add_custom_input('label', PortValueType.STRING)

        self.add_combo_menu('histtype', 'histtype', items=['bar', 'barstacked', 'step', 'stepfilled'])
        
        self.priority_widget = IntSelector_Widget(self.view, name="Priority", label='Priority')
        self.create_property("Priority", 0)
        self.priority_widget.value_changed.connect(lambda k, v: self.set_property(k, v))
        self.view.add_widget(self.priority_widget)
        self.view.draw_node()
        
        self.priority_widget.set_range(0, 50)

        self.add_custom_input('alpha', PortValueType.FLOAT)

        self.add_custom_output('Element', PortValueType.DICT)

        self.add_label("Information")

        self.element_type = "hist"

        self.property_to_update.append("density")
        self.property_to_update.append("cumulative")
        self.property_to_update.append("log")
        self.property_to_update.append("histtype")
        self.property_to_update.append("Priority")

    def check_inputs(self):
        is_valid, message = self.is_input_valid("X")

        self.set_property("is_valid", is_valid)

        if not is_valid:
            self.change_label("Information", message, True)


        for input in self.input_properties:
            if not input == "Y":

                input_value = self.get_value_from_port(input)

                if input_value is not None:
                    is_valid, message = self.is_input_valid(input)

                    self.set_property("is_valid", is_valid and self.get_property("is_valid"))

                    if not is_valid:
                        self.change_label("Information", message, True)

        if is_valid and self.is_input_valid("Weight")[0]:
            if np.squeeze(np.array(self.get_value_from_port("X").get_property())).shape != \
                np.squeeze(np.array(self.get_value_from_port("Weight").get_property())).shape:
                    self.set_property("is_valid", False)
                    self.change_label("Information", "Arrays X and Weight should have the same shape.", True)

                   
    def update_from_input(self):
        
        properties_dict = {"element_type": self.element_type}

        for input in self.input_properties:
            input_value = self.get_value_from_port(input)

            if input_value is not None:
                properties_dict[input] = input_value.get_property()

        properties_dict['histtype'] = self.get_property('histtype')
        properties_dict['density'] = self.get_property('density')
        properties_dict['cumulative'] = self.get_property('cumulative')
        properties_dict['log'] = self.get_property('log')

        if "Weight" in properties_dict:
            properties_dict["weights"] = properties_dict["Weight"]
            del properties_dict["Weight"]

        if "Bins" in properties_dict:
            properties_dict["bins"] = properties_dict["Bins"]
            del properties_dict["Bins"]

        if "X min" in properties_dict:
            if "X max" in properties_dict:
                properties_dict["range"] = [properties_dict["X min"], properties_dict["X max"]]
                del properties_dict["X max"]
            else:
                properties_dict["range"] = [properties_dict["X min"], max(np.array(properties_dict["X"]).flatten())]
            del properties_dict["X min"]

        elif "X max" in properties_dict:
            properties_dict["range"] = [min(np.array(properties_dict["X"]).flatten()), properties_dict["X max"]]
            del properties_dict["X max"]

        properties_dict['priority'] = int(self.priority_widget.get_value())

        self.set_output_property("Element", properties_dict)

        self.change_label("Information", "", True)




























class PltFigureNode(GenericNode):

    # unique node identifier.
    __identifier__ = 'Matplotlib'

    # initial default node name.
    NODE_NAME = 'Figure'

    def __init__(self):
        super(PltFigureNode, self).__init__()

        # create input & output ports
        self.add_custom_input('Input Plottable 1', PortValueType.DICT, multi_input=True)
        self.add_custom_input('Input Plottable 2', PortValueType.DICT, multi_input=True)
        
        self.add_custom_input('Title', PortValueType.STRING)
        
        self.add_custom_input('X_min', PortValueType.FLOAT)
        self.add_custom_input('X_max', PortValueType.FLOAT)
        
        self.add_custom_input('Y_min', PortValueType.FLOAT)
        self.add_custom_input('Y_max', PortValueType.FLOAT)
        
        self.add_custom_input('X label', PortValueType.STRING)
        self.add_custom_input('Y label 1', PortValueType.STRING)
        self.add_custom_input('Y label 2', PortValueType.STRING)
        
        self.add_custom_output('Figure', PortValueType.FIGURE)
        
        self.add_checkbox("x_log", text='X log scale')
        self.add_checkbox("y_log", text='Y log scale')
        self.add_checkbox("legend", text='Legend')
        self.add_checkbox("color_bar", text='Color bar')

        self.add_text_input("canvas_width", "Width", "6")
        self.add_text_input("canvas_height", "Height", "6")

        self.plot_widget = pltWidget(self.view, name="plot")
        self.create_property('Plot_Widget', None)

        self.view.add_widget(self.plot_widget)
        self.view.draw_node()

        self.plot_widget.update_plot()
        
        self.add_label("Information")
        
        self.property_to_update.append("x_log")
        self.property_to_update.append("y_log")
        self.property_to_update.append("legend")
        self.property_to_update.append("color_bar")
        self.property_to_update.append("canvas_height")
        self.property_to_update.append("canvas_width")

        self.update()

    def update_from_input(self):
        if not self.get_value_from_port("Input Plottable 1") == None or not self.get_value_from_port("Input Plottable 2") == None:

            if self.get_value_from_port("Input Plottable 1", multiple=True) == None:
                self.input_arrays_1 = None
            else:
                self.input_arrays_1 = [element.get_property() for element in self.get_value_from_port("Input Plottable 1", multiple=True)]
                
            if self.get_value_from_port("Input Plottable 2", multiple=True) == None:
                self.input_arrays_2 = None
            else:
                self.input_arrays_2 = [element.get_property() for element in self.get_value_from_port("Input Plottable 2", multiple=True)]

            plot_parameters = {"legend":self.get_property("legend"),
                                    "x_log":self.get_property("x_log"),
                                    "y_log":self.get_property("y_log"),
                                    "color_bar":self.get_property("color_bar")}
            
            plot_parameters["width"] = self.get_property("canvas_width")
            plot_parameters["height"] = self.get_property("canvas_height")

            for input_ in self.input_properties:
                if self.is_input_valid(input_)[0]:
                    plot_parameters[input_] = self.get_value_from_port(input_).get_property()


            print("Updating plot")
            self.plot_widget.update_plot_list(self.input_arrays_1, self.input_arrays_2, plot_parameters)

            self.set_output_property("Figure", PltContainer(self.plot_widget.canvas.fig,
                                                            self.plot_widget.canvas.canvas,
                                                            plot_parameters))

    def check_inputs(self):
        if not self.get_value_from_port("Input Plottable 1") == None:
            is_valid, message = self.is_input_valid("Input Plottable 1")

            self.set_property("is_valid", is_valid)

            if not is_valid:
                self.change_label("Information", message, True)

        if not self.get_value_from_port("Input Plottable 2") == None:
            
            is_valid, message = self.is_input_valid("Input Plottable 2")

            self.set_property("is_valid", is_valid)

            if not is_valid:
                self.change_label("Information", message, True)

        if self.get_value_from_port("Input Plottable 1") == None and self.get_value_from_port("Input Plottable 2") == None:
            self.set_property("is_valid", False)
            self.change_label("Information", "No input plottable given", True)

        if not is_float(self.get_property("canvas_height")):
            self.set_property("is_valid", False)
            self.change_label("Information", "Given height should be a float", True)

        if not is_float(self.get_property("canvas_width")):
            self.set_property("is_valid", False)
            self.change_label("Information", "Given width should be a float", True)



    def reset_outputs(self):
        super(PltFigureNode, self).reset_outputs()

        self.plot_widget.update_plot_list(None, None, {"legend": False, "x_log":False, "y_log":False, "color_bar":False})
        self.change_label("Information", "", False)



class SaveFigureNode(GenericNode):

    # unique node identifier.
    __identifier__ = 'Matplotlib'

    # initial default node name.
    NODE_NAME = 'Save Figure'

    def __init__(self):
        super(SaveFigureNode, self).__init__()

        # create input & output ports
        self.add_custom_input('Input Figure', PortValueType.FIGURE)

        self.add_custom_input('File name', PortValueType.STRING)

        self.add_text_input("canvas_dpi", "DPI", "100")
        
        self.add_label("Information")
        
        self.property_to_update.append("canvas_dpi")

        self.update()

    def update_from_input(self):
        print("Saving figure at path :", os.path.abspath(self.get_value_from_port("File name").get_property()))
        self.change_label("Information", "", False)

        figure = self.get_value_from_port("Input Figure").get_property().get_property("Figure")

        try:
            figure.savefig(os.path.abspath(self.get_value_from_port("File name").get_property()), dpi=int(self.get_property("canvas_dpi")))
        except Exception as e:
            self.change_label("Information", str(e), True)

    def check_inputs(self):

        is_valid_1, message_1 = self.is_input_valid("Input Figure")

        self.set_property("is_valid", is_valid_1)

        if not is_valid_1:
            self.change_label("Information", message_1, True)
            

        is_valid_1, message_1 = self.is_input_valid("File name")

        self.set_property("is_valid", self.get_property("is_valid") and is_valid_1)

        if not is_valid_1:
            self.change_label("Information", message_1, True)
        else:
            abs_path = os.path.dirname(os.path.abspath(self.get_value_from_port("File name").get_property()))

            if not os.path.isdir(abs_path):
                self.set_property("is_valid", False)
                self.change_label("Information", "Given path folder does not exist", True)

        if not is_float(self.get_property("canvas_dpi")):
            self.set_property("is_valid", False)
            self.change_label("Information", "Given DPI should be a float", True)
