from NodeGraphQt import NodeBaseWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from Qt import QtWidgets

import pandas as pd
import numpy as np

from nodes.generic_node import GenericNode, PortValueType, check_type
from nodes.custom_widgets import IntSelector_Widget

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
        self.set_name('Plot_Widget')

        # set the label above the widget.
        # self.set_label('Custom Widget')

        self.canvas = PltCanvasWidget()
        # set the custom widget.
        self.set_custom_widget(self.canvas)

        self.input_arrays = []

        self.plot_parameters= {"legend": False, "x_log":False, "y_log":False, "color_bar":False}

        self.title = ""

    def sort_by_priority(self, array):
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


    def update_plot(self, legend = False):
        self.canvas.fig.clear()  # clear the axes content
        self.canvas.axes = self.canvas.fig.add_subplot(111)
        # self.canvas.fig.gca().set_aspect(1.)

        self.input_arrays = self.sort_by_priority(self.input_arrays)

        mappables= []

        for element in self.input_arrays:
            if element['element_type'] == "plot":
                kwargs_dict = {key:element[key] for key in element if key not in ["X", "Y", "element_type", "priority"]}
                self.canvas.axes.plot(element['X'], element['Y'], **kwargs_dict)
                
            if element['element_type'] == "fill_between":
                kwargs_dict = {key:element[key] for key in element if key not in ["X", "Y1", "Y2", "element_type", "priority"]}
                self.canvas.axes.fill_between(element['X'], element['Y1'], element['Y2'], **kwargs_dict)
                
            elif element['element_type'] == "imshow":
                kwargs_dict = {key:element[key] for key in element if key not in ["X", "Y", "element_type", "priority"]}
                kwargs_dict["aspect"] = "auto"
                mappables.append(self.canvas.axes.imshow(element['Y'], **kwargs_dict))

            elif element['element_type'] == "scatter":
                kwargs_dict = {key:element[key] for key in element if key not in ["X", "Y", "element_type", "Color", "Color array", "priority"]}

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

        print([[element, self.plot_parameters[element]] for element in self.plot_parameters if not type(self.plot_parameters[element]) == dict])

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



        if self.plot_parameters["legend"]:
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

        self.canvas.canvas.draw()  # actually draw the new content



    def update_plot_list(self, array, plot_parameters):
        self.input_arrays = array
        self.plot_parameters = plot_parameters

        self.update_plot()



    def get_value(self):
        # widget = self.get_custom_widget()
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

        print(properties_dict.keys())












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



















class PltFigureNode(GenericNode):

    # unique node identifier.
    __identifier__ = 'Matplotlib'

    # initial default node name.
    NODE_NAME = 'Figure'

    def __init__(self):
        super(PltFigureNode, self).__init__()

        # create input & output ports
        self.add_custom_input('Input Plottable', PortValueType.DICT, multi_input=True)
        
        self.add_custom_input('Title', PortValueType.STRING)
        
        self.add_custom_input('X_min', PortValueType.FLOAT)
        self.add_custom_input('X_max', PortValueType.FLOAT)
        
        self.add_custom_input('Y_min', PortValueType.FLOAT)
        self.add_custom_input('Y_max', PortValueType.FLOAT)
        
        self.add_custom_output('Figure', PortValueType.FIGURE)
        
        self.add_checkbox("x_log", text='X log scale')
        self.add_checkbox("y_log", text='Y log scale')
        self.add_checkbox("legend", text='Legend')
        self.add_checkbox("color_bar", text='Color bar')

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

    def update_from_input(self):
        if not self.get_value_from_port("Input Plottable") == None:
            self.input_arrays = [element.get_property() for element in self.get_value_from_port("Input Plottable", multiple=True)]

            plot_parameters = {"legend":self.get_property("legend"),
                                    "x_log":self.get_property("x_log"),
                                    "y_log":self.get_property("y_log"),
                                    "color_bar":self.get_property("color_bar")}

            for input_ in self.input_properties:
                if self.is_input_valid(input_)[0]:
                    plot_parameters[input_] = self.get_value_from_port(input_).get_property()


            self.plot_widget.update_plot_list(self.input_arrays, plot_parameters)


    def check_inputs(self):
        is_valid, message = self.is_input_valid("Input Plottable")

        self.set_property("is_valid", is_valid)

        if not is_valid:
            self.change_label("Information", message, True)



    def reset_outputs(self):
        super(PltFigureNode, self).reset_outputs()

        self.plot_widget.update_plot_list([], {"legend": False, "x_log":False, "y_log":False, "color_bar":False})
        self.change_label("Information", "", False)

