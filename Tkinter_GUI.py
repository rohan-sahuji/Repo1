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
        self.clear_screen()

        self.label = tk.Label(self.root, text="Sample School Data", font=("Arial", 24))
        self.label.pack(padx=20, pady=20)

        self.textbox = tk.Text(self.root, height=5, font=("Arial", 12))
        self.textbox.pack(padx=10, pady=10)

        self.add_button("Add", self.add)
        self.add_button("Search", self.search)
        self.add_button("Extra", self.extra)

    def add_button(self, text, command):
        button = tk.Button(self.root, text=text, font=("Arial", 16), command=command)
        button.pack(padx=10, pady=10)
        return button
    
    #The add method contains all widgets and functions to be applied in 'ADD' screen of the 
    # window and is accessed after pressing Add button on the home screen
    def add(self):
        # Firsty remove widgets of the homescreen
        self.clear_screen()

        self.label = tk.Label(self.root, text="Add a new Entry", font=("Arial", 20))
        self.label.pack(padx=20, pady=20)

        self.addframe = tk.Frame(self.root)
        self.addframe.pack(padx=10, pady=10)

        self.create_label_and_entry(self.addframe, "Name", 0, "Name", "")
        self.create_label_and_entry(self.addframe, "Age", 1, "Age", "")
        self.create_label_and_entry(self.addframe, "Class", 2, "Class", "")

        self.enter = self.add_button("Add", self.connection_add)

        self.back = tk.Button(self.root, text="Home", font=("Arial", 16), command=lambda: [self.clear_screen(), self.back.destroy(), self.home()])
        self.back.pack(padx=10, pady=10)

    def search(self):
        # Firsty remove widgets of the homescreen
        self.clear_screen()

        self.label = tk.Label(self.root, text="Search an Entry", font=("Arial", 20))
        self.label.pack(padx=20, pady=20)

        self.searchframe = tk.Frame(self.root)
        self.searchframe.pack(padx=10, pady=10)

        self.attribute = tk.Label(self.searchframe, text="Search by", font=("Arial", 14))
        self.attribute.grid(row=0, column=0)
        self.sel_string = tk.StringVar()
        self.attribute_sel = tk.OptionMenu(self.searchframe, self.sel_string, *["Name", "Age", "Class"])
        self.attribute_sel.grid(row=1, column=0)
                                
        self.search_value = tk.Text(self.searchframe, height=1, font=("Arial", 12))
        self.search_value.grid(row=1, column=1)

        self.search_button = self.add_button("Search", self.connection_search)

        self.back = tk.Button(self.root, text="Home", font=("Arial", 16), command=lambda: [self.clear_screen(), self.home()])
        self.back.pack(padx=10, pady=10)

    def create_label_and_entry(self, parent, text, row, entry_name, default_value):
        label = tk.Label(parent, text=text, font=("Arial", 14))
        label.grid(sticky=tk.W + tk.E)
        entry = tk.Text(parent, height=1, font=("Arial", 12))
        entry.insert("1.0", default_value)
        entry.grid(row=row, column=1, sticky=tk.W + tk.E)
        setattr(self, entry_name, entry)
  
    def create_connection(self):
        try:
            connection = sqlite3.connect(r"c:\Users\rsahu\Documents\git_files\Repo1\data.db")
            return connection

        except Error as e:
            print(e)


    # Method to connect to database and pass the entries to save
    def connection_add(self):
        try:
            connection = self.create_connection()

            data_entry = '''CREATE TABLE IF NOT EXISTS Stud_Data (name TEXT, age INT, class INT)'''
            connection.execute(data_entry)
            
            cursor = connection.cursor()
            data_insert = '''INSERT INTO Stud_Data (name, age, class) VALUES (?,?,?)'''
            data_insert_tuple = (
                self.Name.get('1.0', 'end-1c'),
                self.Age.get('1.0', 'end-1c'),
                self.Class.get('1.0', 'end-1c')
                )
            cursor.execute(data_insert, data_insert_tuple)
            connection.commit()
            connection.close()
        
        except Error as e:
            print(e)
    
    def connection_search(self):
        try:
            connection = self.create_connection()
            search_column = self.sel_string.get()
            search_querry = "SELECT * FROM Stud_Data WHERE {} = ?".format(search_column)
            cursor = connection.cursor()
            cursor.execute(search_querry, (self.search_value.get('1.0', 'end-1c'),))
            info = cursor.fetchall()

            self.disp_search_results(info)

            connection.commit()
            connection.close()
        
        except Error as e:
            print(e)
    
    def disp_search_results(self, info):
        
        self.label = tk.Label(self.root, text="Search Results", font=("Arial", 20))
        self.label.pack(padx=20, pady=20)

        self.dispframe = tk.Frame(self.root)
        self.dispframe.pack(fill = 'x')

        for i, row in enumerate(info, start=1):
            for j, value in enumerate(row):
                label = tk.Label(self.dispframe, text=value, font=("Arial", 14))
                label.grid(row=i, column=j)

            
    
    def extra(self):
        # Add your additional functionality here
        pass
    
    # Method to clear screen of widgets on the window
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()


School_Data()