import os
import NodesPostPro.hotkeys.save_load as save_load

def load_example(graph, example_file_name):
    file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "user_examples", example_file_name)
    
    if file_path:
        save_load.load_session(graph, file_path)

    graph.clear_selection()
    graph.fit_to_selection()

def first_user_example(graph):
    load_example(graph, "first_user_example.json")

