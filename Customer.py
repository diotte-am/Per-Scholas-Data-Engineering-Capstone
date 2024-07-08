from datetime import date

customer_dict = {
    "SSN": (0, "Social Security Number"), 
    "FIRST_NAME": (1, "First Name"), 
    "MIDDLE_NAME": (2, "Middle Name"), 
    "LAST_NAME": (3, "Last Name"), 
    "CREDIT_CARD_NO": (4, "Credit Card Number"),
    "FULL_STREET_ADDRESS": (5, "Street Address"), 
    "CUST_CITY": (6, "City"), 
    "CUST_STATE": (7, "State"), 
    "CUST_COUNTRY": (8, "Country"), 
    "CUST_ZIP": (9, "Zip Code"), 
    "CUST_PHONE": (10, "Phone Number"),
    "CUST_EMAIL": (11, "Email Address"),
    "LAST_UPDATED": (12, "Last Updated"),
    "CUST_ID": (13, "Customer ID")
    }

class Customer():
    def __init__(self, customer):
        self.dict = {}
        self.dict["SSN"] = customer[0]
        self.dict["FIRST_NAME"] = customer[1]
        self.dict["MIDDLE_NAME"] = customer[2]
        self.dict["LAST_NAME"] = customer[3]
        self.dict["CREDIT_CARD_NO"] = customer[4]
        self.dict["FULL_STREET_ADDRESS"] = customer[5]
        self.dict["CUST_CITY"] = customer[6]
        self.dict["CUST_STATE"] = customer[7]
        self.dict["CUST_COUNTRY"] = customer[8]
        self.dict["CUST_ZIP"] = customer[9]
        self.dict["CUST_PHONE"] = customer[10]
        self.dict["CUST_EMAIL"] = customer[11]
        self.dict["LAST_UPDATED"] = customer[12]
        self.dict["CUST_ID"] = customer[13]



    def customer_summary(self):
        message = "Is this the correct customer?\n"
        message += self.dict["FIRST_NAME"] + " " + self.dict["MIDDLE_NAME"] + " " + self.dict["LAST_NAME"] + "\n"
        message += self.dict["FULL_STREET_ADDRESS"] + "\n" + self.dict["CUST_CITY"] + ", " + self.dict["CUST_STATE"] + ", " + self.dict["CUST_COUNTRY"] + ", " + self.dict["CUST_ZIP"] + "\n"
        message += "Phone: " + self.dict["CUST_PHONE"] + "\n"
        message += "Email: " + self.dict["CUST_EMAIL"] + "\n"
        return message
    
    def first_name(self): return self.dict["FIRST_NAME"]
    def get_id(self): return self.dict["CUST_ID"]
    
    def full_name(self):
        name = self.dict["FIRST_NAME"] + " " + self.dict["MIDDLE_NAME"] + " " + self.dict["LAST_NAME"]
        return name
    
    def get_edit_query(self):
        string = ""
        for item in customer_dict.keys():
            if item not in ("CREDIT_CARD_NO", "CUST_ID", "SSN"):
                if item == "LAST_UPDATED":
                    string += str(item) + " = '" + str(date.today()) + "' "
                else:
                    string += str(item) + " = '" + str(self.dict[item]) + "', "
        return string
