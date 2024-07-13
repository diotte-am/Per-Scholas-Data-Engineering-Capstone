import mysql.connector as dbconnect
from mysql.connector import Error
from sqlalchemy import create_engine
import my_secrets
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

class Graph():
    def __init__(self):
        conn = dbconnect.connect(host='localhost', user=my_secrets.username, database='creditcard_capstone', password=my_secrets.password)
        engine = create_engine('mysql+mysqlconnector://' + my_secrets.username + ":" + my_secrets.password + "@localhost:3306/creditcard_capstone")
        self.conn = engine.connect() 

    
    def create_viz(self):
        query = "SELECT COUNT(TRANSACTION_ID) AS TOTAL,\
        TRANSACTION_TYPE FROM CDW_SAPP_CREDIT\
        GROUP BY TRANSACTION_TYPE\
        ORDER BY TOTAL DESC"
        if self.conn.connection:
            df = pd.read_sql(query, self.conn)
        
        sns.barplot(data=df, x='TRANSACTION_TYPE', y="TOTAL", hue='TRANSACTION_TYPE')
        plt.xlabel("Type of Transaction")
        plt.ylabel("Total Transactions")
        plt.title("What is the Most Common Transaction Type?")
        return 