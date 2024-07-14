import typing
from pyspark.sql import SparkSession
from pyspark.sql.types import StringType, DateType, IntegerType
from models.JSON_util import JSON_util
from models.API_util import API_util

FILE_TYPE = "json"


class extract():
    def __init__(self):
        self.data = {}
        self.JSON = JSON_util()
        self.API = API_util()

    def extract_data(self):
        json_data = self.JSON.extract()
        api_data = self.API.extract()
        # merge the dictionaries into one
        self.data = {**json_data, **api_data}

    def get_data(self):
        return self.data
        

        


