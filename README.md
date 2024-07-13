Workflow Steps
    - Read JSON Files with PySpark: Use PySpark to read and process the JSON files. PySpark is well-suited for handling large datasets and distributed data processing.

    - Transform Data with PySpark: Perform necessary transformations using PySpark.

    - Convert Data to Pandas DataFrame: Convert the transformed PySpark DataFrame to a Pandas DataFrame for any further processing that is more convenient or efficient in Pandas.

    - Load Data into MySQL with SQLAlchemy: Use SQLAlchemy to load the processed data into a MySQL database.

## Writing Data to the MySQL data base

Originally I used PySpark’s JDBC direct write to my database, but I was getting compilation warnings that advised using SQLAlchemy instead. SQLAlchemy allows better transaction management and I need to set keys and alter tables, so I found this suggestion helpful. it also allows you to Object-Relational-Mapping with the database you're connecting to.
