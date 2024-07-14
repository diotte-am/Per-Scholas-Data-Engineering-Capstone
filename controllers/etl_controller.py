import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.types import StringType
from models.extract import extract
from models.load import load
from models.transform import transform
from views.report import report

def run_etl():
    # create the SparkSession
    spark = SparkSession.builder.appName('Bank_Analysis').getOrCreate()

    # Extract
    data = extract()
    data.extract_data()
    
    # Transform
    raw_data = transform(data.get_data())
    transformed_data = raw_data.transform_data()

    # Load
    loaded_data = load(transformed_data)
    loaded_data.load()
    
    # Display
    view = report()
    view.display_report()
    spark.stop()