import sqlite3
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class WrappingFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.bind('<Configure>', self.on_configure)

        self.items = []
        self.columns = 1

    def add_item(self, item):
        self.items.append(item)
        item.pack_forget()  # Hide the item initially
        self.reposition_items()

    def on_configure(self, event):
        self.reposition_items()

    def reposition_items(self):
        width = self.winfo_width()
        height = self.winfo_height()
        if width > 0 and height > 0:
            # Estimate number of columns
            item_width = self.items[0].winfo_reqwidth() if self.items else 1
            item_height = self.items[0].winfo_reqheight() if self.items else 1
            self.columns = max(1, width // item_width)

            # Clear the grid
            for item in self.items:
                item.grid_forget()

            # Place items in the grid, wrapping to the next column if bottom is reached
            current_height = 0
            column = 0
            for idx, item in enumerate(self.items):
                if current_height + item_height > height:
                    column += 1
                    current_height = 0

                item.grid(row=current_height // item_height, column=column, padx=5, pady=5, sticky='nw')
                current_height += item_height


class DisplayData():
    """displays all tables/data points in the ALLDATA.db file in databases folder"""

    def __init__(self, ROOT):

        self.root = ROOT

        self.clean_window()

        #define frames
        self.frame1 = tk.Frame(self.root, width=900, height= 302, bg="Seagreen2") #upper frame
        self.frame1.pack_propagate(False)

        self.frame2 = tk.Frame(self.root, width= 900, height= 605-302) #lower frame
        self.frame2.pack_propagate(False)

        self.frame1.pack()
        
        self.frame2.pack()

        #connect to the ALLDATA

        self.table_names = self.get_available_tables()

        self.display_table_names()


    def get_available_tables(self):
        """Returns names of all tables in ALLDATA.db"""

        #connect to the db file
        self.conn = sqlite3.connect("databases/ALLDATA.db")
        self.cursor = self.conn.cursor()

        #extract all db names
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.cursor.fetchall()

        return tables
    
    def display_table_names(self):
        """displays all stored tables in ALLDATA as buttons(relief = groove)"""

        #define the wrapping frame
        wrapping_frame = WrappingFrame(self.frame1)
        wrapping_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)


        for i in range(len(self.table_names)):
            wrapping_frame.add_item(ttk.Button(wrapping_frame, text=self.table_names[i], width=50, command=lambda i=i: self.show_table_data(self.table_names[i][0])))



    
    def show_table_data(self, name):
        """displays the data of the selected table 'name'  """
        
        self.cursor.execute("SELECT * FROM "+str(name))
        rows = self.cursor.fetchall()

        #define wrappable frame to display datapoints
        frame3 = tk.Frame(self.frame2)
        frame3.pack_propagate(False)
        frame3.config(width = 450, height=605-302)
        frame3.grid(row=0, column=0)

        wrapping_frame3 = WrappingFrame(frame3) # will only display datapoints
        wrapping_frame3.pack(fill=tk.BOTH, expand=True)

        #add datapoints to wrapping_frame3
        #also save the points in a list for sketching
        x_vals = []
        y_vals = []


        for row in rows:
            x = round(row[0], 3)
            y = round(row[1], 3)
            wrapping_frame3.add_item(ttk.Label(wrapping_frame3, text="("+str(x)+","+str(y)+")", borderwidth=2, relief="groove", width=10))

            x_vals.append(row[0])
            y_vals.append(row[1])
        
        frame4 = tk.Frame(self.frame2)
        frame4.pack_propagate(False)
        frame4.config(width = 450, height=605-302)
        frame4.grid(row=0, column=1)

        wrapping_frame4 = WrappingFrame(frame4)
        wrapping_frame4.pack(fill=tk.BOTH, expand=True)

        self.sketch_graph(x_vals, y_vals, wrapping_frame4)

        #wrapping_frame4.add_item(ttk.Label(wrapping_frame4, text=""))

    def sketch_graph(self, x_vals, y_vals, frame):
        """draws the graph of the datapoints selected"""
        #x_values = x_vals
        #y_values = y_vals

        # Create a matplotlib figure
        fig = Figure(figsize=(5, 5), dpi=100)
        plot = fig.add_subplot(1, 1, 1)
        
        # Plot the graph
        plot.plot(x_vals, y_vals, marker='o', linestyle='-')
        plot.set_title("X vs Y")
        plot.set_xlabel("X values")
        plot.set_ylabel("Y values")

        # Embed the plot in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)





    def clean_window(self):
        #delete all widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.configure(bg='#fff')
        self.root.update_idletasks()  # Make sure all pending tasks are complete
        self.root.geometry("900x605")



