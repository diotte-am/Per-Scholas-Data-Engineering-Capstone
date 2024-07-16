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
from schemas.month_schema import MONTHS

class report():
    def __init__(self, parent):
        self.parent = parent
        self.graph = graph()
        self.colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']
     
    def plot_graph(self, query_num):
        top= customtkinter.CTkToplevel(self.parent)
        top.geometry("800x600")
        top.title(GRAPH[query_num][1])
        frame = customtkinter.CTkFrame(top)
        frame.grid(row=0, column=0, sticky="nsew")

        top.grid_rowconfigure(0, weight=1)
        top.grid_columnconfigure(0, weight=1)

        results = self.graph.query(GRAPH[query_num][0])
        fig = Figure(figsize=(8, 6), dpi=100)
        ax = fig.add_subplot(111)
        match query_num:
            case "3.1":
                ax.bar(results["TRANSACTION_TYPE"], results["TOTAL"], color=self.colors)
                ax.set_title(GRAPH[query_num][1])
                ax.set_xlabel("Transaction Type")
                ax.set_ylabel("Total Transactions")
                ax.set_xticklabels(results['TRANSACTION_TYPE'], rotation=45, ha='center')
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
                ax.set_xticklabels(results['NAME'], rotation=45, ha='center')
            case "5.1":
                wedges, texts, autotexts = ax.pie(results["Percent"], labels=results['Result'], autopct='%1.1f%%', startangle=90, colors=['green', 'red'])
                ax.axis("equal")
                ax.set_title(GRAPH[query_num][1])
                for text in texts:
                    text.set_fontsize(12)
                for autotext in autotexts:
                    autotext.set_color("white")
                    autotext.set_fontsize(16)
            case "5.2":
                ax.pie(results["Total"])
                wedges, texts, autotexts = ax.pie(results["Total"], labels=results['Application_Status'], autopct='%1.1f%%', startangle=90, colors=['green', 'red'])
                ax.axis("equal")
                ax.set_title(GRAPH[query_num][1])
                for text in texts:
                    text.set_fontsize(12)
                for autotext in autotexts:
                    autotext.set_color("white")
                    autotext.set_fontsize(16)
                    
            case "5.3":
                bars = ax.barh(results["MONTH"], results["TOTAL"], color=self.colors)
                ax.set_xlabel('Transaction Volume')
                ax.set_ylabel('Month')
                ax.set_title(GRAPH[query_num][1])
                month_index = [MONTHS[int(x[4:]) - 1] for x in results["MONTH"]]
                ax.set_yticklabels(month_index, rotation=45, ha='right')
                for bar in bars:
                    ax.text(bar.get_width() - 0.1*bar.get_width(), bar.get_y() + bar.get_height()/2, 
                            '{:,}'.format(int(bar.get_width())), 
                            va='center', ha='left', fontsize=10)
            case "5.4":
                bars = ax.bar(results["BRANCH_CITY"], results["TOTAL"], color=self.colors)
                ax.set_xlabel('Branch')
                ax.set_ylabel('Total Dollar Value')
                ax.set_title(GRAPH[query_num][1])
                # Add value labels on top of the bars
                for bar in bars:
                    yval = bar.get_height()
                    plt.text(bar.get_x() + bar.get_width()/2, yval, '${:,.0f}'.format(yval), ha='center', va='bottom')

        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
    
        canvas.get_tk_widget().grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        return results.to_string()
        
