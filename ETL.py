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

    def __init__(self):
        super().__init__()
        self.filetype = "json"
        print("JSON loading!")

    def append_JSON_obects(self, filename: str) -> list[str]:
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


    def extract(self):
        dir = os.getcwd() + "/Per-Scholas-Data-Engineering-Capstone/"
        os.chdir(dir)
        parsed_list = {}
        for filename in os.listdir(self.filetype):
            f = os.path.join(self.filetype, filename)
            if os.path.isfile(f):
                table_name = filename.split(".")[0].upper()
                parsed_list[table_name] = self.append_JSON_obects(f)
            else:
                print("Unable to find", f)

        print(parsed_list)
        return parsed_list
        

    def transform(self):
        # add factory pattern for transforms
        spark = SparkSession.getActiveSession()
        spark.stop()
        pass
        print("transform!")

    def load(self):
        # connect to db
        pass
        print("load")

    def run(self):
        self.extract()
        self.transform()
        self.load()