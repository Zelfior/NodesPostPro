#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import signal

from Qt import QtCore, QtWidgets

from NodeGraphQt import (
    NodeGraph,
    PropertiesBinWidget,
    NodesTreeWidget,
    NodesPaletteWidget
)

# import example nodes from the "example_nodes" package
from nodes import operation_nodes, read_file_nodes, get_column_nodes, plt_node, input_nodes, cast_nodes, pickle_nodes, numpy_nodes, tripoli_nodes

if __name__ == '__main__':

    # handle SIGINT to make the app terminate on CTRL+C
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

    app = QtWidgets.QApplication([])

    # create graph controller.
    graph = NodeGraph()

    # set up context menu for the node graph.
    graph.set_context_menu_from_file('hotkeys/hotkeys.json')

    # registered example nodes.
    graph.register_nodes([
        #   Input nodes
        input_nodes.InputFloatNode,
        input_nodes.InputIntegerNode,
        input_nodes.InputBooleanNode,
        input_nodes.InputStringNode,

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

        #   Operation nodes
        operation_nodes.MultiplyNode,
        operation_nodes.GetAverageNode,

        #   Pandas nodes
        read_file_nodes.LoadFileNode,
        get_column_nodes.GetColumnNode,

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
        
        #   Pickle nodes
        pickle_nodes.LoadNumpyNode,
        pickle_nodes.LoadPandasNode,

        #   Tripoli outputs
        tripoli_nodes.TripoliExtendedMeshNode
    ])

    # show the node graph widget.
    graph_widget = graph.widget
    graph_widget.resize(1100, 800)
    graph_widget.show()

    current_height = 0.

    """
    
        Exemple pandas/plot
    
    """
    # # create node with custom text color and disable it.
    read_file_node = graph.create_node('Pandas.LoadFileNode')#, text_color='#feab20')
    read_file_node.set_pos(-400,current_height)

    # # create node and set a custom icon.
    get_column_node = graph.create_node('Pandas.GetColumnNode')

    plot_node = graph.create_node('Matplotlib.PlotNode')
    plot_node.set_pos(400,current_height)

    plot_show_node = graph.create_node('Matplotlib.PltFigureNode')
    plot_show_node.set_pos(800,current_height)

    for node in graph.all_nodes():
        node.set_to_update(False)
    
    read_file_node.set_output(0, get_column_node.input(0))
    get_column_node.set_output(0, plot_node.input(1))
    plot_node.set_output(0, plot_show_node.input(0))
    


    """
    
        Exemple imshow
    
    """
    current_height += 800

    pickle_node = graph.create_node("Pickle.LoadNumpyNode")
    pickle_node.set_pos(-400,current_height)

    set_axis_1_node = graph.create_node("Numpy.SetAxisNode")
    set_axis_1_node.set_pos(0,current_height)
    
    imshow_node = graph.create_node('Matplotlib.ImShowNode')
    imshow_node.set_pos(400,current_height)

    plot_show_node_2 = graph.create_node('Matplotlib.PltFigureNode')
    plot_show_node_2.set_pos(800,current_height)

    for node in graph.all_nodes():
        node.set_to_update(False)

    pickle_node.set_output(0, set_axis_1_node.input(0))
    set_axis_1_node.axis_widget.set_value(1)
    set_axis_1_node.set_output(0, imshow_node.input(0))
    imshow_node.set_output(0, plot_show_node_2.input(0))
    plot_show_node_2.set_property("color_bar", True)


    """
    
        Exemple fill_between
    
    """
    current_height += 1000
    read_tripoli_node = graph.create_node("Tripoli.TripoliExtendedMeshNode")
    read_tripoli_node.set_pos(-800,current_height)

    squeeze_tripoli_node = graph.create_node("Numpy.NP_SqueezeNode")
    squeeze_tripoli_node.set_pos(-400,current_height)

    set_axis_2_1_node = graph.create_node("Numpy.SetAxisNode")
    set_axis_2_1_node.set_pos(0,current_height)

    fill_between_name = graph.create_node("Input.InputStringNode")
    fill_between_name.set_pos(0,current_height - 100)
    fill_between_name.set_property("Value", "Sigma")

    set_axis_2_2_node = graph.create_node("Numpy.SetAxisNode")
    set_axis_2_2_node.set_pos(0,current_height + 200)

    set_axis_2_3_node = graph.create_node("Numpy.SetAxisNode")
    set_axis_2_3_node.set_pos(0,current_height + 400)

    plot_name = graph.create_node("Input.InputStringNode")
    plot_name.set_pos(0,current_height + 550)
    plot_name.set_property("Value", "Value")

    alpha_value = graph.create_node("Input.InputFloatNode")
    alpha_value.set_pos(0,current_height - 200)
    alpha_value.set_property("Value", "0.2")
    
    fill_between_node = graph.create_node('Matplotlib.FillBetweenNode')
    fill_between_node.set_pos(400,current_height)
    
    plot_2_node = graph.create_node('Matplotlib.PlotNode')
    plot_2_node.set_pos(400,current_height+300)

    plot_show_node_3 = graph.create_node('Matplotlib.PltFigureNode')
    plot_show_node_3.set_pos(800,current_height)


    for node in graph.all_nodes():
        node.set_to_update(False)



    read_tripoli_node.set_output(0, squeeze_tripoli_node.input(0))

    squeeze_tripoli_node.set_output(0, set_axis_2_1_node.input(0))
    squeeze_tripoli_node.set_output(0, set_axis_2_2_node.input(0))
    squeeze_tripoli_node.set_output(0, set_axis_2_3_node.input(0))

    set_axis_2_1_node.value_widget.set_value(59)
    set_axis_2_2_node.value_widget.set_value(60)
    set_axis_2_3_node.value_widget.set_value(61)

    set_axis_2_1_node.set_output(0, fill_between_node.input(1))
    set_axis_2_2_node.set_output(0, plot_2_node.input(1))
    set_axis_2_3_node.set_output(0, fill_between_node.input(2))

    read_tripoli_node.set_output(7, fill_between_node.input(0))
    read_tripoli_node.set_output(7, plot_2_node.input(0))

    alpha_value.set_output(0, fill_between_node.input(6))
    plot_name.set_output(0, plot_2_node.input(2))
    fill_between_name.set_output(0, fill_between_node.input(4))

    plot_show_node_3.set_property("legend", True)


    fill_between_node.set_output(0, plot_show_node_3.input(0))
    plot_2_node.set_output(0, plot_show_node_3.input(0))


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

    app.exec_()