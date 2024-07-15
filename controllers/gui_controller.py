import mysql.connector as dbconnect
from mysql.connector import Error
import my_secrets
import pandas as pd
from views.app import app
from models.graph import graph

def run_gui():
    view = app()
    view.mainloop()

    


    # handles request from gui
    # communicates with db
    # sends data to view