from NodeGraphQt import BaseNode, BaseNodeCircle
from functools import wraps

import pandas as pd
import os

def _log_method(val):
    @wraps(val)
    def wrapper(*a, **ka):
        print(val.__name__, 'is called')
        val(*a, **ka)
    return wrapper

class LogMethodCalls(type):
    def __new__(cls, cls_name, bases, attrs):
        for name, attr in attrs.items():
            if callable(attr):
                attrs[name] = _log_method(attr)
            elif isinstance(attr, (classmethod, staticmethod)):
                attrs[name] = type(attr)(_log_method(attr.__func__))
        return type.__new__(cls, cls_name, bases, attrs)

# class Foo(metaclass=LogMethodCalls):
#     def my_method(self):
#         pass

class LoadFileNode(BaseNode):
    """
    An example of a node with a embedded QLineEdit.
    """

    # unique node identifier.
    __identifier__ = 'nodes.Pandas'

    # initial default node name.
    NODE_NAME = 'Read CSV file'

    def __init__(self):
        super(LoadFileNode, self).__init__()

        # create input & output ports
        self.add_output('Output DataFrame', color=(0, 0, 255))

        self.output_data_frame = None
        self.has_loaded_data_frame = False

        # create QLineEdit text input widget.
        self.add_text_input('Filename', 'File name', tab='widgets')

    def update_model(self):
        super(LoadFileNode, self).update_model()

        print("update_model")
    
    def update(self):
        super(LoadFileNode, self).update()

        print("update")

    def set_model(self, model):
        super(LoadFileNode, self).set_model()

        print("set_model")

    def set_property(self, name, value, push_undo=True):
        super(LoadFileNode, self).set_property(name, value, push_undo=push_undo)

        self.given_path = self.get_property(name)

        self.update_from_input()


        # F:/Documents/NodeEditor/NodeGraphQt-master/test.csv

        print("Set property called")
        

    def update_from_input(self):

        if os.path.isfile(self.given_path):
            self.output_data_frame = pd.read_csv(self.given_path, sep = ",")

            print(self.output_data_frame.columns)

            print(self.get_output('Output Array'))

            self.has_loaded_data_frame = True

        else:
            self.output_data_frame = None
            self.has_loaded_data_frame = False


        for output_id in range(len(self.outputs())):
            for connected_id in range(len(self.output(output_id).connected_ports())):
                self.output(output_id).connected_ports()[connected_id].node().update_from_input()