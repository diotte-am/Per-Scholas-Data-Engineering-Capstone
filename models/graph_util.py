import mysql.connector as dbconnect
from mysql.connector import Error
from sqlalchemy import create_engine, Engine
import my_secrets
import pandas as pd
from schemas.graph_schema import GRAPH


class graph_util():
    def __init__(self) -> None:
        # connect to database
        self.engine: Engine = create_engine('mysql+mysqlconnector://' + my_secrets.username + ":" + my_secrets.password + "@localhost:3306/creditcard_capstone")
        
        

    def query(self, query: str):
        conn = self.engine.connect()
        if conn.connection:
            df = pd.read_sql(query, self.engine)
            
        return df
    
