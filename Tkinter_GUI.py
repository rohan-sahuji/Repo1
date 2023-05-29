import tkinter as tk
import SQL_Connect

class School_Data:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('1200x700')

        self.home()

        self.root.mainloop()

    def home(self):

        self.label = tk.Label(self.root, text="Sample School Data", font=("Arial", 24))
        self.label.pack(padx=20, pady=20)

        self.textbox = tk.Text(self.root, height=5, font=("Arial", 12))
        self.textbox.pack(padx=10, pady=10)

        self.btnframe = tk.Frame(self.root)
        self.btnframe.columnconfigure(0, weight = 1)
        
        self.addbtn = tk.Button(self.btnframe, text="Add", font=("Arial", 16), command=self.add)
        self.addbtn.grid(row=0, column=0, sticky=tk.W + tk.E)

        self.search = tk.Button(self.btnframe, text="Search", font=("Arial", 16))
        self.search.grid(row=0, column=1, sticky=tk.W + tk.E)

        self.extra = tk.Button(self.btnframe, text="Extra", font=("Arial", 16))
        self.extra.grid(row=0, column=2, sticky=tk.W + tk.E)

        self.btnframe.pack(padx=10, pady=10)

        self.gui_elements = [self.label, self.textbox, self.btnframe]

    def add(self):
        self.gui_elements_remove(self.gui_elements)

        self.label = tk.Label(self.root, text="Add a new Entry", font=("Arial", 20))
        self.label.pack(padx=20, pady=20)

        self.addframe = tk.Frame(self.root)
        self.addframe.columnconfigure(0, weight = 1)
        self.addframe.columnconfigure(1, weight = 1)

        self.namelab = tk.Label(self.addframe, text="Name", font=("Arial", 14))
        self.namelab.grid(row=0, column=0, sticky=tk.W+tk.E)
        self.name = tk.Text(self.addframe, height=2, font=("Arial", 12))
        self.name.grid(row=1, column=0, sticky=tk.W+tk.E)
        
        self.agelab = tk.Label(self.addframe, text="Age", font=("Arial", 14))
        self.agelab.grid(row=0, column=1, sticky=tk.W+tk.E)
        self.age = tk.Text(self.addframe, height=2, font=("Arial", 12))
        self.age.grid(row=1, column=1, sticky=tk.W+tk.E)

        self.classlab = tk.Label(self.addframe, text="Class", font=("Arial", 14))
        self.classlab.grid(row=0, column=2, sticky=tk.W+tk.E)
        self.classl = tk.Text(self.addframe, height=2, font=("Arial", 12))
        self.classl.grid(row=1, column=2, sticky=tk.W+tk.E)

        self.addframe.pack(padx=10, pady=10)

        self.enter = tk.Button(self.btnframe, text="Add", font=("Arial", 16), command=SQL_Connect.connection_sql)
        self.enter.pack(padx=10, pady=10)

        self.gui_elements = [self.label, self.addframe, self.enter]


    def gui_elements_remove(self, gui_elements):

        for elements in gui_elements:
            elements.destroy() 

School_Data()
