from pyspark.sql import SparkSession
from pyspark.sql.types import StringType, DateType, IntegerType
from schemas.transform_schema import transform_schema

class transform():

    def __init__(self, data):
        self.data = data
        self.transform_data()
        
    def transform_data(self) -> dict:
        spark = SparkSession.getActiveSession()
        data = self.data
        df_dict = {}

        # apply schema to each df
        for k,v in data.items():
            spark.createDataFrame(data[k]).createOrReplaceTempView(k)
            temp = spark.sql(transform_schema[k])
            df_dict[k] = temp

        return df_dict

