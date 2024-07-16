from pyspark.sql import SparkSession
from pyspark.sql.types import StringType
from models.extract import extract
from models.load import load
from models.transform import transform
from views.report import report
import typing

def run_etl() -> None:
    # create the SparkSession
    spark : SparkSession = SparkSession.builder.appName('Bank_Analysis').getOrCreate()

    # Extract
    data : extract = extract()
    data.extract_data()
    
    # Transform
    raw_data : transform = transform(data.get_data())
    transformed_data = raw_data.transform_data()

    # Load
    loaded_data : load = load(transformed_data)
    loaded_data.load()
    

    # Clean up
    data.delete_data()
    spark.stop()