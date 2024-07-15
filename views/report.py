import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import customtkinter as ctk
import tkinter as tk
from models.graph import graph
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from schemas.graph_schema import GRAPH
import customtkinter  
class report():
    def __init__(self, parent):
        self.parent = parent
        self.graph = graph()
        self.colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
     
    def plot_graph(self, query_num):
        top= customtkinter.CTkToplevel(self.parent)
        top.geometry("600x500")
        top.title("Customer Lookup")
        results = self.graph.query(GRAPH[query_num][0])
        print(results)
        fig = Figure(figsize=(6, 5), dpi=100)
        ax = fig.add_subplot(111)
        match query_num:
            case "3.1":
                ax.bar(results["TRANSACTION_TYPE"], results["TOTAL"], color=self.colors)
                ax.set_title(GRAPH[query_num][1])
                ax.set_xlabel("Type of Transaction")
                ax.set_ylabel("Number of Transactions")
            case "3.2":
                ax.bar(results["CUST_STATE"], results["TOTAL"], color=self.colors)
                ax.set_title(GRAPH[query_num][1])
                ax.set_xlabel("Customer State")
                ax.set_ylabel("Total Customers")
            case "3.3":
                ax.bar(results["NAME"], results["SUM"], color=self.colors)
                ax.set_title(GRAPH[query_num][1])
                ax.set_xlabel("Customer Name")
                ax.set_ylabel("Total Transaction Cost")
            case "5.1":
                ax.pie(results["Percent"])
            case "5.2":
                ax.pie(results["Total"])
            case "5.3":
                ax.bar(results["YEAR"], results["TOTAL"], color=self.colors)
            case "5.4":
                ax.bar(results["BRANCH_CITY"], results["TOTAL"], color=self.colors)
            
        canvas = FigureCanvasTkAgg(fig, master=top)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0)

        return results.to_string()
        
