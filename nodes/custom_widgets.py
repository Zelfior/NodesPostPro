from NodeGraphQt import BaseNode, NodeBaseWidget
from enum import Enum
import pandas as pd
import numpy as np
from Qt import QtWidgets




"""






"""
class LabelWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, name=''):
        super(LabelWidget, self).__init__(parent)

        self.label_widget = QtWidgets.QLabel(name)

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(5, 0, 5, 0)
        layout.addWidget(self.label_widget)

    def get_value(self):
        return self.label_widget.text()

    def set_value(self, value):
        return self.label_widget.setText(value)
    
    def clear(self):
        self.label_widget.clear()
    
    def setText(self, label_value):
        self.label_widget.setText(label_value)
    
    def update(self):
        self.label_widget.update()



class InformationLabelWidget(NodeBaseWidget):
    def __init__(self, parent=None, name='', label = False):
        super(InformationLabelWidget, self).__init__(parent)

        # set the name for node property.
        self.set_name(name)

        # set the label above the widget.
        if label:
            self.set_label(name)

        self.label_widget = LabelWidget(name = name)

        self.set_custom_widget(self.label_widget)

    def get_value(self):
        return self.label_widget.get_value()

    def set_value(self, value):
        self.label_widget.clear()
        self.label_widget.setText(value)
        self.label_widget.update()
    
    def set_text(self, label_value, color):
        self.label_widget.clear()
        self.label_widget.setText(label_value)
        self.label_widget.setStyleSheet("color: "+color)
        self.label_widget.update()




"""






"""
class IntSelectorWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, name=''):
        super(IntSelectorWidget, self).__init__(parent)

        self.val_min = 0
        self.val_max = 0

        self.int_selector = QtWidgets.QSpinBox(self)
        self.int_selector.setRange(self.val_min, self.val_max)
        self.int_selector.setSingleStep(1)
        self.int_selector.setValue(0)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(15, 0, 15, 0)
        layout.addWidget(self.int_selector)


    def set_range(self, val_min, val_max):
        if self.get_value() > val_max:
            self.set_value(val_max)
        if self.get_value() < val_min:
            self.set_value(val_min)

        self.val_min = val_min
        self.val_max = val_max

        self.int_selector.setRange(val_min, val_max)

    def get_value(self):
        return self.int_selector.value()

    def get_range(self):
        return [self.val_min, self.val_max]

    def set_value(self, value):
        return self.int_selector.setValue(value)
    


class IntSelector_Widget(NodeBaseWidget):
    def __init__(self, parent=None, name='', label=''):
        super(IntSelector_Widget, self).__init__(parent)

        # set the name for node property.
        self.set_name(name)

        # set the label above the widget.
        self.set_label(label)

        self.int_selector_widget = IntSelectorWidget(name = name)

        self.int_selector_widget.int_selector.valueChanged.connect(self.on_value_changed)

        self.set_custom_widget(self.int_selector_widget)

    def get_value(self):
        return self.int_selector_widget.get_value()

    def get_range(self):
        return self.int_selector_widget.get_range()

    def set_range(self, val_min, val_max):
        return self.int_selector_widget.set_range(val_min, val_max)
        
    def set_value(self, value):
        return self.int_selector_widget.set_value(value)
    