import typing
from pyspark.sql import SparkSession
from pyspark.sql.types import StringType, DateType, IntegerType
from util.JSON_util import JSON_util
from util.API_util import API_util

FILE_TYPE = "json"


class extract():
    data: dict
    JSON: JSON_util
    API: API_util

    def __init__(self):
        self.data = {}
        self.JSON = JSON_util()
        self.API = API_util()

    def extract_data(self) -> None:
        json_data = self.JSON.extract()
        api_data = self.API.extract()
        # merge the dictionaries into one
        self.data = {**json_data, **api_data}

    def get_data(self) -> dict:
        return self.data
    
    def delete_data(self) -> None:
        self.data.clear()
    
        

        


