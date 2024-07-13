import requests
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, substring
import mysql.connector as dbconnect
from mysql.connector import Error
import my_secrets
import schema

class Request():
    api_url = "https://raw.githubusercontent.com/platformps/LoanDataset/main/loan_data.json"
    spark = SparkSession.builder.appName('Bank_Analysis').getOrCreate()
    response = requests.get(api_url)

    # retreive current spark session
    spark = SparkSession.getActiveSession()
    df = spark.createDataFrame(data=response.json())
    table_name = "CDW_SAPP_CREDIT_APPLICATION"

    conn = None
    try: 
        conn = dbconnect.connect(host='localhost', user=my_secrets.username, database='creditcard_capstone', password=my_secrets.password)
        if conn.is_connected():
            # Get a cursor
            cursor = conn.cursor()

            cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
            conn.close()
                
    except Error as e:
        print("Conection failed!", e)
    
    df = df.withColumns({
        "Married": col("Married").cast('boolean'),
        "Self_Employed": col("Self_Employed").cast("boolean"),
        "Application_Status": col("Application_Status").cast("boolean"),
        "A_ID": substring(col("Application_ID"), 3, 6).cast("int")
    })

    try:
        df.write.format("jdbc") \
                .mode("append") \
                .option("url", "jdbc:mysql://localhost:3306/creditcard_capstone") \
                .option("dbtable", table_name) \
                .option("user", my_secrets.username) \
                .option("password", my_secrets.password) \
                .save()
    except Error as e:
        print("Unable to write 'CDW_SAPP_CREDIT_APPLICATION' to database", e)

    conn = None
    try: 
        conn = dbconnect.connect(host='localhost', user=my_secrets.username, database='creditcard_capstone', password=my_secrets.password)
        if conn.is_connected():
            # Get a cursor
            cursor = conn.cursor()
            for v in schema.pk_api:
                    cursor.execute(v)
            conn.close()
                
    except Error as e:
        print("Conection failed!", e)


    def confirm(self):
        print("Data uploaded!")

d = Request()