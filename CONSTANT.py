import os


FILEPATH_DATI = "dati.json"

FOLDER_GRAPH = "plot"
PLOT_STRING_TITLE = "_price_plot.png"

if not os.path.exists(FOLDER_GRAPH):
    os.makedirs(FOLDER_GRAPH)
    print(f"Folder '{FOLDER_GRAPH}' created successfully.")
else:
    print(f"Folder '{FOLDER_GRAPH}' already exists.")



string_from_tcp_ID = "null"
path_here = os.getcwd()
path = path_here + "/data/"
bernardo_chat_id = "283149655"