import tkinter
import tkinter.messagebox
import customtkinter
import GUI_util as util

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
                                                                       command=self.change_appearance_mode_event)
        self.OptionMenu_year.grid(row=5, column=0, padx=20, ipady=0)
        self.OptionMenu_year.set("Choose Year")
        
        self.Label_month = customtkinter.CTkLabel(self.Frame_sidebar, text="Month:", anchor="w")
        self.Label_month.grid(row=6, column=0, padx=20, pady=(10, 0))
        self.OptionMenu_month = customtkinter.CTkOptionMenu(self.Frame_sidebar, values=MONTHS,
                                                               command=self.change_scaling_event)
        self.OptionMenu_month.grid(row=7, column=0, padx=20, ipady=0, pady=(0,10))
        self.OptionMenu_month.set("Choose Month")

        self.Label_zip = customtkinter.CTkLabel(self.Frame_sidebar, text="5 Digit Zip:", anchor="w")
        self.Label_zip.grid(row=8, column=0, padx=20, pady=(10, 0))
        self.Entry_zip = customtkinter.CTkEntry(self.Frame_sidebar, placeholder_text="Enter Zip")
        self.Entry_zip.grid(row=9, column=0, padx=20, pady=(0, 10), ipady=0)
        
        # submit button
        self.Button_submit = customtkinter.CTkButton(master=self.Frame_sidebar, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="Submit Query", width=60)
        self.Button_submit.grid(row=10, column=0, padx=20)

        # create textbox
        self.Textbox_output = customtkinter.CTkTextbox(self)
        self.Textbox_output.grid(row=0, column=1, columnspan=3, rowspan=4, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.Textbox_output.insert("0.0", "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n" * 20)


        # set default values
        self.Button_visualizations.configure(text="Visualizations")
        self.Button_transactions.configure(text="Transactions")
        self.Button_customer.configure(text="Customers")
    
  


       
        
    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        pass
    def sidebar_button_event(self):
        print("sidebar_button click")


if __name__ == "__main__":
    app = App()
    app.mainloop()