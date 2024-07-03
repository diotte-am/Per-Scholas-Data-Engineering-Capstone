import tkinter
import tkinter.messagebox
import customtkinter
import GUI_util as util
from TBL_NAME import TBL_NAME
from tkcalendar import Calendar, DateEntry
import datetime

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
CURRENT_TAB = "Transactions"
class App(customtkinter.CTk):
    

    def __init__(self):
        super().__init__()

        self.util = util.GUI_util()
        self.selected_customer = []

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
        self.Frame_sidebar_transactions = customtkinter.CTkFrame(self.Tabview.tab("Transactions"), width=140, corner_radius=0)
        self.Frame_sidebar_transactions.grid(row=0, column=0, rowspan=10, sticky="nsew")
        self.Frame_sidebar_transactions.grid_rowconfigure(10, weight=1)

        # year dropdown
        year_list = self.util.get_years()
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
        
        self.Frame_sidebar_customers = customtkinter.CTkFrame(self.Tabview.tab("Customers"), width=140, corner_radius=0)
        self.Frame_sidebar_customers.grid(row=0, column=0, rowspan=10, sticky="nsew")
        self.Frame_sidebar_customers.grid_rowconfigure(10, weight=1)

        self.Label_find_customer = customtkinter.CTkLabel(
            self.Frame_sidebar_customers, 
            text="No customer selected\n")
        

        self.Button_find_customer = customtkinter.CTkButton(self.Frame_sidebar_customers, text="Lookup Customer", command=self.lookup_id)
        self.Entry_find_customer = customtkinter.CTkEntry(self.Frame_sidebar_customers, placeholder_text="Customer ID")
        self.Button_edit_customer = customtkinter.CTkButton(self.Frame_sidebar_customers, text="Edit customer", state="disabled")

        self.Label_find_customer.grid(row=0, column=0, padx=30, pady=20)
        self.Entry_find_customer.grid(row=1, column=0, padx=30, ipady=0)
        self.Button_find_customer.grid(row=2, column=0, padx=30, pady=10)
        self.Button_edit_customer.grid(row=3, column=0, padx=30)

        self.Tabview_inner = customtkinter.CTkTabview(self.Frame_sidebar_customers, width=125)
        self.Tabview_inner.grid(row=4, column=0, rowspan=10, sticky="nsew", pady=(30,0))
        self.Tabview_inner.add("Get Bill")
        self.Tabview_inner.add("View Transactions")

        # get transactions by data range
        self.Frame_transactions = customtkinter.CTkFrame(self.Tabview_inner.tab("View Transactions"), width=125, corner_radius=0)
        self.Frame_transactions.grid(row=0, column=0, rowspan=5, sticky="nsew")
        self.Frame_transactions.grid_rowconfigure(5, weight=1)

        self.DateEntry_label1 = customtkinter.CTkLabel(self.Frame_transactions, text="Start Date", state="disabled", text_color_disabled="grey")
        self.DateEntry_1 = DateEntry(
            self.Frame_transactions, 
            date_pattern="yyyy-mm-dd", 
            state="disabled", 
            day=1,
            month=1,
            year=2018
            )

        self.DateEntry_label2 = customtkinter.CTkLabel(self.Frame_transactions, text="End Date", state="disabled", text_color_disabled="grey")
        self.DateEntry_2 = DateEntry(self.Frame_transactions, date_pattern="yyyy-mm-dd", state="disabled")

        self.Button_customer_submit = customtkinter.CTkButton(self.Frame_transactions, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="Submit Query", state="disabled")

        self.DateEntry_label1.grid(row=0, column=0, padx=30, pady=(10, 0), ipady=0)
        self.DateEntry_1.grid(row=1, column=0, padx=30, pady=(10, 0))
        self.DateEntry_2.grid(row=2, column=0, padx=30, pady=(20, 0))
        self.DateEntry_label2.grid(row=3, column=0)
        self.Button_customer_submit.grid(row=4, column=0, pady=20)

        # get bill by month/year
        self.Frame_bill = customtkinter.CTkFrame(self.Tabview_inner.tab("Get Bill"), width=125, corner_radius=0)
        self.Frame_bill.grid(row=0, column=0, rowspan=5, sticky="nsew")
        self.Frame_bill.grid_rowconfigure(5, weight=1)

        
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
            month = str(MONTHS.index(month_name))
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
        customer = self.util.get_customer(customer_id)
        message += customer[1] + " " + customer[2] + " " + customer[3] + "\n"
        message += customer[5] + "\n" + customer[6] + ", " + customer[7] + ", " + customer[8] + ", " + customer[9] + "\n"
        message += "Phone: " + customer[10] + "\n"
        message += "Email: " + customer[11] + "\n"
        customtkinter.CTkLabel(top, text= message).place(x=150,y=50)
        def confirm_button():
            top.destroy()
            top.update()
            self.selected_customer = customer
            self.Label_find_customer.configure(text = customer[1] + " " + customer[2] + " " + customer[3] + "\n")
            self.Button_edit_customer.configure(state="normal")
            self.DateEntry_label1.configure(state="normal")
            self.DateEntry_1.configure(state="normal")
            self.Button_customer_submit.configure(state="normal")
            self.DateEntry_2.configure(state="normal")
            self.DateEntry_label2.configure(state="normal")

        def deny_button():
            top.destroy()
            top.update()
            self.Entry_find_customer.delete(0, customtkinter.END)
            self.open_popup_search()

        confirm = customtkinter.CTkButton(top, text="Yes", width=30, command=confirm_button)
        decline = customtkinter.CTkButton(top, text="No", width=30, command=deny_button)
        confirm.place(x=125, y=175)
        decline.place(x=175, y=175)



    def open_popup_search(self):
        top= customtkinter.CTkToplevel(self)
        top.geometry("750x250")
        top.title("Search for customer ID")
        customer_id = "enter query info"
        customtkinter.CTkLabel(top, text= customer_id).place(x=150,y=80)


        


