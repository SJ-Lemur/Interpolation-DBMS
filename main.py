from tkinter import *
from FrontPage import *
from DBMS import *
from PolynomialInterpolation import *
import matplotlib.pyplot as plt



class Application:

    def __init__(self):
        """Initialize the entire application"""

        self.root = Tk()
        self.root.title("Polynomial Interpolation DBMS")

        RunFrontPage(self.root)
        self.addFrontPageButtons()

        self.root.mainloop()


    def addFrontPageButtons(self):
        
        Button(self.root, text="Show Data Record",padx=50).grid(row=1, column= 1)
        Button(self.root, text="Input Data",padx=50, command= self.show_input_data_options).grid(row=1, column= 3)
        Button(self.root, text="Show Interpolation Example",padx=50).grid(row=1, column =5)
    
    def show_input_data_options(self):
        """displays the options a user would like to use to input data"""
        self.clean_window()

        #now create option 
        self.canvas1 = Canvas(self.root, width =450, height=600, bg= "beige" )
        self.canvas1.grid(row=0, column=0)

        self.frame = Frame(self.root, width=450, height= 600)
        #self.canvas2 = Canvas(self.root, width=450, height=600, bg = "Alice blue")
        #self.canvas2.grid(row=0, column=1)
        self.frame.grid(row=0,column=1)

        self.addButtonOptions()


    def addButtonOptions(self):
        """This method adds buttons with their labels in some space
        """

        opt1 = Button(self.canvas1, text= "   Input Data    ", bg ="beige" , relief="ridge", command = self.inputDataField)
        opt2 = Button(self.canvas1, text= "Insert A CSV File", bg ="beige", relief= "ridge", command = self.readCSV_file)

        self.canvas1.create_window(225,250, window= opt1)
        self.canvas1.create_window(225,300, window= opt2 )


        label = Label(self.canvas1, text="Available Options", pady=10)
        self.canvas1.create_window(50,10, window=label)

    def readCSV_file(self):
        self.filenameInputield = Entry(self.frame)
        self.filenameInputield.pack(fill=BOTH, expand=True)
        self.filenameInputield.place(x=int(150), y= int(250))

        #Create a button to retrieve the input
        self.submitButton = Button(self.canvas1, text="Submit Data", command=self.captureDataFromFile)
        self.canvas1.create_window(225,550, window=self.submitButton)

    def captureDataFromFile(self):
        """captures data stored from text file in folder --textFiles-- """
        self.input_field = Text(self.frame, wrap="word", height =35, width = 60)

        with open("textFiles/"+str(self.filenameInputield.get()), "r") as file:
            #read a line from the file
            for line in file:
                self.input_field.insert("end", line)

        self.storeData()
    def inputDataField(self):
        """Creates entry field built using the Text widget"""
        """The user is expected to insert data in csv format"""

        
        self.input_field = Text(self.frame, wrap="word", height =35, width = 60)
        self.input_field.grid(row=0,column=0)
        
        #Now show a message on how the user will input the data
        label_text= "When you input your data you should write it in CSV format eg.\nNames, Surnames \nBen, Steeler \nBaby, Face\n... and so on \n \n NO SPACE BETWEEN A VALUES AND A COMMA"
        self.inputGuide = Label(self.canvas1, text=label_text, bg = "Light gray")
        self.canvas1.create_window(200,100, window= self.inputGuide)

        #Create a button to retrieve the input
        self.submitButton = Button(self.canvas1, text="Submit Data", command=self.storeData)
        self.canvas1.create_window(225,550, window=self.submitButton)

    
    def storeData(self):
        """Data needed to be store by the user is captured here"""
        self.Data = self.input_field.get("1.0", "end-1c")
        self.Data = self.Data.split("\n")
    
        DatabaseManagement(self.Data,"dataPoints")


        #define button for interpolation process
        interpolateB = Button(self.canvas1, text="Interpolate Data Points", command = self.performInterpolation)
        self.canvas1.create_window(230,500, window=interpolateB)

    def performInterpolation(self):
        k = LagrangePolynomial()
        polynomialDataPoints = k.generateDataPoints(-2,0.5, 100)

        #Show data graph
        x_values = [point[0] for point in polynomialDataPoints]
        y_values = [point[1] for point in polynomialDataPoints]

        plt.plot(x_values,y_values)
        xlabel, ylabel = self.Data[0].split(",")
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

        plt.title(str(ylabel)+" vs "+str(xlabel))

        plt.grid(True)
        plt.show()


    def clean_window(self):
        #delete all widgets
        self.root.after(0)
        for widget in self.root.winfo_children():
            widget.destroy()



Application()