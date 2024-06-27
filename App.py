import tkinter
import tkinter.messagebox
import customtkinter
import GUI_util as util
from TBL_NAME import TBL_NAME

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.util = util.GUI_util()

        # configure window
        self.title("creditcard_capstone Query")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.Frame_sidebar = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.Frame_sidebar.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.Frame_sidebar.grid_rowconfigure(10, weight=1)
        
        # title
        self.Label_title = customtkinter.CTkLabel(self.Frame_sidebar, text="Choose your query type:", font=customtkinter.CTkFont(size=18, weight="bold"))
        self.Label_title.grid(row=0, column=0, padx=20, pady=(20, 10))

        # transaction button
        self.Button_transactions = customtkinter.CTkButton(self.Frame_sidebar, command=self.sidebar_button_event)
        self.Button_transactions.grid(row=1, column=0, padx=20, pady=10)

        # customer button
        self.Button_customer = customtkinter.CTkButton(self.Frame_sidebar, command=self.sidebar_button_event)
        self.Button_customer.grid(row=2, column=0, padx=20, pady=10)

        # visualization button
        self.Button_visualizations = customtkinter.CTkButton(self.Frame_sidebar, command=self.sidebar_button_event)
        self.Button_visualizations.grid(row=3, column=0, padx=20, pady=10)

        # year dropdown
        # frame below to display results
        year_list = self.util.get_years()
        self.Label_year = customtkinter.CTkLabel(self.Frame_sidebar, text="Year:", anchor="w")
        self.Label_year.grid(row=4, column=0, padx=20, pady=(10, 0))
        self.OptionMenu_year = customtkinter.CTkOptionMenu(self.Frame_sidebar, values=year_list,
                                                                       command=self.optionMenu_year)
        self.OptionMenu_year.grid(row=5, column=0, padx=20, ipady=0)
        self.OptionMenu_year.set("Choose Year")
        
        self.Label_month = customtkinter.CTkLabel(self.Frame_sidebar, text="Month:", anchor="w")
        self.Label_month.grid(row=6, column=0, padx=20, pady=(10, 0))
        self.OptionMenu_month = customtkinter.CTkOptionMenu(self.Frame_sidebar, values=MONTHS)
        self.OptionMenu_month.grid(row=7, column=0, padx=20, ipady=0, pady=(0,10))
        self.OptionMenu_month.set("Choose Month")

        self.Label_zip = customtkinter.CTkLabel(self.Frame_sidebar, text="5 Digit Zip:", anchor="w")
        self.Label_zip.grid(row=8, column=0, padx=20, pady=(10, 0))
        self.Entry_zip = customtkinter.CTkEntry(self.Frame_sidebar, placeholder_text="Enter Zip")
        self.Entry_zip.grid(row=9, column=0, padx=20, pady=(0, 10), ipady=0)
        
        # submit button
        self.Label_submit = customtkinter.CTkLabel(self.Frame_sidebar, text="5 Digit Zip:", anchor="w")
        self.Label_submit.grid(row=10, column=0, padx=20, pady=(10, 0))
        self.Button_submit = customtkinter.CTkButton(master=self.Frame_sidebar, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="Submit Query", width=60, command=self.submit_parameters)
        self.Button_submit.grid(row=10, column=0, padx=20)

        # create textbox
        self.Textbox_output = customtkinter.CTkTextbox(self)
        self.Textbox_output.grid(row=0, column=1, columnspan=3, rowspan=4, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.Textbox_output.insert("0.0", "Enter search parameters")


        # set default values
        self.Button_visualizations.configure(text="Visualizations")
        self.Button_transactions.configure(text="Transactions")
        self.Button_customer.configure(text="Customers")
    
    def popup_window(self):
        window = customtkinter.CTkToplevel()

        label = customtkinter.CTkLabel(window, text="Hello World!")
        label.pack(fill='x', padx=50, pady=5)

        button_close = customtkinter.CTkButton(window, text="Close", command=window.destroy)
        button_close.pack(fill='x')




    def optionMenu_year(self, new_appearance_mode: str):
        pass

    def submit_parameters(self):
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
            self.Textbox_output.insert(text=results, index=0.0)



    

    def sidebar_button_event(self):
        print("sidebar_button click")


