#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import signal
import sys
from types import FrameType

from Qt import QtCore, QtWidgets

from NodeGraphQt import (
    NodeGraph,
    PropertiesBinWidget,
    NodesTreeWidget,
    NodesPaletteWidget
)

from NodesPostPro.nodes import input_nodes, \
                    tool_nodes, \
                    math_nodes, \
                    string_nodes, \
                    list_nodes, \
                    random_nodes, \
                    pandas_nodes, \
                    plt_node, \
                    cast_nodes, \
                    pickle_nodes, \
                    numpy_nodes, \
                    tripoli_nodes, \
                    iterator_nodes

def tracefunc(frame:FrameType, event:str, arg, indent=[0]):
    if event == "call":
        indent[0] += 2
        if "NodeGraphQt" in frame.f_code.co_filename:
            if "self" in frame.f_locals:
                try:
                    print("-",indent[0],"> call function", 
                    frame.f_code.co_name, 
                    "> NodeGraphQt"+frame.f_code.co_filename.split("NodeGraphQt")[-1], 
                    ">", frame.f_locals["self"].name)
                except:
                    pass

        

def main():

    # handle SIGINT to make the app terminate on CTRL+C
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

    app = QtWidgets.QApplication([])

    # create graph controller.
    graph = NodeGraph()

    # set up context menu for the node graph.

    file_path = os.path.dirname(os.path.realpath(__file__))
    hotkey_path = os.path.join(file_path,'hotkeys','hotkeys.json')
    current_path = os.getcwd()
    
    os.chdir(file_path)
    graph.set_context_menu_from_file(hotkey_path)
    os.chdir(current_path)

    # registered example nodes.
    graph.register_nodes([
        #   Input nodes
        input_nodes.InputFloatNode,
        input_nodes.InputIntegerNode,
        input_nodes.InputBooleanNode,
        input_nodes.InputStringNode,
        input_nodes.InputListNode,

        #   Tools nodes
        tool_nodes.PrintNode,

        #   Math nodes
        math_nodes.OneMathNode,
        math_nodes.TwoMathNode,
        math_nodes.TrigonometryNode,

        #   Math nodes
        string_nodes.ReplaceNode,

        #   Cast nodes
        cast_nodes.FloatToIntegerCastNode,
        cast_nodes.FloatToStringCastNode,
        cast_nodes.FloatToBooleanCastNode,
        
        cast_nodes.IntegerToFloatCastNode,
        cast_nodes.IntegerToStringCastNode,
        cast_nodes.IntegerToBooleanCastNode,
        
        cast_nodes.StringToIntegerCastNode,
        cast_nodes.StringToFloatCastNode,
        cast_nodes.StringToBooleanCastNode,
        
        cast_nodes.BooleanToIntegerCastNode,
        cast_nodes.BooleanToStringCastNode,
        cast_nodes.BooleanToFloatCastNode,
        
        cast_nodes.DataFrameToArrayCastNode,
        cast_nodes.ArrayToDataFrameCastNode,

        #   List operators,

        list_nodes.GetListElementNode,

        #   Iterators
        iterator_nodes.ExternalNode,
        iterator_nodes.InternalNode,
        iterator_nodes.InteratorListNode,

        #   Pandas nodes
        pandas_nodes.LoadFileNode,
        pandas_nodes.GetColumnNode,
        pandas_nodes.GetColumnSelectorNode,
        pandas_nodes.MultiplyNode,
        pandas_nodes.GetAverageNode,

        #   Numpy nodes
        numpy_nodes.SetAxisNode,
        numpy_nodes.NP_AddNode,
        numpy_nodes.NP_MultiplyFloatNode,
        numpy_nodes.NP_SqueezeNode,
        
        #   Matplotlib nodes
        plt_node.PltFigureNode,
        plt_node.PlotNode,
        plt_node.ScatterNode,
        plt_node.ImShowNode,
        plt_node.FillBetweenNode,
        plt_node.HistNode,
        plt_node.SaveFigureNode,
        plt_node.VerticalSplitNode,
        plt_node.HorizontalSplitNode,
        
        #   Pickle nodes
        pickle_nodes.LoadNumpyNode,
        pickle_nodes.LoadPandasNode,

        #   Tripoli outputs
        tripoli_nodes.TripoliExtendedMeshNode,


        #   Random nodes
        random_nodes.RandomUniformNode,
        random_nodes.RandomIntegerNode
        
    ])

    # show the node graph widget.
    graph_widget = graph.widget
    graph_widget.resize(1100, 800)
    graph_widget.show()

    for node in graph.all_nodes():
        node.set_to_update(True)
        node.update_values()


    # fit nodes to the viewer.
    graph.clear_selection()
    graph.fit_to_selection()

    # Custom builtin widgets from NodeGraphQt
    # ---------------------------------------

    # create a node properties bin widget.
    properties_bin = PropertiesBinWidget(node_graph=graph)
    properties_bin.setWindowFlags(QtCore.Qt.Tool)

    # example show the node properties bin widget when a node is double clicked.
    def display_properties_bin(node):
        if not properties_bin.isVisible():
            properties_bin.show()

    # wire function to "node_double_clicked" signal.
    graph.node_double_clicked.connect(display_properties_bin)

    # create a nodes tree widget.
    # nodes_tree = NodesTreeWidget(node_graph=graph)
    # nodes_tree.set_category_label('nodeGraphQt.nodes', 'Builtin Nodes')
    # nodes_tree.set_category_label('nodes.custom.ports', 'Custom Port Nodes')
    # nodes_tree.set_category_label('nodes.widget', 'Widget Nodes')
    # nodes_tree.set_category_label('nodes.basic', 'Basic Nodes')
    # nodes_tree.set_category_label('nodes.group', 'Group Nodes')
    # nodes_tree.show()

    # create a node palette widget.
    # nodes_palette = NodesPaletteWidget(node_graph=graph)
    # nodes_palette.set_category_label('nodeGraphQt.nodes', 'Builtin Nodes')
    # nodes_palette.set_category_label('nodes.custom.ports', 'Custom Port Nodes')
    # nodes_palette.set_category_label('nodes.widget', 'Widget Nodes')
    # nodes_palette.set_category_label('nodes.basic', 'Basic Nodes')
    # nodes_palette.set_category_label('nodes.group', 'Group Nodes')
    # nodes_palette.show()
    
    if "debug" in sys.argv:
        sys.setprofile(tracefunc)

    sys.gettrace()

    app.exec_()
