# Imports
import findspark
findspark.init()

import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.types import StringType

from ETL import *
import typing

INPUT_TYPES = "json"

def init() -> None:
    # create the SparkSession
    spark = SparkSession.builder.appName('Bank_Analysis').getOrCreate()
    ETLpipeline = jsonETL()
    ETLpipeline.run()
    spark.stop()
    print("Program completed")


def main():
    init()

if __name__ == "__main__":
    main()