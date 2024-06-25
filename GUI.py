import tkinter as tk
import customtkinter
import GUI_util as util

# Create the main window
customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"
WIDTH = 1100 
HEIGHT = 580

class GUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Credit Card Transactions")
        self.geometry(f"{WIDTH}x{HEIGHT}")
        self.columnconfigure(0, weight=1)
        self.tabview = customtkinter.CTkTabview(
            master=self, 
            width=WIDTH, 
            height=HEIGHT, 
            corner_radius=12    
        )
        
        self.tabview.add("Transactions")
        self.tabview.add("Customer Info")
        self.tabview.grid(row=0, column=0, padx=10, pady=10)

        self.cust_label = customtkinter.CTkLabel(master=self.tabview.tab("Customer Info"), text="Customer Info")
        self.cust_label.grid(row=0, column=0, padx=20, pady=20)

        self.trans_label = customtkinter.CTkLabel(master=self.tabview.tab("Transactions"), text="Please enter search criteria below:")
        self.trans_label.grid(row=0, column=0, pady=20, padx=20)
        # add dropdown box with year, month, single text box for zip code
        # submit button
        # frame below to display results

    def button_function(self):
        print("button pressed")

    def run(self):
        u = util.GUI_util()
        u.test()
        self.mainloop()


g = GUI()
g.run()

    

