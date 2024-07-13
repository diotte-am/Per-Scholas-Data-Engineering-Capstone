# Imports
import findspark
findspark.init()

import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.types import StringType
from Graph import Graph

from ETL import *
import typing

from App import App
from Request import Request

INPUT_TYPES = "json"

def runETL() -> None:
    # create the SparkSession
    spark = SparkSession.builder.appName('Bank_Analysis').getOrCreate()
    ETLpipeline = jsonETL()
    loadAPI = Request()
    loadAPI.confirm()
    ETLpipeline.run()
  #  graphics = Graph()
  #  graphics.create_viz()
    spark.stop()
    print("Program completed")

def runApp() -> None:
    app = App()
    app.mainloop()

def main():
    runETL()
    runApp()

if __name__ == "__main__":
    main()