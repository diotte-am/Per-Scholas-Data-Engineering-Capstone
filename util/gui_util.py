import mysql.connector as dbconnect
from mysql.connector import Error
import my_secrets
import pandas as pd

class GUI_util():
    def __init__(self):
        pass
    
    def get_bill(self, zip, year, month):
        query = "SELECT *, SUBSTRING(CREDIT.TIMEID, 7) AS DAY\
                FROM CDW_SAPP_CREDIT AS CREDIT\
                JOIN CDW_SAPP_BRANCH AS BRANCH ON CREDIT.BRANCH_CODE = BRANCH.BRANCH_CODE\
                WHERE SUBSTRING(CREDIT.TIMEID, 1, 6) = " + year + month + " AND \
                BRANCH.BRANCH_ZIP = " + zip + " ORDER BY DAY DESC"
        conn = None
        try: 
            conn = dbconnect.connect(host='localhost', user=my_secrets.username, database='creditcard_capstone', password=my_secrets.password)

            if conn.is_connected():
                df = pd.read_sql(query, conn)
                conn.close()
                return df
                        
        except Error as e:
            print(query)
            print("Query failed at line 65", e)

    def extract_fields(self, results: list[str]):
        final = pd.DataFrame(columns=["credit card number", "transaction time", "branch code", "transaction type", "transaction value", "transaction id"])
        for row in results:
            cc_redacted = "**** **** **** " + str(row[0])[12:]
            time = str(row[1])[0:4] + "/" + str(row[1])[4:6] + "/" + str(row[1])[6:]
            branch_code = row[2]
            t_type = row[3]
            t_value = row[4]
            t_id = row[5]
            temp = pd.DataFrame.from_dict({
                "credit card number": [cc_redacted], 
                "transaction time": [time], 
                "branch code": [branch_code], 
                "transaction type": [t_type], 
                "transaction value": [t_value],
                "transaction id": [t_id]
                })
                
            final = pd.concat([temp, final], ignore_index=True)

        return final.values
        
    def get_years(self):
        conn = None
        query = "SELECT DISTINCT SUBSTRING(CAST(TIMEID AS CHAR), 1, 4) AS YEAR FROM CDW_SAPP_CREDIT"
        try: 
            conn = dbconnect.connect(host='localhost', user=my_secrets.username, database='creditcard_capstone', password=my_secrets.password)
            if conn.is_connected():
                year_df = pd.read_sql(query, conn)
                conn.close()
                                    
        except Error as e:
            print(query)
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
                        string += column + "\t"
                    string += "\n" + str(row[5]) + "\t" + str(row[1])[-2:] + "\t" + str(row[3]) + "\t" + str(row[4]) + "\n\n"
                    sum += row[4]
                conn.close()
                                  
        except Error as e:
            print(query)
            print("Query failed at line 195", e)
        string += "\n" + "Total bill: $" +  str(round(sum, 2))
        return string

    def query_timespan(self, start, end, customer):
        query = "SELECT * FROM CDW_SAPP_CREDIT WHERE CUST_ID = " + str(customer["CUST_ID"]) + " AND TIMEID BETWEEN " + start + " AND " + end + " ORDER BY TIMEID DESC"
        string1 = ""
        string2 = ""
        try:
            conn = dbconnect.connect(host='localhost', user=my_secrets.username, database='creditcard_capstone', password=my_secrets.password)
            if conn.is_connected():
                result = pd.read_sql(query, conn)
                conn.close() 
        except Error as e:
            result = ("Conection failed!", e)
            
        for index, item in result.iterrows():
 
            string1 += "\n" + str(index) 
            string2 += "\n" + str(item) + "\n"
        return result.to_string()

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