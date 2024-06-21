# Imports
import findspark
findspark.init()

import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.types import StringType

from ETL import *
import typing


INPUT_TYPES = "json"

def runETL() -> None:
    # create the SparkSession
    spark = SparkSession.builder.appName('Bank_Analysis').getOrCreate()
    ETLpipeline = jsonETL()
    ETLpipeline.run()
    spark.stop()
    print("Program completed")

def runGUI() -> None:
    program_running = True
    while program_running:
         


def main():
    runETL()
    runGUI()

if __name__ == "__main__":
    main()