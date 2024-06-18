import typing
import os
import json
from abc import ABC, abstractmethod
import schema_patterns
import TBL_NAME
from pyspark.sql import SparkSession

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
        dir = os.getcwd() + "/Per-Scholas-Data-Engineering-Capstone/"
        # set working directory
        os.chdir(dir)
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
            parsed_lists (dict[str]): a dictionary of dataframes, the key is the name of the eventual table

        Returns:
            df_dict (dict[str]):  a transformed dictionary of dataframes, the key is the name of the eventual table

        """
        spark = SparkSession.getActiveSession()
        df_dict = {}
        for name in parsed_dicts:
            df_dict[name] = spark.createDataFrame(parsed_dicts[name])

        for k,v in df_dict.items():
            print(k,v)
            df_dict[k].createOrReplaceTempView(k)
            temp = spark.sql(schema_patterns.pattern_dict[k])
            df_dict[k] = temp

        print(df_dict)

    def load(self):
        # connect to db
        pass
        print("load")

    def run(self):
        data = self.extract()
        self.transform(data)
        self.load()