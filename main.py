from tkinter import *
from FrontPage import *
from DBMS import *
from PolynomialInterpolation import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from DescriptionPage import *



class Application:
    

    def __init__(self):
        """Initialize the entire application"""
        self.destroy_frame = False
        self.root = Tk()
        self.root.title("Polynomial Interpolation DBMS")

        RunFrontPage(self.root)
        self.addFrontPageButtons()

        self.root.mainloop()
        
        

    def addFrontPageButtons(self):
        
        Button(self.root, text="Show Data Record",padx=50).grid(row=1, column= 1)
        Button(self.root, text="Input Data",padx=50, command= self.show_input_data_options).grid(row=1, column= 3)
        Button(self.root, text="Show Interpolation Example", command= self.showInterpolationExample ,padx=50).grid(row=1, column =5)
    
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
        self.show_input_data_options()
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
        self.show_input_data_options()
        
        self.input_field = Text(self.frame, wrap="word", height =35, width = 60)
        self.input_field.grid(row=0,column=0)
        
        #Now show a message on how the user will input the data
        label_text= "When you input your data you should write it in CSV format eg.\nNames, Surnames \nBen, Steeler \nBaby, Face\n... and so on \n \n NO SPACE BETWEEN A VALUES AND A COMMA"
        self.inputGuide = Label(self.canvas1, text=label_text, bg = "Light gray")
        self.canvas1.create_window(200,100, window= self.inputGuide)

        #Create a button to retrieve the input
        self.destroy_frame = True
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
        
        x_values = [point[0] for point in polynomialDataPoints]
        y_values = [point[1] for point in polynomialDataPoints]

        self.tempData = [x_values, y_values] # calculated data temporarly stored | will be permanetely stored when the user wants to

        fig, ax = plt.subplots()
        ax.plot(x_values,y_values)
        ax.set_title("Example Graph")
        
        if self.destroy_frame:
            self.frame.destroy()
            self.frame = Frame(self.root, width=450, height= 600)
            self.frame.grid(row=0,column=1)

        #embed the graph to frame
        canvas = FigureCanvasTkAgg(fig, master=self.frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)

        #define button for saving the data
        saveButton = Button(self.canvas1, text="Save Data", command= self.saveData)
        self.canvas1.create_window(230,450, window=saveButton)

    def saveData(self):
            
            #first clean the LEFT PANE of the program
            self.frame.destroy()
            self.frame = Frame(self.root, width=450, height= 600)
            self.frame.grid_propagate(False)
            self.frame.grid(row=0,column=1)

            #Now ask the user the name of the table they want to save
            name_prompt = Label(self.frame, text="INSERT A UNIQUE NAME FOR THE TABLE")
            name_prompt.grid(row=0, column=0)

            # ADD an entry field and a button to confirm the name
            self.table_name = Entry(self.frame)
            self.table_name.grid(row=1,column=0)

            confirm_button = Button(self.frame, text="confirm name", command = self.storeToDB)
            confirm_button.grid(row=2, column=0)

            # Configure the frame's grid to prevent resizing
            self.frame.grid_rowconfigure(0, weight=1)
            self.frame.grid_columnconfigure(0, weight=1)
    
    def storeToDB(self):
        tempdata = [] #stores tuple (x,y)

        for i in range(len(self.tempData[0])):
            tempdata.append((self.tempData[0][i], self.tempData[1][i]))

        DatabaseManagement.saveToDatabase(self.table_name.get(), tempdata)

        self.frame.destroy()
        self.frame = Frame(self.root, width=450, height= 600)
        self.frame.grid(row=0,column=1)
    

    def showInterpolationExample(self):
        self.clean_window()
        PolynomialInterpolationPage(self.root)
        self.root.geometry("900x605")

        #display the html page
    def clean_window(self):
        #delete all widgets
        self.root.after(0)
        for widget in self.root.winfo_children():
            widget.destroy()



Application()
