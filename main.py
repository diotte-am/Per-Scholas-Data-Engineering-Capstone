# Imports
import findspark
findspark.init()

import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.types import StringType


from ETL import *
import typing

from App import App

INPUT_TYPES = "json"

def runETL() -> None:
    # create the SparkSession
    spark = SparkSession.builder.appName('Bank_Analysis').getOrCreate()
    ETLpipeline = jsonETL()
    ETLpipeline.run()
    spark.stop()
    print("Program completed")

def runApp() -> None:
    program_running = True
    app = App()
    app.mainloop()

def main():
    #runETL()
    runApp()

if __name__ == "__main__":
    main()