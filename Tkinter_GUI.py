# Import necessary Tkinter and sqlite3 libraries.
import tkinter as tk
import sqlite3
from sqlite3 import Error
from PIL import Image, ImageTk
import tkinter.messagebox as messagebox

# Making things object oriented, define a class.
class School_Data:
    '''Constructor to initialize the GUI window'''
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('1200x700')
        self.connection = self.create_connection()
        self.home()
        self.root.mainloop()
        self.connection.close()

    def home(self):
        # Clear the screen and display the home screen
        self.clear_screen()

        # Create a menubar with two menus File and Action
        # From the File Menu the application can be closed
        # From the Action menu a message can be displayed.
        self.menubar = tk.Menu(self.root)

        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label='Close', command=self.close)
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Close without question', command=exit)

        self.actionmenu = tk.Menu(self.menubar, tearoff=0)
        self.actionmenu.add_command(label='Show Message', command=self.show_message)

        self.menubar.add_cascade(menu = self.filemenu, label='File')
        self.menubar.add_cascade(menu = self.actionmenu, label='Action')

        self.root.config(menu = self.menubar)

        # Create a label for the application title
        self.label = tk.Label(self.root, text="Sample School Data", font=("Calibri", 24))
        self.label.pack(padx=20, pady=20)

        # Load and display an image
        image = Image.open("school_image.jpg")
        image = image.resize((800,300))
        self.photo = ImageTk.PhotoImage(image)
        image_label = tk.Label(self.root, image=self.photo)
        image_label.pack(padx=10, pady=10)

        # Create a frame for the buttons
        self.homeframe = tk.Frame(self.root)
        self.homeframe.pack(padx=20, pady=20)

        # Add buttons for Add, Search, and Extra functionality
        self.add_button_in_frame(self.homeframe,"Add",0,0, self.add)
        self.add_button_in_frame(self.homeframe,"Search",0,1, self.search)
        self.add_button_in_frame(self.homeframe,"Extra",0,2, self.extra)

    def add_button_in_frame(self, parent, text, row, col, *commands):
        """
        Create a button and place it in a frame within the parent widget.
        Args:
            parent (tk.Widget): The parent widget.
            text (str): The text to display on the button.
            row (int): The row number within the parent's grid layout.
            col (int): The column number within the parent's grid layout.
            *commands (callable): The command(s) to associate with the button.
        Returns:
            tk.Button: The created button.
        """
        button = tk.Button(parent, text=text, font=("Arial", 14))
        button.grid(row=row, column=col)
        for cmd in commands:
            button.config(command = lambda c=cmd: c())
        return button

    def add_button(self, text, command):
        """
        Create a button and place it in the root window with standard padding.
        Args:
            text (str): The text to display on the button.
            command (callable): The command(s) to associate with the button.
        """
        button = tk.Button(self.root, text=text, font=("Arial", 14), command=command)
        button.pack(padx=10, pady=10)
    
    def add(self):
        """
        Displays the screen for adding a new entry.
        """
        self.clear_screen()

        # Create a label for the add screen title
        self.label = tk.Label(self.root, text="Add a new Entry", font=("Arial", 20))
        self.label.pack(padx=20, pady=20)

        self.addframe = tk.Frame(self.root)
        self.addframe.pack(padx=10, pady=10)

        # Create input fields for name, age, and class
        self.create_label_and_entry(self.addframe, "Name", 0, "Name", "")
        self.create_label_and_entry(self.addframe, "Age", 1, "Age", "")
        self.create_label_and_entry(self.addframe, "Class", 2, "Class", "")

        self.addbtnframe = tk.Frame(self.root)
        self.addbtnframe.pack(padx=10, pady=10)

        # Add buttons to add the entry and return to the home screen
        self.add_button_in_frame(self.addbtnframe,"Add",0,1, self.connection_add)
        self.add_button_in_frame(self.addbtnframe,"Home",0,2, self.home)

    # Method to connect to database and pass the entries to save
    def connection_add(self):
        """
        Add the new entry to the SQLite database.
        """
        try:
            data_entry = '''CREATE TABLE IF NOT EXISTS Stud_Data (name TEXT, age INT, class INT)'''
            self.connection.execute(data_entry,)
            data_insert = '''INSERT INTO Stud_Data (name, age, class) VALUES (?,?,?)'''
            data_insert_tuple = (
                self.Name.get('1.0', 'end-1c'),
                self.Age.get('1.0', 'end-1c'),
                self.Class.get('1.0', 'end-1c')
                )
            # If any space is left blank, prompt user to enter all details else, execute the data entry
            # and display respective messages.
            if '' in data_insert_tuple:
                messagebox.showinfo(title='Error', message='Kindly fill in all the details')
            else:
                cursor = self.connection.cursor()
                cursor.execute(data_insert, data_insert_tuple)
                self.connection.commit()
                
                messagebox.showinfo(title='Congratulations!', message='Entry added Successfully!')
                self.clear_text(self.addframe)
        
        except Error as e:
            print(e)
            
    def search(self):
        """
        Displays the screen for searching an entry.
        """
        self.clear_screen()

        # Create a label for the search screen title
        self.label = tk.Label(self.root, text="Search an Entry", font=("Arial", 20))
        self.label.pack(padx=20, pady=20)

        # Create frame for search input field
        self.searchframe = tk.Frame(self.root)
        self.searchframe.pack(padx=10, pady=10)

        self.attribute = tk.Label(self.searchframe, text="Search by", font=("Arial", 14))
        self.attribute.grid(row=0, column=0)

        # Define a variable to store the attribute name selected by user by which user wants to search
        self.sel_string = tk.StringVar()
        # Define option menu to select Name, Age or Class and store value in variable
        self.attribute_sel = tk.OptionMenu(self.searchframe, self.sel_string, *["Name", "Age", "Class"])
        self.attribute_sel.grid(row=1, column=0)
                                
        # Text input by user which will be searched in the database
        self.search_value = tk.Text(self.searchframe, height=1, font=("Arial", 12))
        self.search_value.grid(row=1, column=1)

        # Add buttons to search the entry and return to the home screen
        self.add_button("Search", self.connection_search)
        self.add_button("Home", self.home)

    def connection_search(self):
        """
        Search for entries in the SQLite database.
        """
        try:
            # Search user given text input in user selected attribute column of database
            search_column = self.sel_string.get()
            search_querry = "SELECT * FROM Stud_Data WHERE {} = ?".format(search_column)
            cursor = self.connection.cursor()

            # if text input is left blank, prompt user to enter a text
            # else store search results from database in global variable self.info
            if self.search_value.get('1.0', 'end-1c') == '':
                messagebox.showinfo(title='Error!', message='Kindly enter value for search')
            else:
                cursor.execute(search_querry, (self.search_value.get('1.0', 'end-1c'),))
                self.info = cursor.fetchall()
                self.disp_search_results(self.info)
                self.connection.commit()
        
        except Error as e:
            print(e)
            
    def disp_search_results(self, info):

        '''Displays all the results of search command in database
        Args:
            info: list of all the rows from database that correspond to user search
        '''

        # Clear any previously displayed search results
        self.clear_search_results()

        # Create label for results of search
        self.label = tk.Label(self.root, text="Search Results", font=("Arial", 20))
        self.label.pack(padx=20, pady=20)
        
        # Create frame to display all matching results
        self.dispframe = tk.Frame(self.root)
        self.dispframe.pack(fill = 'y')

        # Create a variable to store the value of radiobutton
        self.rbvar = tk.StringVar()
        
        # if no matching result is found, display No Results found!
        # else display results
        if len(info) == 0:
            self.label_nor = tk.Label(self.root, text="No Results found!", font=("Arial", 16))
            self.label_nor.pack(padx=20, pady=20)

        # Create radiobutton for each row of result
        # if a row is selected, option to edit or delete the row pops up
        else:
            for i, row in enumerate(info, start=1):
                self.rb = tk.Radiobutton(self.dispframe, variable=self.rbvar, value = i, command=self.enable_options)
                self.rb.grid(row=i, column=0)
                for j, val in enumerate(row):
                    label = tk.Label(self.dispframe, text=val, relief=tk.RAISED, width=15, font=("Arial", 14))
                    label.grid(row=i, column=j+1, sticky= tk.W + tk.E)
                
    def enable_options(self):
        '''Method to display Edit and Delete buttons only on selection of a row'''
        present = False
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Button) and (widget.cget('text') == 'Edit'):
                present = True
        if present == False:
            # If buttons not already present, create frame for buttons
            self.searchbtnframe = tk.Frame(self.root)
            self.searchbtnframe.pack(padx=10,pady=10)
            self.add_button_in_frame(self.searchbtnframe, 'Edit', 0,0, self.edit)
            self.add_button_in_frame(self.searchbtnframe, 'Delete', 0,1, self.delete_entry)
            
    def edit(self):
        ''' Edit the selected row in database'''

        # Extracting details of selected row
        selected_row = int(self.rbvar.get()) -1
        (name, age, classl) = self.info[selected_row]

        # Clear screen for Edit screen
        self.clear_screen()

        # Create label for Edit screen
        self.label = tk.Label(self.root, text="Update an Entry", font=("Arial", 20))
        self.label.pack(padx=20, pady=20)

        # Create frame for text entries that should replace the existing entry
        self.editframe = tk.Frame(self.root)
        self.editframe.pack(padx=10, pady=10)

        self.create_label_and_entry(self.editframe, "Name", 0, "Name", "")
        self.create_label_and_entry(self.editframe, "Age", 1, "Age", "")
        self.create_label_and_entry(self.editframe, "Class", 2, "Class", "")

        # Create a frame for buttons to execute the edit function or cancel the process
        self.editbtnframe = tk.Frame(self.root)
        self.editbtnframe.pack(padx=10, pady=10)

        self.add_button_in_frame(self.editbtnframe,"Update",0,1, lambda: self.edit_entry(self.info[int(self.rbvar.get()) - 1]))
        self.add_button_in_frame(self.editbtnframe,"Cancel",0,2, self.clear_text)
        self.add_button_in_frame(self.editbtnframe,"Back",0,3, self.search)
        self.add_button_in_frame(self.editbtnframe,"Home",0,4, self.home)
    
    def edit_entry(self, entry):
        ''' Method to execute the edit in Sqlite database'''
        edit_query = '''UPDATE Stud_Data SET name=?, age=?, class=? WHERE name=? AND age=? AND class=?'''
        data_edit_tuple = (self.Name.get('1.0', 'end-1c'), self.Age.get('1.0', 'end-1c'), self.Class.get('1.0', 'end-1c'))

        # If any field is left blank, prompt user to fill all details
        if '' in data_edit_tuple:
            messagebox.showinfo(title='Error', message='Kindly fill in all the details')
        else:
            cursor = self.connection.cursor()
            cursor.execute(edit_query,
                           (self.Name.get('1.0', 'end-1c'),
                           self.Age.get('1.0', 'end-1c'),
                           self.Class.get('1.0', 'end-1c'),
                           entry[0], entry[1], entry[2]))
            self.connection.commit()
            messagebox.showinfo(title='Congratulations!', message='Entry updated Successfully!')
            # Clear the text fields after operation
            self.clear_text(self.editframe)

    def delete_entry(self):
        '''Delete the selected entry'''
        # Confirm if user really wants to delete the entry
        sure = messagebox.askyesnocancel(title='Delete?', message='''Are you sure you want to delete this entry?''')
        if sure == True:
            cursor = self.connection.cursor()

            selected_row = int(self.rbvar.get()) -1
            (name, age, classl) = self.info[selected_row]

            delete_query = '''DELETE from Stud_Data WHERE
            name = ? AND age = ? AND class = ?'''
            cursor.execute(delete_query, (name, age, classl))
            self.connection.commit()

            messagebox.showinfo(title="Success", message="Entry deleted successfully!")
            self.connection_search()
            
    def create_label_and_entry(self, parent, text, row, entry_name, default_value):
        """
        Create a label, an entry field, and place them in a frame within the parent widget.

        Args:
            parent (tk.Widget): The parent widget.
            label_text (str): The text to display on the label.
            row (int): The row number within the parent's grid layout.
            entry_placeholder (str): The placeholder text for the entry field.
            entry_default (str): The default value for the entry field.

        Returns:
            tuple: A tuple containing the label and entry field widgets.
        """
        label = tk.Label(parent, text=text, font=("Arial", 14))
        label.grid(sticky=tk.W + tk.E)
        entry = tk.Text(parent, height=1, font=("Arial", 12))
        entry.bind("<KeyPress>", self.shortcut)
        entry.insert("1.0", default_value)
        entry.grid(row=row, column=1, sticky=tk.W + tk.E)
        setattr(self, entry_name, entry)
  
    def clear_text(self, frame):
        ''' Method to clear text fields if present on the screen'''
        text_entry = [widget for widget in frame.winfo_children() if isinstance(widget, tk.Text)]
        for element in text_entry:
            element.delete('1.0', 'end')
    
    def create_connection(self):
        '''Method to create connection with the Sqlite database'''
        try:
            connection = sqlite3.connect(r"c:\Users\rsahu\Documents\git_files\Repo1\data.db")
            return connection

        except Error as e:
            print(e)

    def clear_search_results(self):
        ''' Method to refresh and clear previously displyed results in case of new search or deleted entry'''
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame) and widget != self.searchframe:
                widget.destroy()
            elif isinstance(widget, tk.Label) and widget.cget('text') == 'Search Results':
                widget.destroy()
    
    def shortcut(self, event):
        ''' Method to enable function through shortcut keys'''
        #print(event.keysym, event.state)
        if event.keysym == 'Return':
            self.connection_add()

        if event.keysym == 'Tab':
            current_widget = event.widget
            current_widget.tk_focusNext().focus()
            return 'break'
        
    
    def extra(self):
        """
        Displays the screen for extra functionality (placeholder).
        """
        self.clear_screen()

        # Create a label for the extra screen title
        self.label = tk.Label(self.root, text="Extra Functionality", font=("Arial", 20))
        self.label.pack(padx=20, pady=20)

        self.extrabtnframe = tk.Frame(self.root)
        self.extrabtnframe.pack(padx=10, pady=10)

        # Add button to go back to the home screen
        self.add_button_in_frame(self.extrabtnframe, "Back", 0, 0, self.home)
    
    def clear_screen(self):
        '''Method to clear screen of widgets on the window'''
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_message(self):
        '''Method to show message when asked from Actionmenu'''
        messagebox.showinfo(title='Information', message='This is a sample GUI for entry of data of students in a school')

    def close(self):
        '''Method to kill the application window'''
        if messagebox.askyesno(title="Quit?", message='Do you really want to quit?'):
            self.root.destroy()

# Instantiate the School_Data class to start the application.
if __name__ == '__main__':
    School_Data()