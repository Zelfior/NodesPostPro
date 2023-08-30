from NodeGraphQt import BaseNode, NodeBaseWidget
from enum import Enum
import pandas as pd
import numpy as np
from Qt import QtWidgets, QtCore





"""






"""
class LabelWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, name=''):
        super(LabelWidget, self).__init__(parent)

        self.label_widget = QtWidgets.QLabel(name)
        self.label_widget.setAlignment(QtCore.Qt.AlignCenter)
        # self.label_widget.setWordWrap(True)   #   Cuts the text at the widget size

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.layout.setContentsMargins(5, 0, 5, 0)
        self.layout.addWidget(self.label_widget)

    def get_value(self):
        return self.label_widget.text()

    def set_value(self, value):
        return self.label_widget.setText(str(value))
    
    def clear(self):
        self.label_widget.clear()
    
    def setText(self, label_value):
        self.label_widget.setText(str(label_value))
    
    def update(self):
        self.label_widget.update()

    def set_visible(self, visible):
        self.label_widget.setVisible(visible)



class InputLabelWidget(NodeBaseWidget):
    def __init__(self, parent=None, name='', label = False):
        super(InputLabelWidget, self).__init__(parent)

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

    def boundingRect(self):
        self.label_widget.adjustSize()

        bounding_rect = super().boundingRect()
        
        bounding_rect.setWidth(self.label_widget.width() + 5)
        bounding_rect.setHeight(self.label_widget.height() + 5)

        return bounding_rect


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
    











    
"""






"""
class ButtonWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, name=''):
        super(ButtonWidget, self).__init__(parent)

        self.button_widget = QtWidgets.QPushButton(name)

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(5, 0, 5, 0)
        layout.addWidget(self.button_widget)

    def get_value(self):
        return True

    def set_value(self, value):
        pass
    

class ButtonNodeWidget(NodeBaseWidget):
    def __init__(self, parent=None, name='', label = False):
        super(ButtonNodeWidget, self).__init__(parent)

        # set the name for node property.
        self.set_name(name)

        # set the label above the widget.
        if label:
            self.set_label(name)

        self.button_widget = ButtonWidget(name = name)

        self.set_custom_widget(self.button_widget)

    def get_value(self):
        return True

    def set_value(self, value):
        pass
    
    def set_link(self, function):
        self.button_widget.button_widget.clicked.connect(function)



        
"""






"""
class TableWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, name=''):
        super(TableWidget, self).__init__(parent)

        self.table_widget = QtWidgets.QTableWidget(5, 1)

        layout = QtWidgets.QHBoxLayout(self)
        layout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        layout.setContentsMargins(5, 0, 5, 0)
        layout.addWidget(self.table_widget)

        self.finished = True

    def get_value(self):
        output = []

        for i in range(self.table_widget.rowCount()):
            if not self.table_widget.item(i, 0) == None:
                output.append(self.table_widget.item(i, 0).text())
                
        return output

    def set_value(self, value):
        print("value to set in table", value)
        if type(value) == list:
            self.finished = False
            for i in range(len(value)):
                if i < self.table_widget.rowCount():
                    if i == len(value) - 1:
                        self.finished = True
                    self.table_widget.setItem(i, 0, QtWidgets.QTableWidgetItem(value[i]))
        else:
            self.table_widget.setItem(0, 0, QtWidgets.QTableWidgetItem(value))

        return
    
    def clear(self):
        self.table_widget.clear()
    
    def update(self):
        self.table_widget.update()

    def set_visible(self, visible):
        self.table_widget.setVisible(visible)

    def set_length(self, count):
        self.table_widget.setRowCount(count)



class InputTableWidget(NodeBaseWidget):
    def __init__(self, parent=None, name='', label = False):
        super(InputTableWidget, self).__init__(parent)

        # set the name for node property.
        self.set_name(name)

        # set the label above the widget.
        if label:
            self.set_label(name)

        self.table_widget = TableWidget(name = name)

        self.set_custom_widget(self.table_widget)

    def get_value(self):
        return self.table_widget.get_value()

    def set_value(self, value):
        print(value, self.get_value())
        if value != self.get_value():
            # self.table_widget.clear()
            self.table_widget.set_value(value)
            self.table_widget.update()
    
    def set_length(self, value):
        self.table_widget.set_length(value)









"""






"""
class IntSliderWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, name=''):
        super(IntSliderWidget, self).__init__(parent)

        self.val_min = 0
        self.val_max = 50

        from PySide2.QtCore import Qt

        self.int_slider = QtWidgets.QSlider(Qt.Horizontal, self)
        self.int_slider.setRange(self.val_min, self.val_max)
        self.int_slider.setSingleStep(1)
        self.int_slider.setValue(0)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(15, 0, 15, 0)
        layout.addWidget(self.int_slider)


    def set_range(self, val_min, val_max):
        if self.get_value() > val_max:
            self.set_value(val_max)
        if self.get_value() < val_min:
            self.set_value(val_min)

        self.val_min = val_min
        self.val_max = val_max

        self.int_slider.setRange(val_min, val_max)

    def get_value(self):
        return self.int_slider.value()

    def get_range(self):
        return [self.val_min, self.val_max]

    def set_value(self, value):
        return self.int_slider.setValue(value)
    


class IntSlider_Widget(NodeBaseWidget):
    def __init__(self, parent=None, name='', label=''):
        super(IntSlider_Widget, self).__init__(parent)

        # set the name for node property.
        self.set_name(name)

        # set the label above the widget.
        self.set_label(label)

        self.int_slider_widget = IntSliderWidget(name = name)

        self.int_slider_widget.int_slider.valueChanged.connect(self.on_value_changed)

        self.set_custom_widget(self.int_slider_widget)

    def get_value(self):
        return self.int_slider_widget.get_value()

    def get_range(self):
        return self.int_slider_widget.get_range()

    def set_range(self, val_min, val_max):
        return self.int_slider_widget.set_range(val_min, val_max)
        
    def set_value(self, value):
        return self.int_slider_widget.set_value(value)
    
