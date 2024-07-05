import mysql.connector as dbconnect
from mysql.connector import Error
import my_secrets
from TBL_NAME import TBL_NAME
import calendar
import pandas as pd
from tabulate import tabulate

class GUI_util():
    def __init__(self):
        self.current_table = TBL_NAME.CREDIT
     
    def test(self):
          print("yo!")
    
    def build_query(self):
        if self.current_table == TBL_NAME.CREDIT:
            valid_input = False
            
            while not valid_input:
                input_zip = input("Enter a five digit zip code: ")
                if len(input_zip) == 5:
                    if input_zip.isnumeric():
                        valid_input = True
                print("Zip code must be a five digit number!")

            valid_input = False
            while not valid_input:
                input_month = input("Enter month as a number(1-12):")
                if input_month.isnumeric():
                    month = int(input_month)
                    if month >= 1 and month <= 12:
                        if month >= 1 and month <= 9:
                            input_month = "0" + input_month
                        valid_input = True
                    else: print("Invalid input, must be between 1 and 12!")
                else:
                    print("Invalid input, must be a number!")
            
            valid_input = False
            while not valid_input:
                input_year = input("Enter year:")
                if input_year.isnumeric():
                    year = int(input_year)
                    if year >= 1970 and year <= 2024:
                        valid_input = True
                    else: print("Invalid input, must be between 1 and 12!")
                else:
                    print("Invalid input, must be a number!")
            
        # query = where customer.zip = input_zip AND CONCAT(year, month) LIKE credit.TIMEID[0:6]
        return input_zip, input_month, input_year
    
    def all_details(self, inputs):
        if self.current_table == TBL_NAME.CUST:
            query = "SELECT * FROM CDW_SAPP_CUSTOMER"
            
        elif self.current_table == TBL_NAME.CREDIT:
            query = "SELECT *, SUBSTRING(CREDIT.TIMEID, 7) AS DAY FROM CDW_SAPP_CREDIT AS CREDIT\
                JOIN CDW_SAPP_BRANCH AS BRANCH ON CREDIT.BRANCH_CODE = BRANCH.BRANCH_CODE\
                WHERE SUBSTRING(CREDIT.TIMEID, 1, 6) = " + inputs[2] + inputs[1] + " AND \
                BRANCH.BRANCH_ZIP = " + inputs[0] + " ORDER BY DAY DESC"

        conn = None
        try: 
            conn = dbconnect.connect(host='localhost', user=my_secrets.username, database='creditcard_capstone', password=my_secrets.password)

            if conn.is_connected():
                print('Connected to MySQL database')
                cursor = conn.cursor()
                cursor.execute(query)
                df = cursor.fetchall()

                conn.close()
                return df
                        
        except Error as e:
            print("Conection failed!", e)
        
        
    
    def set_table(self, table_name: TBL_NAME):
        self.current_table = table_name
    
    def extract_fields(self, results: list[str]):
        if self.current_table == TBL_NAME.CUST:
            for row in results:
                full_name = " ".join([row[1], row[2], row[3]])
                ssn_redacted = "***-**-" + str(row[0])[5:]
                cc_redacted = "**** **** **** " + str(row[4])[12:]
                street = row[5]
                city = row[6]
                state = row[7]
                country = row[8]
                zip = row[9]
                phone = row[10]
                email = row[11]
                print(full_name, ssn_redacted, cc_redacted, street, city, state, country, zip, phone, email)

        elif self.current_table == TBL_NAME.CREDIT:
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
        
    def get_years():
        conn = None
        query = "SELECT DISTINCT Year FROM CDW_SAPP_PERIOD"
        try: 
            conn = dbconnect.connect(host='localhost', user=my_secrets.username, database='creditcard_capstone', password=my_secrets.password)

            if conn.is_connected():
                print('Connected to MySQL database')
                cursor = conn.cursor()
                cursor.execute(query)
                results = cursor.fetchall()
                year_list = []
                for row in results:
                    year_list.append(str(row[0]))

                conn.close()
                                      
        except Error as e:
            print("Conection failed!", e)
        



        return year_list
        
    def get_all_CUST_IDs(self):
        conn = None
        query = "SELECT CUST_ID FROM CDW_SAPP_CUSTOMER"
        try:
            conn = dbconnect.connect(host='localhost', user=my_secrets.username, database='creditcard_capstone', password=my_secrets.password)

            if conn.is_connected():
                print('Connected to MySQL database')
                cursor = conn.cursor()
                cursor.execute(query)
                results = cursor.fetchall()
                id_list = []
                for row in results:
                    id_list.append(str(row[0]))
                conn.close()
                                  
        except Error as e:
            print("Conection failed!", e)
        return id_list
    
    def get_customer(self, cust_id):
        conn = None
        query = "SELECT * FROM CDW_SAPP_CUSTOMER WHERE CUST_ID = " + cust_id
        try:
            conn = dbconnect.connect(host='localhost', user=my_secrets.username, database='creditcard_capstone', password=my_secrets.password)

            if conn.is_connected():
                print('Connected to MySQL database')
                cursor = conn.cursor()
                cursor.execute(query)
                result = cursor.fetchone()

                conn.close()
                                  
        except Error as e:
            print("Conection failed!", e)
        return result
    
    def get_bills(self, month, year, selected_customer):
        customer_id = selected_customer[13]
        conn = None
        query = "SELECT * FROM CDW_SAPP_CREDIT WHERE CUST_ID = " + str(customer_id) + " AND CAST(TIMEID AS CHAR) LIKE '" + year + month + "__'"

        try:
            conn = dbconnect.connect(host='localhost', user=my_secrets.username, database='creditcard_capstone', password=my_secrets.password)

            if conn.is_connected():
                print('Connected to MySQL database')
                cursor = conn.cursor()
                cursor.execute(query)
                result = cursor.fetchall()
                id_list = []
                for row in result:
                    id_list.append(str(row[4]))
                conn.close()
                                  
        except Error as e:
            print("Conection failed!", e)
        return id_list

    def query_timespan(self, start, end, customer):
        return start, end, customer[13]
        

    

        


                
   



