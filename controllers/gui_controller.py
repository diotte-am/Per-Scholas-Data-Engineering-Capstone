import mysql.connector as dbconnect
from mysql.connector import Error
import my_secrets
import pandas as pd
from views import view

def run_gui():
    app = view()
    app.mainloop()

    # handles request from gui
    # communicates with db
    # sends data to view