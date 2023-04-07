from NodeGraphQt import BaseNode, BaseNodeCircle, NodeBaseWidget
from functools import wraps
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from NodeGraphQt.constants import NodePropWidgetEnum, PortTypeEnum
from Qt import QtCore, QtWidgets

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os


class PltCanvasWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(PltCanvasWidget, self).__init__(parent)
        self.fig = Figure(figsize=(5, 5), dpi=100)
        self.canvas = FigureCanvasQTAgg(self.fig)
        self.axes = self.fig.add_subplot(111)

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.canvas)





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

    def update_plot(self):
        self.canvas.axes.cla()  # clear the axes content

        for element in self.to_plot:
            if element['type'] == "plot":
                self.canvas.axes.plot(element['x'], element['y'])

        self.canvas.canvas.draw()  # actually draw the new content

    def update_plot_list(self, array):
        self.to_plot = array

        self.update_plot()



    def get_value(self):
        widget = self.get_custom_widget()
        return ''














class PltNode(BaseNode):

    # unique node identifier.
    __identifier__ = 'Matplotlib'

    # initial default node name.
    NODE_NAME = 'plot input array'

    def __init__(self):
        super(PltNode, self).__init__()

        # create input & output ports
        self.add_input('Input Array', color=(0, 255, 0))

        self.input_array = None

        self.plot_widget = pltWidget(self.view, name="plot")
        self.view.add_widget(self.plot_widget)
        #: redraw node to address calls outside the "__init__" func.
        self.view.draw_node()

        self.plot_widget.update_plot()

        # print(self.model.properties.keys())
        # print("view", self.view)

    # def set_property(self, name, value, push_undo=True):
    #     super(PltNode, self).set_property(name, value, push_undo=push_undo)
        
    def on_input_connected(self, in_port, out_port):
        super(PltNode, self).on_input_connected(in_port, out_port)

        self.plugged_input_port = out_port

        self.update_from_input()

        print("on_input_connected", in_port, out_port, self._model.name)
        

    def on_input_disconnected(self, in_port, out_port):
        super(PltNode, self).on_input_disconnected(in_port, out_port)

        print("on_input_disconnected", in_port, out_port, self._model.name)

    def update_from_input(self):
        if self.plugged_input_port == None:
            pass
        else:
            if self.plugged_input_port.node().is_defined:
                self.is_defined = True
                self.input_array = self.plugged_input_port.node().output_array

                self.plot_widget.update_plot_list([{'type':"plot", 'x':list(range(len(self.input_array))), 'y':self.input_array}])


        for output_id in range(len(self.outputs())):
            for connected_id in range(len(self.output(output_id).connected_ports())):
                self.output(output_id).connected_ports()[connected_id].node().update_from_input()