import mysql.connector as dbconnect
from mysql.connector import Error
import my_secrets
import pandas as pd

class GUI_util():
    def __init__(self):
        pass
    
    def date_to_string(self, dateID):
        return dateID[0:4] + "/" + dateID[4:6] + "/" + dateID[6:]

    def get_date_zip(self, zip, year, month):
        query = "SELECT *, SUBSTRING(CREDIT.TIMEID, 7) AS DAY\
                FROM CDW_SAPP_CREDIT AS CREDIT\
                JOIN CDW_SAPP_BRANCH AS BRANCH ON CREDIT.BRANCH_CODE = BRANCH.BRANCH_CODE\
                WHERE SUBSTRING(CREDIT.TIMEID, 1, 6) = " + year + month + " AND \
                BRANCH.BRANCH_ZIP = " + zip + " ORDER BY DAY DESC"
        conn = None
        try: 
            conn = dbconnect.connect(host='localhost', user=my_secrets.username, database='creditcard_capstone', password=my_secrets.password)

            if conn.is_connected():
                result = pd.read_sql(query, conn)
                string = ""
                for row in result.values:
                    for column in ("CC Last 4", "Date", "Branch", "Type", "Total$", "Cust ID"):
                        string += column +"\t\t"
                    string += str(row[0])[-4:] + "\t\t" + self.date_to_string(str(row[1])) + "\t\t" + str(row[2]) + "\t\t" + str(row[3]) + "\t\t" + str(row[4]) + "\t\t" + str(row[6]) + "\n\n"

                conn.close()
        except Error as e:
            print("Query failed at line 65", e)
        return string
        
    def get_years(self):
        conn = None
        query = "SELECT DISTINCT SUBSTRING(CAST(TIMEID AS CHAR), 1, 4) AS YEAR FROM CDW_SAPP_CREDIT"
        try: 
            conn = dbconnect.connect(host='localhost', user=my_secrets.username, database='creditcard_capstone', password=my_secrets.password)
            if conn.is_connected():
                year_df = pd.read_sql(query, conn)
                conn.close()
                                    
        except Error as e:
            print("Query failed at line 142", e)
        return year_df["YEAR"]
        
    def get_all_CUST_IDs(self):
        conn = None
        query = "SELECT DISTINCT CAST(CUST_ID AS CHAR) AS CUST FROM CDW_SAPP_CUSTOMER"
        try:
            conn = dbconnect.connect(host='localhost', user=my_secrets.username, database='creditcard_capstone', password=my_secrets.password)
            if conn.is_connected():
                id_list = pd.read_sql(query, conn)
                conn.close()
                                  
        except Error as e:
            print("Query failed at line 157", e)
        return id_list.values
    
    def get_customer(self, cust_id):
        conn = None
        query = "SELECT * FROM CDW_SAPP_CUSTOMER WHERE CUST_ID = " + cust_id
        try:
            conn = dbconnect.connect(host='localhost', user=my_secrets.username, database='creditcard_capstone', password=my_secrets.password)
            if conn.is_connected():
                cust_list = pd.read_sql(query, conn)
                conn.close()
                                  
        except Error as e:
            print(query)
            print("Query failed at line 171", e)
        return cust_list.values[0]
    
    def get_bills(self, month, year, selected_customer):
        customer_id = selected_customer.get_id()
        conn = None
        query = "SELECT * FROM CDW_SAPP_CREDIT WHERE CUST_ID = " + str(customer_id) + " AND CAST(TIMEID AS CHAR) LIKE '" + year + month + "__'"

        try:
            conn = dbconnect.connect(host='localhost', user=my_secrets.username, database='creditcard_capstone', password=my_secrets.password)
            if conn.is_connected():
                result = pd.read_sql(query, conn)
                string = ""
                sum = 0
                for row in result.values:
                    for column in ("Trans. ID", "Date", "Type", "Cost"):
                        string += column + "\t\t"
                    string += "\n" + str(row[5]) + "\t\t" + self.date_to_string(str(row[1])) + "\t\t" + str(row[3]) + "\t\t" + str(row[4]) + "\n\n"
                    sum += row[4]
                conn.close()
                                  
        except Error as e:
            print("Query failed at line 195", e)
        string += "\n" + "Total bill: $" +  str(round(sum, 2))
        return string

    def query_timespan(self, start, end, customer):
        query = "SELECT * FROM CDW_SAPP_CREDIT WHERE CUST_ID = " + str(customer["CUST_ID"]) + " AND TIMEID BETWEEN " + start + " AND " + end + " ORDER BY TIMEID DESC"
        try:
            conn = dbconnect.connect(host='localhost', user=my_secrets.username, database='creditcard_capstone', password=my_secrets.password)
            if conn.is_connected():
                result = pd.read_sql(query, conn)
                conn.close() 
        except Error as e:
            result = ("Conection failed!", e)
        string = ""
        for row in result.values:
            for column in ("Date", "Branch", "Type", "Value", "Trans ID"):
                string += column + "\t\t"
            string += "\n" + self.date_to_string(str(row[1])) + "\t\t" + str(row[2]) + "\t\t" + str(row[3]) + "\t\t" + str(row[4]) + "\t\t" + str(row[5]) + "\n\n"
        return string
    
    def edit_query(self, customer):
        query = "UPDATE CDW_SAPP_CUSTOMER SET " + customer.get_edit_query() + " WHERE CUST_ID = " + str(customer.get_id()) 
        try:
            conn = dbconnect.connect(host='localhost', user=my_secrets.username, database='creditcard_capstone', password=my_secrets.password)

            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute(query)
                conn.commit()
                
                string = ""
                result = [string.__add__(x) for x in customer.dict]
        except Error as e:
           result = "Conection failed! 233" + e

        return result