import typing
import my_secrets
import mysql.connector as dbconnect
from mysql.connector import Error
from schemas.pk_schema import pk_schema  
from schemas.fk_schema import fk_schema

class load():
    def __init__(self, data):
        # connect to the database, save connection as object
        self.data = data
        self.create_db()

    def create_db(self):
        # connect to MySQL database
        conn = None
        try: 
            conn = dbconnect.connect(host='localhost', user=my_secrets.username, password=my_secrets.password)

            if conn.is_connected():
                print('Connected to MySQL database')
                # Get a cursor
                cursor = conn.cursor()
                query = "DROP DATABASE IF EXISTS creditcard_capstone"
                cursor.execute(query)
                query = "CREATE DATABASE IF NOT EXISTS creditcard_capstone"
                cursor.execute(query)
                conn.close()
                
        except Error as e:
            print("Conection failed!", e)

    def load(self):
        
        # connect to db
        self.create_db()

        # iterate thru all dataframes and load them to the database as a table
        for k, df in self.data.items():
            df.write.format("jdbc") \
            .mode("append") \
            .option("url", "jdbc:mysql://localhost:3306/creditcard_capstone") \
            .option("dbtable", k) \
            .option("user", my_secrets.username) \
            .option("password", my_secrets.password) \
            .save()
        self.load_FKs()

    def load_FKs(self):
        ''' Connect to MySQL database'''
        conn = None
        try: 
            conn = dbconnect.connect(host='localhost', user=my_secrets.username, database='creditcard_capstone', password=my_secrets.password)

            if conn.is_connected():
                # Get a cursor
                cursor = conn.cursor()
                for k,v in pk_schema.items():
                    cursor.execute(v)
                
                for query in fk_schema:
                    print(query)
                    cursor.execute(query)

                conn.close()
                
        except Error as e:
            print("Conection failed!", e)