#!/usr/bin/python

# ------------------------------------------------------------------------------
# menu command functions
# ------------------------------------------------------------------------------

import os
import NodesPostPro.hotkeys.save_load as save_load
from NodeGraphQt.base.graph import NodeGraph
from NodeGraphQt.base.menu import NodeGraphMenu, NodesMenu
from Qt import QtGui, QtCore
from distutils.version import LooseVersion
import json


def zoom_in(graph):
    """
    Set the node graph to zoom in by 0.1
    """
    zoom = graph.get_zoom() + 0.1
    graph.set_zoom(zoom)


def zoom_out(graph):
    """
    Set the node graph to zoom in by 0.1
    """
    zoom = graph.get_zoom() - 0.2
    graph.set_zoom(zoom)


def reset_zoom(graph):
    """
    Reset zoom level.
    """
    graph.reset_zoom()


def layout_h_mode(graph):
    """
    Set node graph layout direction to horizontal.
    """
    graph.set_layout_direction(0)


def layout_v_mode(graph):
    """
    Set node graph layout direction to vertical.
    """
    graph.set_layout_direction(1)


def open_session(graph):
    """
    Prompts a file open dialog to load a session.
    """
    current = graph.current_session()
    file_path = graph.load_dialog(current)
    if file_path:
        save_load.load_session(graph, file_path)


def import_session(graph):
    """
    Prompts a file open dialog to load a session.
    """
    current = graph.current_session()
    file_path = graph.load_dialog(current)
    if file_path:
        save_load.import_session(graph, file_path)


def save_session(graph):
    """
    Prompts a file save dialog to serialize a session if required.
    """
    current = graph.current_session()
    if current:
        save_load.save_session(graph, current)
        msg = 'Session layout saved:\n{}'.format(current)
        viewer = graph.viewer()
        viewer.message_dialog(msg, title='Session Saved')
    else:
        save_session_as(graph)


def save_session_as(graph, folder_path = ""):
    """
    Prompts a file save dialog to serialize a session.
    """
    current = graph.current_session()

    if folder_path=="":
        file_path = graph.save_dialog(current)
    else:
        file_path = graph.save_dialog(current_dir = folder_path)

    if file_path:
        save_load.save_session(graph, file_path)


def new_session(graph):
    """
    Prompts a warning dialog to new a node graph session.
    """
    if graph.question_dialog('Clear Current Session?', 'Clear Session'):
        graph.clear_session()


def clear_undo(graph):
    """
    Prompts a warning dialog to clear undo.
    """
    viewer = graph.viewer()
    msg = 'Clear all undo history, Are you sure?'
    if viewer.question_dialog('Clear Undo History', msg):
        graph.clear_undo_stack()


def copy_nodes(graph):
    """
    Copy nodes to the clipboard.
    """
    graph.copy_nodes()


def cut_nodes(graph):
    """
    Cut nodes to the clip board.
    """
    graph.cut_nodes()


def paste_nodes(graph):
    """
    Pastes nodes copied from the clipboard.
    """
    graph.paste_nodes()


def delete_nodes(graph):
    """
    Delete selected node.
    """
    graph.delete_nodes(graph.selected_nodes())


def select_all_nodes(graph):
    """
    Select all nodes.
    """
    graph.select_all()


def clear_node_selection(graph):
    """
    Clear node selection.
    """
    graph.clear_selection()


def disable_nodes(graph):
    """
    Toggle disable on selected nodes.
    """
    graph.disable_nodes(graph.selected_nodes())


def duplicate_nodes(graph):
    """
    Duplicated selected nodes.
    """
    graph.duplicate_nodes(graph.selected_nodes())


def expand_group_node(graph):
    """
    Expand selected group node.
    """
    selected_nodes = graph.selected_nodes()
    if not selected_nodes:
        graph.message_dialog('Please select a "GroupNode" to expand.')
        return
    graph.expand_group_node(selected_nodes[0])


def fit_to_selection(graph):
    """
    Sets the zoom level to fit selected nodes.
    """
    graph.fit_to_selection()


def show_undo_view(graph):
    """
    Show the undo list widget.
    """
    graph.undo_view.show()


def curved_pipe(graph):
    """
    Set node graph pipes layout as curved.
    """
    from NodeGraphQt.constants import PipeLayoutEnum
    graph.set_pipe_style(PipeLayoutEnum.CURVED.value)


def straight_pipe(graph):
    """
    Set node graph pipes layout as straight.
    """
    from NodeGraphQt.constants import PipeLayoutEnum
    graph.set_pipe_style(PipeLayoutEnum.STRAIGHT.value)


def angle_pipe(graph):
    """
    Set node graph pipes layout as angled.
    """
    from NodeGraphQt.constants import PipeLayoutEnum
    graph.set_pipe_style(PipeLayoutEnum.ANGLE.value)


def bg_grid_none(graph):
    """
    Turn off the background patterns.
    """
    from NodeGraphQt.constants import ViewerEnum
    graph.set_grid_mode(ViewerEnum.GRID_DISPLAY_NONE.value)


def bg_grid_dots(graph):
    """
    Set background node graph background with grid dots.
    """
    from NodeGraphQt.constants import ViewerEnum
    graph.set_grid_mode(ViewerEnum.GRID_DISPLAY_DOTS.value)


def bg_grid_lines(graph):
    """
    Set background node graph background with grid lines.
    """
    from NodeGraphQt.constants import ViewerEnum
    graph.set_grid_mode(ViewerEnum.GRID_DISPLAY_LINES.value)


def layout_graph_down(graph):
    """
    Auto layout the nodes down stream.
    """
    nodes = graph.selected_nodes() or graph.all_nodes()
    graph.auto_layout_nodes(nodes=nodes, down_stream=True)


def layout_graph_up(graph):
    """
    Auto layout the nodes up stream.
    """
    nodes = graph.selected_nodes() or graph.all_nodes()
    graph.auto_layout_nodes(nodes=nodes, down_stream=False)


def toggle_node_search(graph):
    """
    show/hide the node search widget.
    """
    graph.toggle_node_search()

def load_example(graph, example_file_name):
    file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "examples", example_file_name)
    
    if file_path:
        save_load.load_session(graph, file_path)

    graph.clear_selection()
    graph.fit_to_selection()


def load_read_csv(graph):
    load_example(graph, "read_csv.json")

def pickle_imshow_savefig(graph):
    load_example(graph, "pickle_imshow_save.json")

def tripoli_fill_between(graph):
    load_example(graph, "tripoli_fill_between.json")
    
def internal_iterator_random(graph):
    load_example(graph, "internal_iterator_random.json")

def internal_column_plot(graph):
    load_example(graph, "interator_column_plot.json")

def iterator_random_hist(graph):
    load_example(graph, "iterator_random_hist.json")

def external_iterator_column_plot(graph):
    load_example(graph, "external_iterator_column_plot.json")

def multi_plot(graph):
    load_example(graph, "multi_plot.json")

def iterator_filter(graph):
    load_example(graph, "iterator_filter.json")

def color_maps(graph):
    load_example(graph, "color_maps.json")

def read_json(file_path):
    with open(file_path, 'r') as openfile:
        return json.load(openfile)
    return

def write_json(data, file_path):
    json_object = json.dumps(data, indent=4)
    
    # Writing to sample.json
    with open(file_path, "w+") as outfile:
        outfile.write(json_object)


def reload_user_examples(graph:NodeGraph):
    
    file_path = os.path.dirname(os.path.realpath(__file__))
    hotkey_path = str(os.path.join(file_path, 'hotkeys.json'))

    current_json_data = read_json(hotkey_path)
    index_user_examples = 0

    while not "label" in current_json_data[index_user_examples] or not "User examples" in current_json_data[index_user_examples]["label"]:
        index_user_examples+=1

    while not current_json_data[index_user_examples]["items"][0] == {"type":"separator"}:
        del current_json_data[index_user_examples]["items"][0]

    file_list = os.listdir(os.path.join(file_path, "..", "user_examples"))

    for element in file_list:
        if element.endswith(".json"):
            
            json_entry = {
                            "type":"command",
                            "label":element.replace(".json", "").replace("_", " "),
                            "file":"hotkeys/user_custom_functions.py",
                            "function_name":element.replace(".json", "").lower().replace(" ", "_")
                        }

            current_json_data[index_user_examples]["items"].insert(0, json_entry)

    write_json(current_json_data, hotkey_path)

    
    user_custom_functions_path = str(os.path.join(file_path, 'user_custom_functions.py'))
    user_custom_file = open(user_custom_functions_path, "w+")
    
    user_custom_file.write("import os\n")
    user_custom_file.write("import NodesPostPro.hotkeys.save_load as save_load\n")
    user_custom_file.write("\n")
    user_custom_file.write("def load_example(graph, example_file_name):\n")
    user_custom_file.write("    file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), \"user_examples\", example_file_name)\n")
    user_custom_file.write("    \n")
    user_custom_file.write("    if file_path:\n")
    user_custom_file.write("        save_load.load_session(graph, file_path)\n")
    user_custom_file.write("\n")
    user_custom_file.write("    graph.clear_selection()\n")
    user_custom_file.write("    graph.fit_to_selection()\n")
    user_custom_file.write("\n")

    for element in file_list: 
        user_custom_file.write("def "+element.replace(".json", "").lower().replace(" ", "_")+"(graph):\n")
        user_custom_file.write("    load_example(graph, \""+element+"\")\n\n")

    user_custom_file.close()

    menus = graph._viewer.context_menus()
    new_menu = NodeGraphMenu(graph, menus['graph'])
    
    new_menu.qmenu.clear()
    
    undo_action = graph.undo_stack().createUndoAction(graph._viewer, '&Undo')
    redo_action = graph.undo_stack().createRedoAction(graph._viewer, '&Redo')

    undo_action.setShortcuts(QtGui.QKeySequence.Undo)
    redo_action.setShortcuts(QtGui.QKeySequence.Redo)

    if LooseVersion(QtCore.qVersion()) >= LooseVersion('5.10'):
        undo_action.setShortcutVisibleInContextMenu(True)
        redo_action.setShortcutVisibleInContextMenu(True)

    new_menu.qmenu.addAction(undo_action)
    new_menu.qmenu.addAction(redo_action)
    new_menu.qmenu.addSeparator()

    graph._context_menu['graph'] = new_menu
    
    
    current_path = os.getcwd()
    
    os.chdir(os.path.join(file_path, '..'))
    graph.set_context_menu_from_file(hotkey_path)
    os.chdir(current_path)
    
def add_user_example(graph):
    save_session_as(graph, folder_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "user_examples"))

    reload_user_examples(graph)

def open_user_example_folder(graph):
    folder_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "user_examples")
    os.startfile(folder_path)