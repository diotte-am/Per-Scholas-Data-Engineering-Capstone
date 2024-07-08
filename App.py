import tkinter
import tkinter.messagebox
import customtkinter
import GUI_util as util
from Customer import Customer
from TBL_NAME import TBL_NAME
from tkcalendar import Calendar, DateEntry
import datetime

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

year_list = util.GUI_util.get_years()

MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

customer_dict = {
    "SSN": "Social Security Number", 
    "FIRST_NAME": "First Name", 
    "MIDDLE_NAME": "Middle Name", 
    "LAST_NAME": "Last Name", 
    "CREDIT_CARD_NO": "Credit Card Number",
    "FULL_STREET_ADDRESS": "Street Address", 
    "CUST_CITY": "City", 
    "CUST_STATE": "State", 
    "CUST_COUNTRY": "Country", 
    "CUST_ZIP": "Zip Code", 
    "CUST_PHONE": "Phone Number",
    "CUST_EMAIL": "Email Address",
    "LAST_UPDATED": "Last Updated",
    "CUST_ID": "Customer ID"
    }

        
class App(customtkinter.CTk):
    

    def __init__(self):
        super().__init__()

        self.util = util.GUI_util()

        # configure window
        self.title("creditcard_capstone Query")
        self.geometry(f"{1100}x{550}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # tabs
        self.Tabview = customtkinter.CTkTabview(self, width=140)
        self.Tabview.grid(row=0, column=0, rowspan=10, sticky="nsew")
        self.Tabview.add("Customers")
        self.Tabview.add("Transactions")
        self.Tabview.add("Viz")
        
        # create textbox for output
        self.Textbox_output = customtkinter.CTkTextbox(self, width=850)
        self.Textbox_output.grid(row=0, column=1, rowspan=12, sticky="ns", pady=40)
        self.Textbox_output.insert("0.0", "Enter search parameters")
        self.Textbox_output.configure(state="disabled")

        '''
        Transactions
        ''' 

        # transaction sidebar
        self.Frame_sidebar_transactions = customtkinter.CTkFrame(self.Tabview.tab("Transactions"), width=150, corner_radius=0)
        self.Frame_sidebar_transactions.grid(row=0, column=0, rowspan=10, sticky="nsew")
        self.Frame_sidebar_transactions.grid_rowconfigure(10, weight=1)

        # year dropdown
        self.Label_year = customtkinter.CTkLabel(self.Frame_sidebar_transactions, text="Year:", anchor="w")
        self.OptionMenu_year = customtkinter.CTkOptionMenu(self.Frame_sidebar_transactions, values=year_list)
        self.OptionMenu_year.set("Choose Year")

        # month dropdown
        self.Label_month = customtkinter.CTkLabel(self.Frame_sidebar_transactions, text="Month:", anchor="w")
        self.OptionMenu_month = customtkinter.CTkOptionMenu(self.Frame_sidebar_transactions, values=MONTHS)
        self.OptionMenu_month.set("Choose Month")

        # zip code entry
        self.Label_zip = customtkinter.CTkLabel(self.Frame_sidebar_transactions, text="5 Digit Zip:", anchor="w")
        self.Entry_zip = customtkinter.CTkEntry(self.Frame_sidebar_transactions, placeholder_text="Enter Zip")

        # submit button
        self.Button_submit = customtkinter.CTkButton(master=self.Frame_sidebar_transactions, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="Submit Query", width=60, command=self.submit_parameters)
        self.Button_submit.grid(row=10, column=0, padx=30)

        # set to view
        self.Label_year.grid(row=4, column=0, padx=30, pady=(10, 0))
        self.OptionMenu_year.grid(row=5, column=0, padx=30, ipady=0)
        self.Label_month.grid(row=6, column=0, padx=30, pady=(10, 0))
        self.OptionMenu_month.grid(row=7, column=0, padx=30, ipady=0, pady=(0,10))
        self.Label_zip.grid(row=8, column=0, padx=30, pady=(10, 0))
        self.Entry_zip.grid(row=9, column=0, padx=30, pady=(0, 10), ipady=0)

        '''
        Customers
        ''' 
        # Customers sidebar
        # add customer button, if customer is not selected, the options are
        
        self.Frame_sidebar_customers = customtkinter.CTkFrame(self.Tabview.tab("Customers"), width=150, corner_radius=0)
        self.Frame_sidebar_customers.grid(row=0, column=0, rowspan=10, sticky="nsew")
        self.Frame_sidebar_customers.grid_rowconfigure([0,10], weight=1)
        self.Frame_sidebar_customers.grid_columnconfigure(0, weight=1)

        self.Label_find_customer = customtkinter.CTkLabel(
            self.Frame_sidebar_customers, 
            text="No customer selected\n")
        

        self.Button_find_customer = customtkinter.CTkButton(self.Frame_sidebar_customers, text="Lookup Customer", command=self.lookup_id)
        self.Entry_find_customer = customtkinter.CTkEntry(self.Frame_sidebar_customers, placeholder_text="Customer ID")
        self.Button_edit_customer = customtkinter.CTkButton(self.Frame_sidebar_customers, text="Edit customer", state="disabled", command=self.edit_customer)

        self.Label_find_customer.grid(row=0, column=0, padx=30, pady=20)
        self.Entry_find_customer.grid(row=1, column=0, padx=30, ipady=0)
        self.Button_find_customer.grid(row=2, column=0, padx=30, pady=10)
        self.Button_edit_customer.grid(row=3, column=0, padx=30)

        self.Tabview_inner = customtkinter.CTkTabview(self.Frame_sidebar_customers, width=100)
        self.Tabview_inner.grid(row=4, column=0, rowspan=10, sticky="nsew", pady=(30,0))
        self.Tabview_inner.grid_columnconfigure(0, weight=1)
        self.Tabview_inner.add("Get Bill")
        self.Tabview_inner.add("View Transactions")

        # get transactions by data range
        self.Frame_transactions = customtkinter.CTkFrame(self.Tabview_inner.tab("View Transactions"), width=125, corner_radius=0)
        self.Frame_transactions.grid(row=0, column=0, rowspan=5)
        self.Frame_transactions.grid_rowconfigure(5, weight=1)
        self.Frame_transactions.grid_columnconfigure(0, weight=1)
        

        self.DateEntry_label1 = customtkinter.CTkLabel(self.Frame_transactions, text="Start Date", state="disabled", text_color_disabled="grey")
        self.DateEntry_1 = DateEntry(
            self.Frame_transactions, 
            date_pattern="yyyy-mm-dd", 
            state="disabled"
            )

        self.DateEntry_label2 = customtkinter.CTkLabel(self.Frame_transactions, text="End Date", state="disabled", text_color_disabled="grey")
        self.DateEntry_2 = DateEntry(self.Frame_transactions, date_pattern="yyyy-mm-dd", state="disabled")

        self.Button_customer_submit = customtkinter.CTkButton(self.Frame_transactions, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="Submit Query", state="disabled", command=self.query_timespan)

        self.DateEntry_label1.grid(row=0, column=0, padx=25, pady=(10, 0), ipady=0, sticky="ew")
        self.DateEntry_1.grid(row=1, column=0, padx=25, pady=(10, 0))
        self.DateEntry_2.grid(row=2, column=0, padx=25, pady=(20, 0))
        self.DateEntry_label2.grid(row=3, column=0)
        self.Button_customer_submit.grid(row=4, column=0, padx=25, pady=20)


        # get bill by month/year
        self.Frame_bill = customtkinter.CTkFrame(self.Tabview_inner.tab("Get Bill"), width=100, corner_radius=0)
        self.Frame_bill.grid(row=0, column=0, rowspan=5, sticky="nsew")
        self.Frame_bill.grid_rowconfigure(5, weight=1)

        # year dropdown
        self.Label_year_bill = customtkinter.CTkLabel(self.Frame_bill, text="Year:", state="disabled", text_color_disabled="grey")
        self.OptionMenu_year_bill = customtkinter.CTkOptionMenu(self.Frame_bill, values=year_list, state="disabled")
        self.OptionMenu_year_bill.set("Choose Year")

        # month dropdown
        self.Label_month_bill = customtkinter.CTkLabel(self.Frame_bill, text="Month:", state="disabled", text_color_disabled="grey")
        self.OptionMenu_month_bill = customtkinter.CTkOptionMenu(self.Frame_bill, values=MONTHS, state="disabled")
        self.OptionMenu_month_bill.set("Choose Month")
        self.Button_submit_bill = customtkinter.CTkButton(self.Frame_bill, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="Submit Query", state="disabled", command=self.generate_bill)
        

        self.Label_year_bill.grid(row=0, column=0, padx=25, pady=(10, 0), ipady=0)
        self.OptionMenu_year_bill.grid(row=1, column=0, padx=25, pady=(0, 10))
        self.Label_month_bill.grid(row=2, column=0, padx=25, pady=(10, 0), ipady=0)
        self.OptionMenu_month_bill.grid(row=3, column=0, padx=25, pady=(0, 10))
        self.Button_submit_bill.grid(row=4, column=0, padx=25, pady=20)

    def query_timespan(self):
        self.Textbox_output.configure(state="normal")
        start_date = str(self.DateEntry_1.get_date()).replace("-", "")
        end_date = str(self.DateEntry_2.get_date()).replace("-", "")
        results = self.selected_customer.full_name() + "\n" + "Transactions between " + self.DateEntry_1.get_date().strftime("%m/%d/%Y") + " and " + self.DateEntry_2.get_date().strftime("%m/%d/%Y") + "\n"
        results += self.util.query_timespan(start_date, end_date, self.selected_customer.dict)
        self.Textbox_output.configure(text_color="white")
        self.Textbox_output.delete(0.0, 'end')
        self.Textbox_output.insert(text=results, index=0.0)
        self.Textbox_output.configure(state="disabled")

        
    def generate_bill(self):
        self.Textbox_output.configure(state="normal")
        month_name = self.OptionMenu_month_bill.get()
        year = self.OptionMenu_year_bill.get()
        missing = []
        if year == "Choose Year":
                missing.append("- select year")
        if month_name == "Choose Month":
            missing.append("- select month")
        else:
            month = str(MONTHS.index(month_name) + 1)
            if len(month) == 1 : month = "0" + month
            print(month)
        if len(missing) > 0:
            message = "INVALID QUERY:\n"
            for error in missing:
                message += error + "\n"
                self.Textbox_output.delete(0.0, 'end')
                self.Textbox_output.insert(text=message, index=0.0)
                self.Textbox_output.configure(text_color="red")
        else:
            self.Textbox_output.configure(text_color="white")
            self.Textbox_output.delete(0.0, 'end')
            results = self.util.get_bills(month, year, self.selected_customer)
            text = self.Label_find_customer.cget("text") + "\n" + month_name + " " + str(year) + "\n"
            self.Textbox_output.insert(text=results, index=0.0)
            self.Textbox_output.insert(text=text, index=0.0)

        self.Textbox_output.configure(state="disabled")

    def submit_parameters(self):
        self.Textbox_output.configure(state="normal")
        year = self.OptionMenu_year.get()
        missing = []
        if year == "Choose Year":
            missing.append("- select year")
        month_name = self.OptionMenu_month.get()
        if month_name == "Choose Month":
            missing.append("- select month")
        else:
            month = str(MONTHS.index(month_name) + 1)
            if len(month) == 1 : month = "0" + month
        zip = self.Entry_zip.get()
        if zip == "":
            missing.append("- zip code field cannot be empty")
        elif not zip.isnumeric() or len(zip) != 5:
            missing.append("- zip code must be a 5 digit number")
        if len(missing) > 0:
            message = "INVALID QUERY:\n"
            for error in missing:
                message += error + "\n"
            self.Textbox_output.delete(0.0, 'end')
            self.Textbox_output.insert(text=message, index=0.0)
            self.Textbox_output.configure(text_color="red")
        else:
            self.Textbox_output.configure(text_color="white")
            self.Textbox_output.delete(0.0, 'end')
            
            util.GUI_util.set_table(util.GUI_util, TBL_NAME.CREDIT)
            results = util.GUI_util.all_details(util.GUI_util,
                                      [zip, month, year])
            results = util.GUI_util.extract_fields(util.GUI_util, results)
            if len(results) < 1:
                string = "No results found."
            else:
                string = ""
                for row in results:

                    string += "CC#: " + str(row[0]) + "\tDate: " + str(row[1]) + "\tBranch: " + str(row[2]) + "\tType: " + str(row[3]) + "\tTotal$: " + str(row[4]) + "\tBranch: " + str(row[5]) + "\n"
            self.Textbox_output.insert(text=string.expandtabs(18), index=0.0)
        self.Textbox_output.configure(state="disabled")

    def lookup_id(self):
        customer_id = self.Entry_find_customer.get()
        all_ids = self.util.get_all_CUST_IDs()
        if customer_id in all_ids:
            self.open_popup(customer_id)
        else:
            self.Textbox_output.configure(state="normal", text_color="red")
            self.Textbox_output.delete("0.0", customtkinter.END)
            self.Textbox_output.insert(index=customtkinter.END, text="ID not found!")
            self.Textbox_output.configure(state="disabled")
            self.open_popup_search()
 


    def hide_customers(self):
        pass

    def open_popup(self, customer_id):
        top= customtkinter.CTkToplevel(self)
        top.geometry("350x200")
        top.title("Customer Lookup")
        message = "Is this the correct customer?\n"
        customer_data = self.util.get_customer(customer_id)
        customer = Customer(customer_data)
        message = customer.customer_summary()
        customtkinter.CTkLabel(top, text= message).place(x=75,y=35)

        def confirm_button():
            top.destroy()
            top.update()
            self.selected_customer = customer

            # enable transaction search
            self.Label_find_customer.configure(text = customer.full_name())
            self.Button_edit_customer.configure(state="normal")
            self.DateEntry_label1.configure(state="normal")
            self.DateEntry_1.configure(state="normal")
            self.Button_customer_submit.configure(state="normal")
            self.DateEntry_2.configure(state="normal")
            self.DateEntry_label2.configure(state="normal")

            # year dropdown
            self.Label_year_bill.configure(state="normal")
            self.OptionMenu_year_bill.configure(state="normal")

            # month dropdown
            self.Label_month_bill.configure(state="normal")
            self.OptionMenu_month_bill.configure(state="normal")
            self.Button_submit_bill.configure(state="normal")
        
        def deny_button():
            top.destroy()
            top.update()
            self.Entry_find_customer.delete(0, customtkinter.END)
            self.open_popup_search()

        confirm = customtkinter.CTkButton(top, text="Yes", width=30, command=confirm_button)
        decline = customtkinter.CTkButton(top, text="No", width=30, command=deny_button)
        confirm.place(x=130, y=150)
        decline.place(x=180, y=150)

    def open_popup_search(self):
        top= customtkinter.CTkToplevel(self)
        top.geometry("600x250")
        top.title("Search for customer ID")
        customer_id = "Customer ID not found!\nContact administrator for assistance"
        customtkinter.CTkLabel(top, text= customer_id).place(x=150,y=80)

    def on_change(self, var_name, index, mode):
        widget = self.widgets[var_name]
        self.selected_customer.dict[var_name] = widget.get()
        



    def submit_edit(self):
        self.current_top.destroy()
        self.util.edit_query(self.selected_customer)
        
        
    def edit_customer(self):
        self.widgets = {}
        top = customtkinter.CTkToplevel(self)
        top.geometry("750x250")
        top.title("Edit customer details")
        top.grid_rowconfigure(0, weight=1)
        top.grid_columnconfigure(0, weight=1)

        self.Frame_edit = customtkinter.CTkFrame(top)
        self.Frame_edit.grid(row=0, column=0, sticky="nsew", ipadx=10)

        self.Frame_edit.grid_rowconfigure([0,1,2,3,4,5,6], weight=1)
        self.Frame_edit.grid_columnconfigure([0,1,2,3], weight=1)
        self.current_top = top

        row = 0
        column = 0
        for k, v in customer_dict.items():
            if k != "SSN" and k != "LAST_UPDATED":
                entry_value = str(self.selected_customer.dict[k])
                var = customtkinter.StringVar(name=k, value=entry_value)
                var.trace_add('write', self.on_change)
                label = customtkinter.CTkLabel(self.Frame_edit, text=v)
                self.widgets[k] = customtkinter.CTkEntry(self.Frame_edit, textvariable=var, width=150)
                label.grid(row=(row % 6), column=(column // 3), sticky='s')
                self.widgets[k].grid(row=(row % 6)+1, column=(column // 3), sticky='n')
                if k == "CREDIT_CARD_NO":
                    var.set("**** **** **** " + entry_value[12:])
                    self.widgets[k].configure(state="disabled")
                if k == "CUST_ID":
                    self.widgets[k].configure(state="disabled")
                    
                
                row += 2
                column += 1
                

        submit_button = customtkinter.CTkButton(self.Frame_edit, text="Submit", command=self.submit_edit)
        submit_button.grid(row=6, columnspan=2, column=1, pady=20)
            

        

        




        


