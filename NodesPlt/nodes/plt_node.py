from NodeGraphQt import NodeBaseWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from Qt import QtWidgets

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

from nodes.generic_node import GenericNode, PortValueType

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

        self.to_plot = []

        self.title = ""

    def update_plot(self):
        self.canvas.axes.cla()  # clear the axes content

        for element in self.to_plot:
            if element['type'] == "plot":
                self.canvas.axes.plot(element['x'], element['y'])

        if not self.title == "":
            self.canvas.title = self.title

        self.canvas.canvas.draw()  # actually draw the new content

    def update_plot_list(self, array):
        self.to_plot = array

        self.update_plot()



    def get_value(self):
        widget = self.get_custom_widget()
        return ''














class PltNode(GenericNode):

    # unique node identifier.
    __identifier__ = 'Matplotlib'

    # initial default node name.
    NODE_NAME = 'plot input array'

    def __init__(self):
        super(PltNode, self).__init__()

        # create input & output ports
        self.add_custom_input('Input Array', PortValueType.PD_DATAFRAME, multi_input=True)
        
        self.add_custom_input('Title', PortValueType.STRING)
        
        self.add_custom_input('X_min', PortValueType.FLOAT)
        self.add_custom_input('X_max', PortValueType.FLOAT)
        
        self.add_custom_input('Y_min', PortValueType.FLOAT)
        self.add_custom_input('Y_max', PortValueType.FLOAT)
        
        self.add_checkbox("x_log", text='X log scale')
        self.add_checkbox("y_log", text='Y log scale')

        self.plot_widget = pltWidget(self.view, name="plot")

        self.view.add_widget(self.plot_widget)
        self.view.draw_node()

        self.plot_widget.update_plot()
        
        self.add_label("Information")

    def update_from_input(self):
        if not self.get_value_from_port("Input Array") == None:
            self.input_array = self.get_value_from_port("Input Array").get_property()

            self.plot_widget.update_plot_list([{'type':"plot", 'x':list(range(len(self.input_array))), 'y':self.input_array}])



    def check_inputs(self):
        input_given = self.get_value_from_port("Input Array")
        
        self.set_property("is_valid", input_given is not None \
                                            and input_given.is_defined() \
                                                and input_given.get_property_type() == PortValueType.PD_DATAFRAME)

    def reset_outputs(self):
        super(PltNode, self).reset_outputs()

        self.plot_widget.update_plot_list([])

