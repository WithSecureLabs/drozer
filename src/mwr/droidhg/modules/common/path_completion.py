import os

def on_console(path):
    """
    Provides path completion, against files local to the Console.
    """

    folder, search_path = get_folder_and_search_path(path, os.path.sep)
    folders = os.listdir(folder)
    
    return get_suggestions(folder, search_path, folders, os.path.sep)

def on_agent(path):
    """
    Provides path completion, against files local to the Agent.
    """

    #folder, search_path = get_folder_and_search_path(path, "/")
    #folders = []
    #
    #return get_suggestions(folder, search_path, folders, "/")

    return []

def get_folder_and_search_path(path, sep):
    """
    Breakdown the search path, to determine the base folder and search string.
    """

    if path == "":
        path = "/"

    folder = path[:path.rfind(sep) + 1] if (path != sep) else sep
    search_path = path[path.rfind(sep) + 1:]

    return (folder, search_path)

def get_suggestions(folder, search_path, folders, sep):
    """
    Filter a list of folders with a given search path.
    """

    return [ (folder + p + sep) for p in folders if (p.startswith(search_path) and p != search_path and os.path.isdir(folder + p)) ]
    