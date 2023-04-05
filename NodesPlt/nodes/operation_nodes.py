from NodeGraphQt import BaseNode


class DropdownMenuNode(BaseNode):
    """
    An example node with a embedded added QCombobox menu.
    """

    # unique node identifier.
    __identifier__ = 'nodes.widget'

    # initial default node name.
    NODE_NAME = 'menu'

    def __init__(self):
        super(DropdownMenuNode, self).__init__()

        # create input & output ports
        self.add_input('in 1')
        self.add_output('out 1')
        self.add_output('out 2')

        # create the QComboBox menu.
        items = ['item 1', 'item 2', 'item 3']
        self.add_combo_menu('my_menu', 'Menu Test', items=items)


class MultiplyNode(BaseNode):
    """
    A node class with 2 inputs and 2 outputs.
    """

    # unique node identifier.
    __identifier__ = 'nodes.multiply'

    # initial default node name.
    NODE_NAME = 'node Multiply'

    def __init__(self):
        super(MultiplyNode, self).__init__()

        # create node inputs.
        self.add_input('Input Array')

        # create node outputs.
        self.add_output('Output Array')
        
        self.add_text_input('Value', 'Value', tab='widgets')

