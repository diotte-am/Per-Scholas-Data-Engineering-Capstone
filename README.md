



![Schema for creditcard_capstone db](images/data_lake.png)



### Workflow Steps
- Read JSON Files with PySpark: Use PySpark to read and process the JSON files. PySpark is well-suited for handling large datasets and distributed data processing.

- Transform Data with PySpark: Perform necessary transformations using PySpark.

- Convert Data to Pandas DataFrame: Convert the transformed PySpark DataFrame to a Pandas DataFrame for any further processing that is more convenient or efficient in Pandas.

- Load Data into MySQL with SQLAlchemy: Use SQLAlchemy to load the processed data into a MySQL database.

### Cleaning and transforming data
I created a ETL pipeline to clean and organize the data from the JSON files and API into a one database. I was given a mapping document with instructions on how to organize this text into tables. 
I made a couple changes to the proposed tables to normalize them:
- I removed the social security number column from the CDW_SAPP_CREDIT table, to get rid of duplicate data.
- I added a customer id to the CDW_SAPP_CUSTOMER table so that the SSN wouldn't act as a primary key. Where it's private information and has actual meaning to the data set, it's not a good candidate key
- The customer phone numbers did not have area codes. Where all the phone numbers of the branches are "123", I changed the customer numbers to have the same area code.

### Loading to a Database
Originally I used PySpark’s JDBC direct write to my database, but I was getting compilation warnings that advised using SQLAlchemy instead. SQLAlchemy allows better transaction management and I need to set keys and alter tables, so I found this suggestion helpful. it also allows you to Object-Relational-Mapping with the database you're connecting to. I would like to explore ORM when I have more time.

## Creating a Dashboard
I used the CustomTkinter library to build my Dashboard. I didn't have a lot of time to design the look of my UI so the color presets in this library made it a great option. Learning the grid layout system took some effort and some of the widgets are still a little buggy (DateEntry is pretty bad), but for the most part, it was easy to use and easy to make nice looking UI.

I split my dashboard into three tabs - Customers, Transactions, Viz

### Transactions Tab, Req 2.1 
![Transactions Tab, Req 2.1](images/gui_transaction_result.png)
The user choses the year and month from the drop down menus and a 5 digit zip code in the entry box. Upon clicking the button, a query is run on the connected MySQL db returning up to date information on all transactions that occured in that zip code during that month. This data is parsed and formatted and displayed in the large text box in the dashboard.

### Customers Tab, Req 2.2
![Customers Tab, Req 2.2](images/gui_customer_tab.png)
When you first get to the customer tab, the search functions are disabled because a customer must be chosen for this search.

![Customers Tab, Req 2.2.1](images/gui_customer_tab_lookup.png)
Enter a customer ID and hit the lookup customer button. A pop up will come up to confirm the individual is the correct person. Upon accepting, the customer is now selected and you can do the searches below.

![Customers Tab, Req 2.2.2](images/gui_customer_edit.png)
Hitting the edit customer button will bring up a new window where fields can be updated. Some of the fields are not able to be changed for security reasons - SSN, ID, credit card number. Only the last 4 digits of the card number are shown for security reasons as well.

![Customers Tab, Req 2.2.3](images/gui_customer_tab_bill.png)
Under the Get Bill tab, you can select the year and month and get an itemized bill for the customer's transactions during that period.

![Customers Tab, Req 2.2.4](images/gui_customer_tab_timespan.png.png)
Under the view transactions tab, you can use the two calendar widgets to select your date range. Hitting the button will query the db for any transactions this customer made during that period of time.

### Visualizations Tab, Req 3