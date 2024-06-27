import typing
import os
import json
from abc import ABC, abstractmethod
import schema
from TBL_NAME import TBL_NAME
from pyspark.sql import SparkSession
from pyspark.sql.types import StringType, DateType, IntegerType
import mysql.connector as dbconnect
from mysql.connector import Error
import my_secrets

class ETL(ABC):

    @abstractmethod
    def extract(self):
        pass

    @abstractmethod
    def transform(self):
        pass

    @abstractmethod
    def load(self):
        pass


class jsonETL(ETL):
    # constructor
    def __init__(self):
        super().__init__()
        self.filetype = "json"
        print("JSON loading!")

    def extract_JSON_files(self, filename: str) -> list[str]:
        """
        Returns all JSON objects in file appended to a single list

        Parameters:
            filename (str): The name of the file containing the JSON objects
        
        Returns:
            branch_list (list[str]): The list of json obects
        
        """
        branch_list = []
        with open(filename) as f:
            data = json.load(f)
        for i in data:
            branch_list.append(i)
        f.close()
        return branch_list


    def extract(self)-> dict[str]:
        """
        Returns a dictionary of JSON file names within the given directory

        Parameters: 
            directoryName (str): the name of a directory containing only JSON files

        Returns:
            parsed_list (list[str]): list of file names within the directory
        """
 
        parsed_dict = {}
        # iterate thru every json in the directory
        for filename in os.listdir(self.filetype):
            f = os.path.join(self.filetype, filename)
            if os.path.isfile(f):
                table_name = filename.split(".")[0].upper()
                # extract each JSON object in the given file
                parsed_dict[table_name] = self.extract_JSON_files(f)
            else:
                print("Unable to find", f)
        return parsed_dict
        

    def transform(self, parsed_dicts: dict[str]) -> dict[str]:
        """
        Applies transformations to each table depending on stored schema

        Parameters: 
            parsed_lists (dict[str]): a dictionary of lists, the key is the name of the eventual table

        Returns:
            df_dict (dict[str]):  a transformed dictionary of dataframes, the key is the name of the eventual table

        """
        # retreive current spark session
        spark = SparkSession.getActiveSession()
        df_dict = {}
  
        # apply schema to each DF
        for k,v in parsed_dicts.items():
            # convert to df and create temp view
            spark.createDataFrame(parsed_dicts[k]).createOrReplaceTempView(k)
            
            temp = spark.sql(schema.main[k])
            # save transformed DF
            df_dict[k] = temp

        # create another table for dates based on credit data
        spark.createDataFrame(
            parsed_dicts[TBL_NAME.CREDIT.value]).createOrReplaceTempView(TBL_NAME.PERIOD.value)
        temp = spark.sql(schema.main[TBL_NAME.PERIOD.value])
        df_dict[TBL_NAME.PERIOD.value] = temp

        print(df_dict)
        return df_dict
    
    def create_db(self):
        ''' Connect to MySQL database'''
        conn = None
        try: 
            conn = dbconnect.connect(host='localhost', user=my_secrets.username, password=my_secrets.password)

            if conn.is_connected():
                print('Connected to MySQL database')
                # Get a cursor
                cursor = conn.cursor()
                query = "CREATE DATABASE IF NOT EXISTS creditcard_capstone"
                cursor.execute(query)
                conn.close()
                
        except Error as e:
            print("Conection failed!", e)

    def load_FKs(self):
        ''' Connect to MySQL database'''
        conn = None
        try: 
            conn = dbconnect.connect(host='localhost', user=my_secrets.username, database='creditcard_capstone', password=my_secrets.password)

            if conn.is_connected():
                print('Connected to MySQL database')
                # Get a cursor
                cursor = conn.cursor()
                for k,v in schema.pk.items():
                    cursor.execute(v)
                
                for query in schema.fk:
                    cursor.execute(query)

                conn.close()
                
        except Error as e:
            print("Conection failed!", e)

    def load(self, data: dict[str]):
        
        # connect to db
        self.create_db()

        # iterate thru all dataframes and load them to the database as a table
        for k, df in data.items():
            df.write.format("jdbc") \
            .mode("append") \
            .option("url", "jdbc:mysql://localhost:3306/creditcard_capstone") \
            .option("dbtable", k) \
            .option("user", my_secrets.username) \
            .option("password", my_secrets.password) \
            .save()

        self.load_FKs()

    # create period table
    def run(self): 
        data = self.extract()
        data = self.transform(data)
        self.load(data)