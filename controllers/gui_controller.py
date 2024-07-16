import pandas as pd
from views.app import app
from models.graph_util import graph_util
import typing

def run_gui() -> None :
    view : app = app()
    view.mainloop()

    


    # handles request from gui
    # communicates with db
    # sends data to view