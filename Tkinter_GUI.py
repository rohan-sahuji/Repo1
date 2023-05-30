# Import necessary Tkinter and sqlite3 libraries.
import tkinter as tk
import sqlite3
from sqlite3 import Error

# Making things object oriented, define a class.
class School_Data:
    # Constructor to initialize the GUI window
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('1200x700')

        self.home()

        self.root.mainloop()

    #The home Method contains all the widgets on the homescreen and their functions on the window
    def home(self):

        self.label = tk.Label(self.root, text="Sample School Data", font=("Arial", 24))
        self.label.pack(padx=20, pady=20)

        self.textbox = tk.Text(self.root, height=5, font=("Arial", 12))
        self.textbox.pack(padx=10, pady=10)

        self.btnframe = tk.Frame(self.root)
        self.btnframe.columnconfigure(0, weight = 1)
        
        self.addbtn = tk.Button(self.btnframe, text="Add", font=("Arial", 16), command=self.add)
        self.addbtn.grid(row=0, column=0, sticky=tk.W + tk.E)

        self.searchdb = tk.Button(self.btnframe, text="Search", font=("Arial", 16), command=self.search)
        self.searchdb.grid(row=0, column=1, sticky=tk.W + tk.E)

        self.extra = tk.Button(self.btnframe, text="Extra", font=("Arial", 16))
        self.extra.grid(row=0, column=2, sticky=tk.W + tk.E)

        self.btnframe.pack(padx=10, pady=10)

        # Collect all widgets in a list which will be passed to the destroy function to clear the screen
        self.gui_elements = [self.label, self.textbox, self.btnframe]

    #The add method contains all widgets and functions to be applied in 'ADD' screen of the 
    # window and is accessed after pressing Add button on the home screen
    def add(self):
        # Firsty remove widgets of the homescreen
        self.gui_elements_remove(self.gui_elements)

        self.label = tk.Label(self.root, text="Add a new Entry", font=("Arial", 20))
        self.label.pack(padx=20, pady=20)

        self.addframe = tk.Frame(self.root)
        self.addframe.columnconfigure(0, weight = 1)
        self.addframe.columnconfigure(1, weight = 1)

        self.namelab = tk.Label(self.addframe, text="Name", font=("Arial", 14))
        self.namelab.grid(row=0, column=0, sticky=tk.W+tk.E)
        self.name = tk.Text(self.addframe, height=1, font=("Arial", 12))
        self.name.grid(row=1, column=0, sticky=tk.W+tk.E)
        
        self.agelab = tk.Label(self.addframe, text="Age", font=("Arial", 14))
        self.agelab.grid(row=0, column=1, sticky=tk.W+tk.E)
        self.age = tk.Text(self.addframe, height=1, font=("Arial", 12))
        self.age.grid(row=1, column=1, sticky=tk.W+tk.E)

        self.classlab = tk.Label(self.addframe, text="Class", font=("Arial", 14))
        self.classlab.grid(row=0, column=2, sticky=tk.W+tk.E)
        self.classl = tk.Text(self.addframe, height=1, font=("Arial", 12))
        self.classl.grid(row=1, column=2, sticky=tk.W+tk.E)

        self.addframe.pack(padx=10, pady=10)

        self.enter = tk.Button(self.root, text="Add", font=("Arial", 16), command=self.connection_sql)
        self.enter.pack(padx=10, pady=10)

        self.gui_elements = [self.label, self.addframe, self.enter]

        self.back = tk.Button(self.root, text="Home", font=("Arial", 16), command=lambda: [self.gui_elements_remove(self.gui_elements), self.back.destroy(), self.home()])
        self.back.pack(padx=10, pady=10)

    def search(self):
        # Firsty remove widgets of the homescreen
        self.gui_elements_remove(self.gui_elements)

        self.label = tk.Label(self.root, text="Search an Entry", font=("Arial", 20))
        self.label.pack(padx=20, pady=20)

        self.searchframe = tk.Frame(self.root)
        self.searchframe.columnconfigure(0, weight = 1)
        self.searchframe.columnconfigure(1, weight = 1)

        self.attribute = tk.Label(self.searchframe, text="Search by", font=("Arial", 14))
        self.attribute.grid(row=0, column=0)
        self.sel_string = ""
        self.attribute_sel = tk.OptionMenu(self.searchframe, self.sel_string, "Name", "Age", "Class")
        self.attribute_sel.grid(row=1, column=0)
                                
        self.search_value = tk.Text(self.searchframe, height=1, font=("Arial", 12))
        self.search_value.grid(row=1, column=1)

        self.searchframe.pack(padx=10, pady=10)

        self.enter = tk.Button(self.root, text="Search", font=("Arial", 16))
        self.enter.pack(padx=10, pady=10)

        self.gui_elements = [self.label, self.searchframe, self.enter]

        self.back = tk.Button(self.root, text="Home", font=("Arial", 16), command=lambda: [self.gui_elements_remove(self.gui_elements), self.back.destroy(), self.home()])
        self.back.pack(padx=10, pady=10)

    # Method to clear screen of widgets on the window
    def gui_elements_remove(self, gui_elements):
        for elements in gui_elements:
            elements.destroy()

    # Method to connect to database and pass the entries to save
    def connection_sql(self):
        connection = None
        try:
            connection = sqlite3.connect(r"c:\Users\rsahu\Documents\git_files\Repo1\data.db")
            print('Connection established')
            data_entry = '''CREATE TABLE IF NOT EXISTS Stud_Data (Name TEXT, Age INT, Class INT)'''
            connection.execute(data_entry)
            data_insert = '''INSERT INTO Stud_Data (Name, Age, Class)
            VALUES (?,?,?)'''
            data_insert_tuple = (self.name.get('1.0', 'end-1c'), self.age.get('1.0', 'end-1c'), self.classl.get('1.0', 'end-1c'))
            print(data_insert_tuple)
            cursor = connection.cursor()
            cursor.execute(data_insert, data_insert_tuple)
            connection.commit()
            connection.close()
        
        except Error as e:
            print(e)

        return connection


School_Data()
