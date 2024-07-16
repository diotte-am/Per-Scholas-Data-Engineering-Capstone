import pandas as pd
from views.app import app
from models.graph import graph

def run_gui():
    view = app()
    view.mainloop()

    


    # handles request from gui
    # communicates with db
    # sends data to view