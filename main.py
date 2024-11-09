#import tkinter as tk
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import sqlite3
import time
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import random as r
from datetime import datetime
import math
from tkcalendar import DateEntry
from tkinter import messagebox




conn = sqlite3.connect('AdjustMaths.db')
cursor = conn.cursor()

# making the students table
create_students_table = '''
CREATE TABLE IF NOT EXISTS Students (
    StudentID INTEGER PRIMARY KEY AUTOINCREMENT,
    ClassID INTEGER,
    FirstName TEXT,
    LastName TEXT,
    DoB Date,
    Username TEXT,
    Password TEXT,
    FOREIGN KEY (ClassID) REFERENCES Class(ClassID)
)
'''

# making the teachers table
create_teachers_table = '''
CREATE TABLE IF NOT EXISTS Teachers (
    TeacherID INTEGER PRIMARY KEY AUTOINCREMENT,
    Title TEXT,
    FirstName TEXT,
    LastName TEXT,
    Username TEXT,
    Password TEXT,
    DoB Date
)
'''

# making the class table
create_class_table = '''
CREATE TABLE IF NOT EXISTS Class (
    ClassID INTEGER PRIMARY KEY AUTOINCREMENT,
    TeacherID INTEGER,
    ClassName TEXT,
    FOREIGN KEY (TeacherID) REFERENCES Teachers(TeacherID)
)
'''

# making the topic table
create_topic_table = '''
CREATE TABLE IF NOT EXISTS Topic (
    TopicID INTEGER PRIMARY KEY,
    TopicName TEXT
)
'''

# making the result table
create_result_table = '''
CREATE TABLE IF NOT EXISTS Result (
    ResultID INTEGER PRIMARY KEY AUTOINCREMENT,
    QuestionID INTEGER,
    StudentID INTEGER,
    TopicID INTEGER,
    Correct INTEGER,
    Grade INTEGER,
    Date TEXT,
    FOREIGN KEY (QuestionID) REFERENCES Question(QuestionID),
    FOREIGN KEY (StudentID) REFERENCES Students(StudentID),
    FOREIGN KEY (TopicID) REFERENCES Topic(TopicID)
)
'''
# SQLite does not have boolean as a data type, so Correct will be an INTEGER, either 0 for wrong, or 1 for right


create_question_table = '''
CREATE TABLE IF NOT EXISTS Question (
    QuestionID INTEGER PRIMARY KEY AUTOINCREMENT,
    QuestionText TEXT,
    StudentOption TEXT,
    CorrectOption TEXT
    )
'''


cursor.execute(create_students_table)
cursor.execute(create_teachers_table)
cursor.execute(create_class_table)
cursor.execute(create_topic_table)
cursor.execute(create_result_table)
cursor.execute(create_question_table)




# tables = ["Students", "Teachers", "Class", "Topic", "Result", "Leaderboard", "Question"]
# tables = ["Leaderboard"]
# tables_to_delete = [tables]




# for table_name in tables:
#     drop_table_query = f"DROP TABLE IF EXISTS {table_name}"
#     cursor.execute(drop_table_query)
#     conn.commit()


# conn.commit()



resolutionwindow = ctk.CTk()
resolutionwindow.withdraw()  # Hide the window


screen_width = resolutionwindow.winfo_screenwidth() # Get the screen resolution
screen_height = resolutionwindow.winfo_screenheight()



class AdjustMaths:
    def __init__(self):
        self.conn = conn
        self.cursor = self.conn.cursor()

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("dark-blue") # dark-blue, blue, green
        ctk.set_widget_scaling(1.5)
        ctk.set_window_scaling(1.5)


        self.window = ctk.CTk() # making a window to put all the information on
        self.window.geometry(f"{1280}x{720}") # setting a window size, this is adjustable.


        self.window.title("Welcome to AdjustMaths!")
        self.font_settings = ("Times", 24, 'bold')


        self.login_page() # calling the first method, the login page.


    def page_clearer(self, window):
        for widget in window.winfo_children():
            widget.destroy()


    def login_page(self):
        self.page_clearer(self.window)

        # Set window size

        # mainframe
        self.allframe = ctk.CTkFrame(self.window, fg_color="#d0d0d0")  # darkish grey
        self.allframe.pack(pady=20, padx=20, fill="y", expand=True)

        # Welcome label
        welcome = ctk.CTkLabel(self.allframe, text="AdjustMaths!", font=("Times", 30, 'bold'), text_color="blue")
        welcome.pack(pady=20)

        # Username entry
        self.u_enter = ctk.CTkEntry(self.allframe, placeholder_text="Username")
        self.u_enter.pack(pady=10, padx=20, fill="x")

        # Password entry
        self.P_enter = ctk.CTkEntry(self.allframe, placeholder_text="Password", show="*")
        self.P_enter.pack(pady=10, padx=20, fill="x")


        self.ShowPassword = ctk.CTkCheckBox(self.allframe, text = "Show Password", command = lambda: self.P_enter.configure(show="" if self.P_enter.cget("show") == "*" else "*"))
        self.ShowPassword.pack(pady=10, padx=20)

        # Login button
        login = ctk.CTkButton(self.allframe, text="Login", command=self.login_check)
        login.pack(pady=20)

        # Sign up buttons
        button_frame = ctk.CTkFrame(self.allframe, fg_color="#d0d0d0")  # Create inner for sign-up buttons
        button_frame.pack(pady=10, fill="x")

        t_sign_upbutton = ctk.CTkButton(button_frame, text="Teacher Sign up", command=self.teacher_signup)
        t_sign_upbutton.pack(side="left", padx=(20, 10), pady=10)

        s_sign_upbutton = ctk.CTkButton(button_frame, text="Student Sign up", command=self.student_signup)
        s_sign_upbutton.pack(side="right", padx=(10, 20), pady=10)



    def login_check(self):
        # Getting the username and password from the input boxes
        username = self.u_enter.get()
        password = self.P_enter.get()

        # Reset the background color for all fields
        self.u_enter.configure(fg_color="white")
        self.P_enter.configure(fg_color="white")


        # Check if the username field is empty
        if username == "":
            self.u_enter.configure(fg_color="#f8d7da")  # Pastel red color

        # Check if the password field is empty
        if password == "":
            self.P_enter.configure(fg_color="#f8d7da")  # Pastel red color


        # Determines if the user is a student or teacher
        if username[0].isdigit():
            user_search = "SELECT Password FROM Students WHERE Username = ?"
            self.cursor.execute(user_search, (username,))
            password_from_table = self.cursor.fetchone()
            student = True
        else:
            teacher_search = "SELECT Password FROM Teachers WHERE Username = ?"
            self.cursor.execute(teacher_search, (username,))
            password_from_table = self.cursor.fetchone()
            student = False

        # Check if the password is correct
        if password_from_table is not None:
            if password == password_from_table[0]:
                if student:
                    Student(self.window, self.cursor, username)  # Navigate to student home screen
                else:
                    Teacher(self.window, self.cursor, username)  # Navigate to teacher home screen
            else:

                self.P_enter.configure(fg_color="#f8d7da")  # Highlight password field
                
        else:
            self.u_enter.configure(fg_color="#f8d7da")  # Highlight username field

    



   




    def wrong_info(self, Text): # makes a popup that the wrong password has been entered
        popup = ctk.CTkToplevel() # will show up above the current window
        popup.title(f"{Text}")


        popup.configure(bg = "#000000", pady = 20) # setting some coloours
        popup.geometry("300x120") #] size of the window
        label = ctk.CTkLabel(popup, text=f"{Text}" ) # text for popup
        label.pack()


        popup.focus() # puts into the top level properly


        close_button = ctk.CTkButton(popup, text="Close" , command=popup.destroy) # button to close the popup
        close_button.pack(pady=10)




    def student_signup(self): # needs code


        self.page_clearer(self.window)


       # Welcome to page label
        welcome = ctk.CTkLabel(self.window, text="Student Sign Up Page", font = (("Times"), 26, 'bold', "underline") , width=30, height=3, text_color = "blue") # setting a large title
        welcome.pack(pady=25)

        # making a larger frame for all the entries to go into
        input_frame = ctk.CTkFrame(self.window) # making a frame in which the username and password can be placed
        input_frame.pack(pady=(20, 5))


        # Entries for first name, last name, date of birth
        self.fname_enter = ctk.CTkEntry(input_frame ,  width=200, placeholder_text = "First Name")
        self.fname_enter.grid(row=0, column=1, padx = (20,5) ,pady = (20,10), sticky = "ew") # sticky goes ew, meaning east west expansion for when the window is expanded.


        self.lname_enter = ctk.CTkEntry(input_frame ,  width=200, placeholder_text = "Last Name")
        self.lname_enter.grid(row=0, column=2, padx = (5,20) ,pady = (20,10), sticky = "ew") # sticky goes ew, meaning east west expansion for when the window is expanded.


        def DeleteButton(): # function which deletes the display button when clicked
            self.placeholder_button.destroy()
            self.dob_enter.grid(row=1, column=1, padx=(20, 5), pady=10, sticky="ew")



        self.dob_enter = DateEntry(input_frame, width = 20, height = 4, date_pattern = "y-mm-dd", foreground = "white", borderwidth = 2, year = 2000)
        self.dob_enter.grid(row=1, column=1, padx=(20, 5), pady=10, sticky="ew")

        self.placeholder_button = tk.Button(input_frame, text="Date of Birth", fg="grey", command= DeleteButton)
        self.placeholder_button.grid(row=1, column=1, padx=(20, 5), pady=10, sticky="ew")


        class_names = [] # list which will contain all class names
        cursor.execute("SELECT ClassName FROM Class") 
        c = cursor.fetchall() # getting all the classnames

        for row in c:
            class_names.append(row[0]) # appending to end of lsit

        # to choose which class they want to be in
        self.newclass_box = ctk.CTkComboBox(input_frame, values = class_names, state = "readonly") 
        self.newclass_box.grid(row=1, column=2, padx = 10 ,pady = 10, sticky = "ew", ) # sticky goes ew, meaning east west expansion for when the window is expanded.
        self.newclass_box.set("Class Name")


        self.pass_enter = ctk.CTkEntry(input_frame ,  width=200,  placeholder_text = "Password", show = "*")
        self.pass_enter.grid(row=2, column=1, padx = (20,5) ,pady = 10, sticky = "ew") # sticky goes ew, meaning east west expansion for when the window is expanded.#


        self.repass_enter = ctk.CTkEntry(input_frame ,  width=200, placeholder_text = "Re-enter" , show = "*")
        self.repass_enter.grid(row=2, column=2, padx = (5,20) ,pady = 10, sticky = "ew") # sticky goes ew, meaning east west expansion for when the window is expanded.

        self.ShowPasswords = ctk.CTkCheckBox(
            input_frame, 
            text="Show Passwords", 
            command=lambda: [
                self.pass_enter.configure(show="" if self.pass_enter.cget("show") == "*" else "*"),
                self.repass_enter.configure(show="" if self.repass_enter.cget("show") == "*" else "*")
            ]
        )
        self.ShowPasswords.grid(row=3, columnspan=4, pady=20)

        # Signup and Back buttons
        signup_button = ctk.CTkButton(input_frame, text="Sign Up!",  command= lambda: self.signup_check("Student"))
        signup_button.grid(row=4, columnspan=4, pady=20)


        back_button = ctk.CTkButton(self.window, text = "Back", command = self.login_page, fg_color = "#4169E1")
        back_button.pack(side = "left", padx= 15)




    def teacher_signup(self):


        self.page_clearer(self.window)


        welcome = ctk.CTkLabel(self.window, text="Teacher Sign Up Page", font = (("Times"), 26, 'bold', "underline") , width=30, height=3, text_color = "blue") # setting a large title
        welcome.pack(pady=25)


        input_frame = ctk.CTkFrame(self.window) # making a frame in which the username and password can be placed
        input_frame.pack(pady=20)



        # entry for first name
        self.fname_enter = ctk.CTkEntry(input_frame ,  width=200, placeholder_text = "First Name")
        self.fname_enter.grid(row=0, column=1, padx = (20,5) ,pady = (20,10), sticky = "ew") # sticky goes ew, meaning east west expansion for when the window is expanded.



        # entry for last name
        self.lname_enter = ctk.CTkEntry(input_frame ,  width=200, placeholder_text = "Last Name")
        self.lname_enter.grid(row=0, column=2, padx = (5,20) ,pady = (20,10), sticky = "ew") # sticky goes ew, meaning east west expansion for when the window is expanded.

        
        # date entry function 

        def DeleteButton(): # function which deletes the display button when clicked
            self.placeholder_button.destroy()
            self.dob_enter.grid(row=1, column=1, padx=(20, 5), pady=10, sticky="ew")


        # enter date of birth
        self.dob_enter = DateEntry(input_frame, width = 20, height = 4, date_pattern = "y-mm-dd", foreground = "white", borderwidth = 2, year = 2000)
        self.dob_enter.grid(row=1, column=1, padx=(20, 5), pady=10, sticky="ew")

        # placeholder to show date of birth entry
        self.placeholder_button = tk.Button(input_frame, text="Date of Birth", fg="grey", command= DeleteButton)
        self.placeholder_button.grid(row=1, column=1, padx=(20, 5), pady=10, sticky="ew")


        # title of teacher entry
        self.title_enter = ctk.CTkEntry(input_frame ,  width=200, placeholder_text = "Title")
        self.title_enter.grid(row=1, column=2, padx = (5,20) ,pady = 10, sticky = "ew", ) # sticky goes ew, meaning east west expansion for when the window is expanded.




        self.pass_enter = ctk.CTkEntry(input_frame ,  width=200,  placeholder_text = "Password", show = "*")
        self.pass_enter.grid(row=2, column=1, padx = (20,5) ,pady = 10, sticky = "ew") # sticky goes ew, meaning east west expansion for when the window is expanded.#




        self.repass_enter = ctk.CTkEntry(input_frame ,  width=200, placeholder_text = "Re-enter" , show = "*")
        self.repass_enter.grid(row=2, column=2, padx = (5,20) ,pady = 10, sticky = "ew") # sticky goes ew, meaning east west expansion for when the window is expanded.

        # checkbox 
        self.ShowPasswords = ctk.CTkCheckBox(
            input_frame, 
            text="Show Passwords", 
            command=lambda: [
                self.pass_enter.configure(show="" if self.pass_enter.cget("show") == "*" else "*"),
                self.repass_enter.configure(show="" if self.repass_enter.cget("show") == "*" else "*")
            ]
        )
        self.ShowPasswords.grid(row=3, columnspan=4, pady=20)

        # Signup and Back buttons
        signup_button = ctk.CTkButton(input_frame, text="Sign Up!",  command= lambda: self.signup_check("Teacher"))
        signup_button.grid(row=4, columnspan=4, pady=20)


       
        back_button = ctk.CTkButton(self.window, text = "Back", command = self.login_page, fg_color="#4169E1")
        back_button.pack(side = "left", padx= 15)


       






    def signup_check(self, student_or_teacher):
        firstname = ""
        lastname = ""
        dob = ""
        title = "ReallQuiteUnlucky123"
        password = ""
        reentry = ""

        print (student_or_teacher)

        firstname = self.fname_enter.get() # since all this data is emptied every time the user leaves each signup page, I don't need to have seperate inputs for teacher and students for the common data between them.
        lastname = self.lname_enter.get()
        dob = self.dob_enter.get()
        password = self.pass_enter.get()
        reentry = self.repass_enter.get()
        if student_or_teacher == "Student":
            classname = self.newclass_box.get()

        elif student_or_teacher == "Teacher":
            title = self.title_enter.get()


        # producing the results for whether the user is a student or teacher, and putting all the information from the table into the tuple "result"

        con = True
        
        # adding validation to all fields preventing a user from not entering anything using red fields 

        # first name is not present
        if firstname == "":
            self.fname_enter.configure(fg_color = "#f8d7da")
            self.fname_enter.delete(0, tk.END)
            con = False

        # lastname is not present
        if lastname == "":
            self.lname_enter.configure(fg_color = "#f8d7da")
            self.lname_enter.delete(0, tk.END)
            con = False

        if title == "ReallQuiteUnlucky123":
            pass

        elif title == "":
            self.title_enter.configure(fg_color = "#f8d7da")



        # password is less than 8 characters long
        if len(password) < 8:
            self.pass_enter.configure(fg_color = "#f8d7da", placeholder_text = ">8 characters long")
            self.pass_enter.delete(0, tk.END)
            con = False

        # passwords are not the same
        if password != reentry:
            self.pass_enter.configure(fg_color = "#f8d7da", placeholder_text = "Passwords must be the same!")
            self.pass_enter.delete(0, tk.END)
            self.repass_enter.configure(fg_color = "#f8d7da", placeholder_text = "Passwords must be the same")
            self.repass_enter.delete(0, tk.END)
            con = False


        if con == True: # continue = true
        
            if student_or_teacher == "Student":


                # verifying that the user doesn't exist
                studentexists = "SELECT * FROM Students WHERE FirstName = ? AND LastName = ? AND DoB = ?"
                self.cursor.execute(studentexists, (firstname,lastname, dob))
                conn.commit()


                result = self.cursor.fetchone() # will contain all information about a Student with all the characteristics above IF they exist
                conn.commit()


            elif student_or_teacher == "Teacher":
                title = self.title_enter.get()
                teacherexists = "SELECT * FROM Teachers WHERE FirstName = ? AND LastName = ? AND DoB = ?"
                self.cursor.execute(teacherexists, (firstname, lastname, dob))
                conn.commit()


                result = self.cursor.fetchone()
                conn.commit()






            if result: # if there is something in result, it shows up as True, so a user will already exist if something is in result
                messagebox.showinfo(title="Error", message="User already exists!")
                self.fname_enter.configure(placeholder_text = "User already exists!")
                self.lname_enter.configure(placeholder_text = "User already exists!")
                self.pass_enter.configure(placeholder_text = "User already exists!") 

                self.window.after(300, lambda: (self.login_page())) # <- using .after function instead of .sleep


               
            else:
                # adding the teachers and students to the database 
                if student_or_teacher == "Teacher":
                    username = (firstname[0] + lastname)

                    usernamet_exists = "SELECT Username FROM Teachers WHERE Username = ?"
                    self.cursor.execute(usernamet_exists, (username,))
                    username_check = self.cursor.fetchone()
                    conn.commit()

                    count = 1
                    while username_check: # until no existing username
                        username = f"{firstname[0]}{lastname}{count}"  # Iterating again
                        self.cursor.execute(usernamet_exists, (username,))
                        username_check = self.cursor.fetchone()
                        count += 1  # incremement 



                    self.wrong_info(f"Username: {username} \n \nPassword: {password}") # outputting the username


                    teacher_insert = '''
                    INSERT INTO Teachers (FirstName, LastName, Username, DoB, Title, Password) VALUES (?, ?, ?, ?, ?, ?)
                    '''


                    teacher_values = (firstname, lastname, username, dob, title, password)


                    self.cursor.execute(teacher_insert, teacher_values) 


                    conn.commit()

                    # -- Code which adds a class to a teacher so the code later can run -- # 

                    teacher_id_q = "SELECT TeacherID FROM Teachers WHERE FirstName = ? AND LastName = ? AND DoB = ?"
                    self.cursor.execute(teacher_id_q, (firstname, lastname, dob))


                    result = self.cursor.fetchone()



                    teacher_id = result[0]  

                    # insert the class into the Class table using the TeacherID that was just produced
                    self.cursor.execute("INSERT INTO Class (TeacherID, ClassName) VALUES (?, ?)", (teacher_id, f"{firstname}1"))
                    conn.commit()



                elif student_or_teacher == "Student":




                    username = (dob[2:4] + firstname[0] + lastname) # creating username as is made in school

                    usernamet_exists = "SELECT Username FROM Students WHERE Username = ?"
                    self.cursor.execute(usernamet_exists, (username,))
                    username_check = self.cursor.fetchone()
                    conn.commit()

                    count = 1
                    while username_check: # until no existing username
                        username = f"{dob[2:4]}{firstname[0]}{lastname}{count}"  # Iterating again
                        self.cursor.execute(usernamet_exists, (username,))
                        username_check = self.cursor.fetchone()
                        count += 1  # incremement 



                    if self.newclass_box.get() == "Class Name":
                        messagebox.showinfo(title="Enter all information", message="Choose a class!")


                    else:
                        classID_query = "SELECT ClassID FROM Class WHERE ClassName = ?"
                        self.cursor.execute(classID_query, (self.newclass_box.get(),))
                        classID_var = self.cursor.fetchone()[0]


                

                        # inserting values into the database for the student. 
                        student_insert = '''
                        INSERT INTO Students (FirstName, LastName, DoB, Username, Password, ClassID) VALUES (?, ?, ?, ?, ?, ?)
                        '''


                        student_values = (firstname, lastname, dob, username, password, classID_var)


                        self.cursor.execute(student_insert, student_values)


                        self.wrong_info(f"Username: {username} \n \nPassword: {password}")


                        conn.commit()


               
    def run(self):
        self.window.mainloop() # actually runs everything..






class Student:
    def __init__(self, window, cursor, username):
        self.username = username # passing the student's username for database functions, the cursor to manipulate the databse, and the window to display visualisations.
        self.cursor = cursor
        self.window = window


        student_id_query = "SELECT StudentID FROM Students WHERE Username = ?" # getting the student ID using the given username
        cursor.execute(student_id_query, (self.username,))
        self.student_id = cursor.fetchone()[0] # taking the first variable as tuples are given

        class_id_query = "SELECT ClassID FROM Students WHERE Username = ?" # getting the classID using given username
        cursor.execute(class_id_query, (self.username,))
        self.class_id = cursor.fetchone()[0]


        self.topic_id_array = ["Number", "Algebra", "Ratio", "Geometry", "Probability", "Statistics"]


        self.student_home_screen() # calls the home screen for the student.



    def page_clearer(self, window):
        for widget in window.winfo_children():
            widget.destroy()




    def student_home_screen(self):
        self.page_clearer(self.window)

    
         # using the page_clearer function from the original application
       
        self.window.title(f"Welcome {self.username}") # setting the title



        student_name = '''
        SELECT FirstName, LastName FROM Students WHERE Username = ?
'''
       
        self.cursor.execute(student_name, (self.username,))


        result = self.cursor.fetchone() # placing the student's full name into a variable to add to the label.



        mainframe = ctk.CTkFrame(self.window) # creating the frame where the buttons, labels, and graphs will be placed
        mainframe.pack(pady =0.01 * screen_height)

        title_frame = ctk.CTkFrame(mainframe)
        title_frame.pack(pady = 30, padx = 15)




        welcome = ctk.CTkLabel(title_frame, text=f"Welcome, {result[0]} {result[1]}", font = ("Times", 40, 'bold'), text_color="blue") # setting a label which welcomes the user.
        welcome.pack(pady = 30, padx = 15) # 250 padding on top, 175 below

                            



        graph_frame = ctk.CTkFrame(mainframe) # frame which will contain the 3 graphs for the student
        graph_frame.pack()




        # TopicIDs:
        # 0 is Number
        # 1 is Algebra
        # 2 is Ratio
        # 3 is Geometry
        # 4 is Probability
        # 5 is Statistics






        Percent_Graph = ctk.CTkCanvas(graph_frame, bg="black") # percentage of questions correct
        Perc_x_values = self.topic_id_array
        Perc_y_values = self.data_maker("Percent") # calling the function which will return the x and y values which will be needed
        self.graph_maker(Percent_Graph, Perc_x_values, Perc_y_values, "Percentage of Correct Answers Per Topic") # function which will create the graphs with the givend data
        Percent_Graph.pack(side="left", padx=3)


        Correct_Graph = ctk.CTkCanvas(graph_frame, bg="black") # correct questions answered
        Correct_y_values = self.data_maker("Correct")
        Correct_x_values = self.topic_id_array


        self.graph_maker(Correct_Graph, Correct_x_values, Correct_y_values, "Number of Correct Answers Per Topic")


        Correct_Graph.pack(side="left", padx=3)






        Total_Graph = ctk.CTkCanvas(graph_frame, bg="black") # total questions done


        self.data_maker("Total")


        Total_x_values = self.topic_id_array
        Total_y_values = self.data_maker("Total")




        self.graph_maker(Total_Graph, Total_x_values, Total_y_values, "Total Questions Answered Per Topic")


        Total_Graph.pack(side="left", padx=3)






        button_frame = ctk.CTkFrame(mainframe) # setting a frame for the buttons
        button_frame.pack(pady = 10)


        topic_selection_button = ctk.CTkButton(button_frame, text = "Topic Selection", command = self.topic_selection) # button which calls the topic selection function
        topic_selection_button.pack(side = "left" , pady = 15, padx = 5)


        automatic_questions_button = ctk.CTkButton(button_frame, text = "Automatic Questions", command = self.auto_questions) # button which calls the automatic questions function
        automatic_questions_button.pack(side = "left" ,pady = 15, padx = 5)


        leaderboard_button = ctk.CTkButton(button_frame, text = "Leaderboard", command = self.leaderboard) # button which calls the leaderboard function
        leaderboard_button.pack(side = "left" , pady = 15, padx = 5)        

        full_paper_button = ctk.CTkButton(button_frame, text = "Full Paper", command = self.full_paper) # button which calls a full paper
        full_paper_button.pack(side = "left" , pady = 15, padx = 5)

        def BackCommands():
            self.window.destroy()
            StartCode()

        back_button = ctk.CTkButton(mainframe, text="Back",fg_color="#4169E1", command = BackCommands)
        back_button.pack(side="left", padx = 5, pady=5)

        edit_button = ctk.CTkButton(mainframe, text = "Change Details", command = lambda: self.Change_Details())
        edit_button.pack(pady = 5, padx = 10, side = "right")



    # function creating all the data for the student graphs
    def data_maker(self, graph_type):


        information_array = np.full((6, 2), None) # making an array with required dimensions, and filling it with nothing


        # TopicIDs:
        # 0 is Number
        # 1 is Algebra
        # 2 is Ratio
        # 3 is Geometry
        # 4 is Probability
        # 5 is Statistics


        correct_count = 0


        for i in range(0,6):
            for j in range (0,2):


                # 0 0 - Number done
                # 0 1 - Number correct
                # 1 0 - Algebra done
                # 1 1 - Algebra correct
                # 2 0 - Ratio done
                # 2 1 - Ratio correct
                # 3 0 - Geometry done
                # 3 1 - Geometry correct
                # 4 0 - Probability done
                # 4 1 - Probability correct
                # 5 0 - Statistics done
                # 5 1 - Statistics correct




                current_query = None # storing the current query based on the topic
                holding_variable = None # what is in the fetch


                if j == 1:
                    current_query = """SELECT Correct FROM Result WHERE TopicID = ? AND Correct = ? AND StudentID = ?"""
                    cursor.execute(current_query, (i, j, self.student_id,))
                    correct_count += 1


                else:
                    current_query = """SELECT Correct FROM Result WHERE TopicID = ? AND StudentID = ?"""
                    cursor.execute(current_query, (i, self.student_id,))


                holding_variable = cursor.fetchall()




                count = 0
                for item in holding_variable:
                    count +=1






                information_array[i, j] = count # adding the number values to the list in the indexes provided above



        percent_list = []
        correct_list = []
        total_list = []



        for element in information_array: # adding all the necessary graph information from the arrays into their respective lists
            # element[0] = total
            # element[1] = correct

            if element[0] == 0: # preventing undefined percentage
                percent_list.append(0)
                total_list.append(0)
                correct_list.append(0)

            else:
                percent_list.append((element[1] / element[0]) * 100) # correct for this topic/total for this topic * 100
                correct_list.append(element[1]) # correct for this topic
                total_list.append(element[0]) # total for this topic



        if graph_type == "Percent": # returning the respective y values for all the graphs
            return percent_list


        elif graph_type == "Correct":
            return correct_list


        elif graph_type == "Total":
            return total_list






    def graph_maker(self, graph, x_values, y_values, Title): # add x and y values from database as parameters


        facecolor_var = "white" # setting to a variable to allow customization


        Fig = Figure(figsize = (4,3.5), dpi = 100, facecolor = facecolor_var) # making the object Figure where the graph will be placed
        axis = Fig.add_subplot(111) # making the axis. Setting 1 row, 1 column, and adding 1 subplot




        bar_color = "blue" # setting to a variable so it can be adjusted later


        axis.bar(x_values, y_values, color = bar_color) # using a bar chart and plotting the x and ys.
        axis.set_facecolor(facecolor_var)
        axis.tick_params(axis='x', rotation=15, labelsize = 9) # adjusting these values to get the words to fit on the axis
        axis.set_title(Title) # setting a title for the graph




        canvas = FigureCanvasTkAgg(Fig, master=graph) # making the canvas where the graph will go
        canvas.draw() # drawing the graph
        canvas.get_tk_widget().pack(side="left", padx=3) # packing the graph itself




    def topic_selection(self):
        self.page_clearer(self.window) # using the page_clearer function from the original application
        self.no_of_questions = 1


        # topic selection creations #


    # Main frame for everything to go in
        large_frame = ctk.CTkFrame(self.window)
        large_frame.pack(pady=0.02 * screen_height, padx=0.02 * screen_width, fill="both", expand=True)

        # Title label for the UI
        title_label = ctk.CTkLabel(large_frame, text="Topic Selection", font=("Calibri", 32, "bold"))  # Setting a title
        title_label.pack(pady=0.02 * screen_height)

        # Frame for the slider and its label
        slide_frame = ctk.CTkFrame(large_frame)
        slide_frame.pack(pady=0.02 * screen_height, fill="x", expand=False)

        def slider_output(value):  # Function which changes when slider changes value
            self.no_of_questions = int(value)  # Setting variable to the current slider value
            value_label.configure(text=f"{self.no_of_questions} questions")  # Outputting the current question number to the user as a label

        # Thicker slider to choose the number of questions, with default set to 10
        question_slider = ctk.CTkSlider(slide_frame, from_=1, to=50, command=slider_output, orientation="horizontal", number_of_steps=49, width= 0.05 * screen_height)
        question_slider.set(self.no_of_questions)  # Set initial number of questions to 10
        question_slider.pack(padx=0.005 * screen_width, pady=0.005 * screen_height, side="left", fill="x", expand=True)

        # Label displaying the current number of questions
        value_label = ctk.CTkLabel(slide_frame, text=f"{self.no_of_questions} questions")
        value_label.pack(padx=0.005 * screen_width, pady=0.005 * screen_height, side="left")

        # Frame to hold all topic buttons
        button_frame = ctk.CTkFrame(large_frame)
        button_frame.pack(pady=0.03 * screen_height, fill="both", expand=True)

        # Centering the buttons within their frame by adjusting row/column configuration
        button_frame.grid_rowconfigure(0, weight=1)  # Makes the row flexible
        button_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)  # Ensures all columns can change size

        topic_array = np.array([None] * 6)  # Creating an array for the topic buttons

        def questions_call(topic_name):  # Called when one of the buttons is pressed
            Questions(self.window, self.cursor, self.student_id, topic_name, self.username, self.no_of_questions)  # Calling the questions class with all required parameters

        # Creating larger buttons and centering them within the frame
        for i in range(6):  # Loop to create buttons for all topics using their database names and pass them as parameters
            topic_array[i] = ctk.CTkButton(button_frame, text=self.topic_id_array[i], width=180, height=180)  # Larger buttons
            topic_array[i].grid(row=0, column=i, padx=10, pady=10, sticky="nsew")  # using grid to centralise
            topic_array[i].configure(command=lambda i=i: questions_call(self.topic_id_array[i]))

        # back frame
        buttonframe = ctk.CTkFrame(large_frame)
        buttonframe.pack(pady=0.02 * screen_height, padx=0.02 * screen_width, fill="x", side="bottom")

        # Back button to return to the student home screen
        back_button = ctk.CTkButton(buttonframe, text="Back", command=self.student_home_screen, fg_color="#4169E1")
        back_button.pack(pady=0.02 * screen_height, padx=0.02 * screen_width)



    def auto_questions(self):
        self.page_clearer(self.window)

        def LinearRegressionModel():
            import pandas as pd # used for data analysis
            from sklearn.linear_model import LinearRegression # creates linear regression models/ data science models
            from sklearn.model_selection import train_test_split # for training and test sets
            from sklearn.metrics import mean_squared_error # for evaluating the performance


            student_id = self.student_id # which student looking at


            # Connect to database
            conn = sqlite3.connect('AdjustMaths.db') # connecting to database


            # query to get average grades and accuracy for all students
            data_query = '''SELECT StudentID, AVG(Grade) AS AvgGrade, AVG(Correct) AS Accuracy FROM Result GROUP BY StudentID
            '''




            df = pd.read_sql_query(data_query, conn) # loading ALL the data into the dataframe





            if df.empty: # if no data is selected, outputting that
                print("No data available.")




            else: # if there is data
                X = df[['AvgGrade', 'Accuracy']] # used for prediction, the percentage correct
                Y = df['AvgGrade']  # trying to predict grade


                # Split data into training and test sets
                X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42) # 80% training and 20% testing. 42, "The answer to the ultimate question of life, the universe and everything"




                model = LinearRegression() # starting the model
                model.fit(X_train, y_train) # training the model using the data




                y_pred = model.predict(X_test) # using the model to predict
                mse = mean_squared_error(y_test, y_pred) # finding the Mean Squared Error between the actual values (y_test) and the predicted values (y_predict)



                student_query = '''SELECT AVG(Grade) AS AvgGrade, AVG(Correct) AS Accuracy FROM Result WHERE StudentID = ?''' # for specific student now
            
                student_df = pd.read_sql_query(student_query, conn, params=(student_id,)) # loading the student data into another dataframe
            
                if student_df.empty: # checking if data has been retrieved
                    print("No data available for the specified student.")
                else:
                    student_data = student_df.iloc[0]
                    # DataFrame with same structure as training data, will be used to make predictions
                    X_new = pd.DataFrame({
                        'AvgGrade': [student_data['AvgGrade']], # AVgGrade column in X_new to average grade of student
                        'Accuracy': [student_data['Accuracy']] # Accuracy column in X_new to accuracy of student
                    })


                    # Predict the grade level
                    predicted_grade_decimal = (model.predict(X_new)) # predicitng the grade the student is at
                    predicted_grade = round(predicted_grade_decimal[0])
                    # print(f"Predicted Grade for student with student ID {student_id}: {predicted_grade}") # oujtputting predicted grade

            return predicted_grade
            

        mainframe = ctk.CTkFrame(self.window) # mainframe
        mainframe.pack(padx=0.05 * screen_width, pady=0.05 * screen_height)


        title_text = ctk.CTkLabel(mainframe, text="Welcome to Automatic Questions!", font=("Times New Roman", 32, "bold")) # setting title
        title_text.pack(padx=0.03 * screen_width, pady=0.03 * screen_height)


        warningLabel = ctk.CTkLabel(mainframe, text="Warning! These questions may take longer to generate than normal questions!", font=("Arial", 20, "bold"), text_color="red") # warning about potential slower times
        warningLabel.pack(padx=0.02 * screen_width, pady=0.02 * screen_height)

        informationBox = ctk.CTkLabel(mainframe, text=(f"Generating..."), font=("Arial", 18), justify="left")
        informationBox.pack(padx=0.02 * screen_width, pady=0.02 * screen_height)


        button_frame = ctk.CTkFrame(mainframe) # creating seperate frame for button
        button_frame.pack(padx=0.03 * screen_width, pady=0.03 * screen_height)

        back_button = ctk.CTkButton(button_frame, text="Back", command=self.student_home_screen, font=("Arial", 18)) # back button
        back_button.pack(padx=0.02 * screen_width, pady=0.01 * screen_height, side="left")

        # continue button to start the questions
        continue_button = ctk.CTkButton(button_frame, text="Continue", font=("Arial", 18, "bold"), command=lambda: Questions(self.window, self.cursor, self.student_id, "Random", self.username, 20, grade_level=LinearRegressionModel()))
        continue_button.pack(padx=0.02 * screen_width, pady=0.01 * screen_height, side="left")

        # statement which finds how many questions the user has completed
        self.cursor.execute("SELECT COUNT(*) FROM Result WHERE StudentID = ?", (self.student_id,))
        row_count = self.cursor.fetchone()[0] # variable storing the no. of questions


        if row_count < 50: # if they havent done sufficient questions the model will not start. Will prevent the linear regression from starting without a reason.
            informationBox.configure(text = f"Pressing continue will start generating questions tailored to you as a user.\nThese questions are based on the grade level the system believes you are at. \nGetting these - and other questions correct will increase your grade over time.\nYou must complete 50 questions first.\n{50-row_count} left.", font=("Arial", 18), justify="left")
        
        # otherwise give them the questions
        else:
            informationBox.configure(text = f"Pressing continue will start generating questions tailored to you as a user.\nThese questions are based on the grade level the system believes you are at: {LinearRegressionModel()}\nGetting these - and other questions correct will increase your grade over time.\nGood luck!", font=("Arial", 18), justify="left")



    def Change_Details(self): # function which allows the user to change their details
        self.page_clearer(self.window)


        # frame to store widgets
        mainframe = ctk.CTkFrame(self.window) 
        mainframe.pack(pady = 0.1 * screen_height)

        # Comboxbox which shows all available classes
        class_names = [] # list which will contain all class names
        cursor.execute("SELECT ClassName FROM Class") 
        c = cursor.fetchall() # getting all the classnames

        for row in c:
            class_names.append(row[0]) # appending to end of lsit

        title_text = ctk.CTkLabel(mainframe, text="Welcome to Change Details!", font=("Calibri", 32, "bold")) # setting title
        title_text.grid(row = 0, column = 0, columnspan = 3, padx = 0.02 * screen_width, pady = 0.02 * screen_height)

        # to choose which class they want to be in
        self.newclass_box = ctk.CTkComboBox(mainframe, values = class_names, state = "readonly") 
        self.newclass_box.grid(row=1, column=1, padx = 10 ,pady = 10, sticky = "ew", ) # sticky goes ew, meaning east west expansion for when the window is expanded.
        self.newclass_box.set("Select Class")

        # Password and Re-entry Password
        self.passw_enter = ctk.CTkEntry(mainframe ,  width=200,  placeholder_text = "Current password", show = "*")
        self.passw_enter.grid(row=1, column=2, padx = 10 ,pady = 10, sticky = "ew") # sticky goes ew, meaning east west expansion for when the window is expanded.#
    
        # entering the new password
        self.newpass_enter = ctk.CTkEntry(mainframe ,  width=200, placeholder_text = "New Password" , show = "*")
        self.newpass_enter.grid(row=3, column=1, padx = 10 ,pady = 10, sticky = "ew") # sticky goes ew, meaning east west expansion for when the window is expanded.

        # re entering the new password
        self.renewpass_enter = ctk.CTkEntry(mainframe ,  width=200, placeholder_text = "Re-enter" , show = "*")
        self.renewpass_enter.grid(row=3, column=2, padx = 10 ,pady = 10, sticky = "ew") # sticky goes ew, meaning east west expansion for when the window is expanded.

        self.ShowPasswords = ctk.CTkCheckBox(
            mainframe, 
            text="Show Passwords", 
            command=lambda: [
                self.newpass_enter.configure(show="" if self.newpass_enter.cget("show") == "*" else "*"),
                self.renewpass_enter.configure(show="" if self.renewpass_enter.cget("show") == "*" else "*")
            ]
        )
        self.ShowPasswords.grid(row=4, columnspan=4, pady=10)

        # buttong to update details
        update_button = ctk.CTkButton(mainframe, text="Update Details", command=self.update_details)
        update_button.grid(row=5, column=2, pady=10)

        # button to go back to the home page
        back_button = ctk.CTkButton(mainframe, text = "Back", command = self.student_home_screen, fg_color="#4169E1")
        back_button.grid(row = 5, column = 1, pady=10)


    def update_details(self): # function which makes the database changes and verifies everything
        old_password = self.passw_enter.get() # getting the password input
        new_password = self.newpass_enter.get() # getting the new password input
        reenter_password = self.renewpass_enter.get() # getting the re entry input

        classname = self.newclass_box.get() # getting the new classname input

        if self.newclass_box.get() == "Select Class":
            messagebox.showinfo(title="Enter all information", message="Choose a class!")


        else:
            # select statement getting the class id of the classname input so database changes can be made
            self.cursor.execute(("SELECT ClassID FROM Class WHERE ClassName = ?"), (classname,))
            class_id = self.cursor.fetchone()[0]

            # current password from database
            self.cursor.execute("SELECT Password FROM Students WHERE StudentID = ?", (self.student_id,))
            result = self.cursor.fetchone()
            current_password = result[0] # changing from tuple to the password itself



            con = True
            # Check if the old password is correct
            if old_password != current_password:
                self.passw_enter.configure(fg_color="#f8d7da")
                self.passw_enter.configure(placeholder_text = "The old password is incorrect.")
                messagebox.showinfo("Error", "The password is incorrect")
                con = False


            # Check if the new passwords match
            if new_password != reenter_password:
                self.newpass_enter.configure(fg_color="#f8d7da")
                self.renewpass_enter.configure(fg_color="#f8d7da")
                self.newpass_enter.configure(placeholder_text = "Passwords do not match")
                self.renewpass_enter.configure(placeholder_text = "Passwords do not match")
                messagebox.showinfo("Error", "Passwords do not match")
                con = False

            # ensuring the length is appropriate
            if len(new_password) < 8:
                self.newpass_enter.configure(fg_color="#f8d7da")
                self.renewpass_enter.configure(fg_color="#f8d7da")
                self.newpass_enter.configure(placeholder_text = "Password must be > 8 characters long")
                self.renewpass_enter.configure(placeholder_text = "Password must be > 8 characters long")
                messagebox.showinfo("Error", "Password must be > 8 characters long")
                con = False

            # if continue is true after all the validation then update the password and class
            if con == True:
                self.cursor.execute("UPDATE Students SET Password = ? WHERE StudentID = ?", (new_password, self.student_id))
                conn.commit()
                self.cursor.execute(("UPDATE Students SET ClassID = ? WHERE StudentID = ?"), (class_id, self.student_id))
                conn.commit()
                messagebox.showinfo("Change Complete", f"Password: {new_password}. \nClass: {classname}")
            








    def leaderboard(self):
        self.page_clearer(self.window)  # Empties the window

        ViewStudentsStatement = "SELECT StudentID, FirstName, Username FROM Students WHERE ClassID = ?" # retrieves the necessary information from table
        self.cursor.execute(ViewStudentsStatement, (self.class_id,)) 
        students_info = self.cursor.fetchall()

        treeview_data = []  # holding all data for the leaderboard

        for student in students_info: # iterating over all the students within the set class
            student_id = student[0] # since it is a tuple: [StudentID, FirstName, Username]
            first_name = student[1]
            username = student[2]

            # Getting the number of correct answers for the specified student
            self.cursor.execute("SELECT COUNT(*) FROM Result WHERE StudentID = ? AND Correct = 1", (student_id,)) # condition for when they are correct, counting ther number of rows
            correct_count = self.cursor.fetchone()[0] # first value as tuple

            # Getting the total number of answers from specified student
            self.cursor.execute("SELECT COUNT(*) FROM Result WHERE StudentID = ?", (student_id,)) # no condition to find the number of questions done
            total_count = self.cursor.fetchone()[0] # fetching the first value as tuple

            if total_count > 0:  # Preventing division by zero
                percentage_correct = ((correct_count / total_count) * 100)  # Percentage correct calculation
            else:
                percentage_correct = 0

            treeview_data.append((first_name, username, correct_count, total_count, f"{percentage_correct:.2f}%")) # adding all the data that was just calculated/selected


        # configuring treeview
        student_tree = ttk.Treeview(self.window, columns=("FirstName", "Username", "Correct", "Total", "Percentage Correct"), style="Custom.Treeview", show="headings")

        student_tree.heading("FirstName", text="FirstName") # all the headings 
        student_tree.heading("Username", text="Username")
        student_tree.heading("Correct", text="Correct")
        student_tree.heading("Total", text="Total")
        student_tree.heading("Percentage Correct", text="Percentage Correct")

        student_tree.column("FirstName", width=150) # setting the width of the columns
        student_tree.column("Username", width=150)
        student_tree.column("Correct", width=100)
        student_tree.column("Total", width=100)
        student_tree.column("Percentage Correct", width=150)

        # Inserting data
        for row in treeview_data:
            student_tree.insert("", tk.END, values=row) # adding into the tree

        student_tree.pack(fill=tk.BOTH, expand=True) # filling up the screen

        # go back to home_screen
        back_button = ctk.CTkButton(self.window, text="Back", command=self.student_home_screen, fg_color="#4169E1")
        back_button.pack(padx=10, pady=15)



    def full_paper(self):  # function which will give a set number of random questions
        self.page_clearer(self.window)
        
        # Create the main frame that will contain all UI
        large_frame = ctk.CTkFrame(self.window)
        large_frame.pack(padx=0.05 * screen_width, pady=0.05 * screen_height, fill="both", expand=True)

        # Create a sub-frame to hold the content, centered 
        content_frame = ctk.CTkFrame(large_frame)
        content_frame.pack(padx=0.03 * screen_width, pady=0.03 * screen_height, fill="both", expand=True)

        # Label describing the purpose
        q_label = ctk.CTkLabel(content_frame, text="You will now be given 35 questions to complete of varying difficulty.", font=("Arial", 18), wraplength=0.9 * screen_width)
        q_label.pack(pady=(0.03 * screen_height, 0.05 * screen_height))  # Space above and below label

        # Function to start the questions
        def Cont():
            Questions(self.window, self.cursor, self.student_id, "Random", self.username, 35)  # Begin questions

        # Continue button
        continue_button = ctk.CTkButton(content_frame, text="Continue", command=Cont, width=200, height=40, font=("Arial", 16), corner_radius=10)
        continue_button.pack(pady=(0, 0.02 * screen_height))  # Space below the button

        # Back button, styled similarly to continue button
        back_button = ctk.CTkButton(content_frame, text="Back", command=self.student_home_screen, width=200, height=40, font=("Arial", 16), corner_radius=10, fg_color="#4169E1")
        back_button.pack(pady=(0.02 * screen_height, 0))  # Space below the back button to avoid clutter



class Questions():
    def __init__(self, window, cursor, student_id, chosen_topic, username, no_of_questions, **kwargs): 
        self.student_id = student_id # passing the student's username for database functions, the cursor to manipulate the databse, and the window to display visualisations.
        self.cursor = cursor
        self.window = window
        self.username = username
        self.NoOfQuestions = no_of_questions # the number of questions that thhe user will complete

        self.chosen_topic = chosen_topic
        self.QuestionNumber = 0 # defining the question number to be incremented for every time the Question maker function is called
        self.NoOfCorrect = 0 # defining the number of correct questions initially done

        if "grade_level" in kwargs: # if passed as a parameter from being chosen as automatic questions
            self.grade_level = kwargs['grade_level'] # setting the grade level to the value requried

        else:
            self.grade_level = -1 # otherwise setting to an impossible value to be used in questionChooser

        


        self.QuestionChooser()


    def page_clearer(self, window):
        for widget in self.window.winfo_children():
            widget.destroy()


    def QuestionChooser(self):

        if self.chosen_topic == "Number":
            self.Number()

        elif self.chosen_topic == "Algebra":
            self.Algebra()

        elif self.chosen_topic == "Ratio":
            self.Ratio()

        elif self.chosen_topic == "Geometry":
            self.Geometry()

        elif self.chosen_topic == "Probability":
            self.Probability()

        elif self.chosen_topic == "Statistics":
            self.Statistics() 

        elif self.chosen_topic == "Random":
            r.choice([self.Number, self.Algebra, self.Ratio, self.Geometry, self.Probability, self.Statistics])()

        self.Date()

 

    def FinishScreen(self): # screen which is displayed after all questions are completed
        

        finish_frame = ctk.CTkFrame(self.window, fg_color="#D3D3D3") # frame for all messages
        finish_frame.pack(pady=30, padx=30)

        congrats_label = ctk.CTkLabel(finish_frame, text="Well Done!", font=("Calibri", 40, "bold"), text_color="#0066CC")  # well done message in bold blue
        congrats_label.pack(pady=20, padx = 0.05 * screen_width)


        questions_label = ctk.CTkLabel(finish_frame, text=f"You completed {self.NoOfQuestions} questions,\nand got {self.NoOfCorrect} correct.", font=("Calibri", 28), text_color="#333333")  # stats in grey
        questions_label.pack(pady=10)


        percentage_label = ctk.CTkLabel(finish_frame, text=f"Your score: {(self.NoOfCorrect/self.NoOfQuestions)*100:.2f}%", font=("Calibri", 30, "bold"), text_color="#FF4500")  # percentage in reddish
        percentage_label.pack(pady=10)

        encourage_label = ctk.CTkLabel(finish_frame, text="Keep up the great work!", font=("Calibri", 26, "italic"), text_color="#228B22")  # continue working in green
        encourage_label.pack(pady=20)

        back_button = ctk.CTkButton(finish_frame, text = "Back", fg_color="#4169E1", command= lambda: [Student(self.window, self.cursor, self.username), Student.student_home_screen]) # summons the class, and the page within it
        back_button.pack(pady = 20)

    def QuestionCreator(self, QuestionText, Answer, Notes, grade, topic_id, **kwargs):

        
        

        if 'font_size' in kwargs:
            font_size = kwargs['font_size'] # setting font_sizes

        else:
            font_size = 14

        if self.grade_level != -1: # if the grade_level is not just the default then use the grade model to give tailored questions

            if abs(self.grade_level - grade) > 1: # not enough functions to always get the exact grade i want, so a difference in 1 of grade is acceptable. e.g if grade_level = 5, grade 3 and 6 are also acceptable
                self.QuestionChooser()
            
            else:
                pass

        else:
            pass
        



        canvas_frame = ctk.CTkFrame(self.window, fg_color="#FFFFFF")
        canvas_frame.grid(row = 0, column = 1, padx=10, pady=10)

        drawing_canvas = ctk.CTkCanvas(canvas_frame, width= (0.48 * screen_width), height= (0.9 *screen_height), bg="white") # setting the size of the canvas with respect to the size of the self.window
        drawing_canvas.pack(padx=10, pady=10)

        # Adding drawing functionality to the canvas
        def draw(event):
            # event.x and event.y retrieve the coordinates of the mouse. +/- 1 make an oval AROUND the mouse 
            #
            x1 = event.x - 1
            y1 = event.y - 1
            x2 = event.x + 1
            y2 = event.y + 1
            drawing_canvas.create_oval(x1, y1, x2, y2, fill="black", width=2) # creating the oval around the mouse with parameters given


        drawing_canvas.bind("<B1-Motion>", draw)  # <B1-Motion> is the event of the mouse holding left click. The bind function causes the draw function to be called


        def right_angled_triangle(): # function which creates a right angled triangle when called
            x1, y1 = 50, 50 # points for this
            x2, y2 = 150, 50
            x3, y3 = 50, 150

            coordinates = [x1, y1, x2, y2, x3, y3] 
            drawing_canvas.create_polygon(coordinates, fill="white", outline="black") # plotting the values

        def square():
            x1, y1 = 200, 50 # variable coordinates
            x2, y2 = 300, 150
            coordinates = [x1, y1, x2, y2]
            drawing_canvas.create_rectangle(coordinates, fill="white", outline="black") # create the rectangle of equal length

        def circle():
            x1, y1 = 350, 50 # variable coordinates
            x2, y2 = 450, 150 
            coordinates = [x1, y1, x2, y2]
            drawing_canvas.create_oval(coordinates, fill="white", outline="black") # slightly different using the create_oval function similar to writing on the whiteboard

        def rectangle(): # function which creates a rectangle 
            x1, y1 = 50, 200
            x2, y2 = 200, 300
            drawing_canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")

            

        if "shape" in kwargs: # checking whether it exists as a parameter as it will not be used for all functions
            if kwargs["shape"] == "right_triangle" or kwargs["shape"] == "triangle": # if statements checking for all tghe shapes, and calling them if the question asks for them
                right_angled_triangle()


            elif kwargs["shape"] == "square":
                square()

            elif kwargs["shape"] == "rectangle":
                rectangle()

            elif kwargs["shape"] == "circle":
                circle()



        def AnswerChecker(): # this function checks the answer and returns data to the database
            submitbutton.configure(state = "disabled") # submit button cannot be clicked more than once giving multiple correct answers for 1 question
            nextbutton.configure(state = "normal")
            user_answer = answerbox.get()

            if (answerbox.get()) == str(Answer):
                answerbox.configure(fg_color="#e6ffe6") # if the answer is correct, the textbox & background becomes green
                self.window.configure(fg_color = "#e6ffe6") 
                correct = 1
                self.NoOfCorrect += 1
                report = "Well Done!"



            else:
                answerbox.configure(fg_color="#FFCCCB", text_color="#000") # if the answer is incorrect, the textbox & background become red
                self.window.configure(fg_color = "#FFCCCB")
                correct = 0
                report = "Unlucky."

            answerbox.delete(0, tk.END)
            answerbox.configure(placeholder_text = f"{report} The answer is {Answer}.")
            answerbox.configure(state="disabled") # an answer is submitted so the entrybox is locked



            self.database_adder(user_answer, Answer, QuestionText, topic_id, grade, correct) # this adds all the data from the question into the database

#    self, user_input, actual_answer, questiontext, topic_id, correct

        def NextQuestion():

            self.window.configure(fg_color = "#FFFFFF") #making the screen white again
            self.page_clearer(self.window) # clearing the window
            if self.QuestionNumber < self.NoOfQuestions: # if they havent met the number of questions they set
                self.QuestionChooser() # continue with questions
            
            else: 
                self.FinishScreen() # otherwise take them to the end screen where they can see their stats.


        self.QuestionNumber +=1

        if self.NoOfQuestions != 0:
            Progress = (self.QuestionNumber/self.NoOfQuestions) # if they select 0
        else:
            Progress = 0

        # configuring the weights of the rows
        self.window.grid_rowconfigure(0, weight = 1)
        self.window.grid_columnconfigure(0, weight = 1)

        self.window.grid_rowconfigure(1, weight = 1)

        mainframe = ctk.CTkFrame(self.window, fg_color="#FFFFFF", height = 0.9 * screen_height) # frame
        mainframe.grid(row = 0, column = 0, padx=10, pady=10, sticky = "nesw")

        # creating progress bar to show how far through the questions the user is
        progress_bar = ctk.CTkProgressBar(mainframe, orientation = "horizontal", determinate_speed = 0, height = (0.02 * screen_height), width = (0.45 * screen_width))
        progress_bar.pack(padx = 0.01 * screen_width, pady = 0.01 * screen_width)

        progress_bar.set(Progress) # setting the progress bar to the value assigned

        # creating frame for widgets to go into
        question_frame = ctk.CTkFrame(mainframe, height = 0.48 * screen_height, fg_color="#CEDAEC")
        question_frame.pack(padx = 0.01 * screen_width, pady = 0.01 * screen_width)

        # creating label which will display the question
        question_label = ctk.CTkLabel(question_frame, text = QuestionText, width = (0.48 * screen_width), font = ("Calibri", font_size), wraplength=(0.35 * screen_width)) # places the question in
        question_label.pack(padx = 0.01 * screen_width, pady = 0.01 * screen_width)

        # creating notes which will show any extra information required
        notes_label = ctk.CTkLabel(question_frame, text = Notes, font = ("Calibri", font_size - 4))
        notes_label.pack(padx = 0.01 * screen_width, pady = 0.01 * screen_width)

        # creating entry field for user to input their answer
        answerbox = ctk.CTkEntry(question_frame, placeholder_text = "Answer Here", height = 0.03 * screen_height, width = 0.44 * screen_width, fg_color="#FFFFFF", font=("Calibri", 20), corner_radius=0) # blue: #A0C6FC
        answerbox.pack(padx = 0.01 * screen_width, pady = 0.01 * screen_width)

        # button to call the answer checker so the user can see their answer
        submitbutton = ctk.CTkButton(question_frame, text="Submit", command=AnswerChecker, height = 0.1 * screen_height, width = 0.1 * screen_width, font = ("Calibri", 17))
        submitbutton.pack(padx = 0.01 * screen_width, pady = ((0.01 * screen_height),(0.1 * screen_height)), side = "left")


        # nextbutton to start the next question
        nextbutton = ctk.CTkButton(question_frame, text="Next Question", height = 0.1 * screen_height, width = 0.1 * screen_width, font = ("Calibri", 17) ,  command=NextQuestion)
        nextbutton.pack(padx = 0.01 * screen_width, pady = ((0.01 * screen_height),(0.1 * screen_height)), side = "right")
        nextbutton.configure(state = "disabled") 


        # back button to return back to the student home screen.
        backbutton = ctk.CTkButton(question_frame, text = "Back",fg_color="#4169E1", height = 0.05 * screen_height, width = 0.05 * screen_width, font = ("Calibri", 12), command= lambda: [self.window.configure(fg_color = "#FFFFFF"), Student(self.window, self.cursor, self.username), Student.topic_selection])
        backbutton.pack(padx = 0.01 * screen_width, pady = ((0.01 * screen_height),(0.1 * screen_height)), side = "left")
    



    def Quicksort(self, S):
        if len(S) <= 1:  # Base case, return if the list is empty or has one element
            return S


        pivot_index = len(S) // 2  # Choose the middle element as the pivot
        pivot_value = S[pivot_index] # storing the original pivot value


        left_array = [] # making the sub-arrays
        right_array = []


        for x in range(len(S)): # for every element in the list
            if x != pivot_index:  # don't compare the pivot to the pivot
       
                if S[x] < pivot_value:
                    left_array.append(S[x]) # placing elements in each sub-array
                else:
                    right_array.append(S[x])


        left_array = self.Quicksort(left_array) # sorting the subarrays the same way
        right_array = self.Quicksort(right_array)

        return left_array + [pivot_value] + right_array # returning the completed list




    def Date(self):
        self.todays_date = datetime.now().date()

    def random_integer(self, start, end): # function which creates random integers
        val = r.randint(start, end)

        return val
    


    


    def database_adder(self, user_input, actual_answer, questiontext, topic_id, grade, correct): # takes the parameters: users answer, the answer, the topicid of the question, and whether they are correct. 


            question_query = "INSERT INTO Question (QuestionText, StudentOption, CorrectOption) VALUES (?, ?, ?)"
            question_values = (questiontext, user_input, actual_answer,)
            self.cursor.execute(question_query, question_values)




            conn.commit() # do not delete this


            last_question_id = self.cursor.lastrowid



            result_query = "INSERT INTO Result (StudentID, QuestionID, TopicID, Correct, Grade, Date) VALUES (?, ?, ?, ?, ?, ?)" 
            self.cursor.execute(result_query, (self.student_id, last_question_id, topic_id, correct, grade, self.todays_date,))
            conn.commit()



        


    def Number(self):
        self.page_clearer(self)


        def OrderingIntegers():
            integers = []

            for i in range(5):
                ran = r.randint(-100, 100)
                integers.append(ran)

            QuestionText = f"Order the integers {integers} from smallest to largest."
            Notes = "Give your answer in the form of a list: [-3, 1, 5]."
            Answer = self.Quicksort(integers)  # sorting
            self.QuestionCreator(QuestionText, Answer, Notes, 1, 0)


        def FractionsOfShape():
            numerator = r.randint(1, 20) # numerator and denominator
            denominator = r.randint(numerator + 1, 50)  
            shape = r.choice(["circle", "square", "triangle"]) # random shape

            gcd = math.gcd(numerator, denominator)  # find the greatest common denominator of both numbers

            simplified_numerator = numerator // gcd # integer divsiion to prevent floats from being produced
            simplified_denominator = denominator // gcd # creating the lowest fracction

            QuestionText = f"A {shape} is divided into {denominator} equal parts. \n{numerator} parts are shaded. \nWhat fraction of the shape is shaded?"
            Notes = "Give your answer as a fraction in its simplest form: a/b"
            Answer = f"{simplified_numerator}/{simplified_denominator}"
            self.QuestionCreator(QuestionText, Answer, Notes, 3, 0)



        def SimplifyFractions():
            numerator = r.randint(2, 100)
            denominator = r.randint(numerator + 1, 120)  # denominator > numerator
            gcd = math.gcd(numerator, denominator)  # greatest common divisor

            QuestionText = f"Simplify the fraction {numerator}/{denominator} to its lowest terms."
            Notes = "Give your answer in the form a/b."
            Answer = f"{numerator // gcd}/{denominator // gcd}"  # simplified fraction
            self.QuestionCreator(QuestionText, Answer, Notes, 3, 0)


        def Multiples():
            num = r.randint(1, 12)  # small number for multiples
            multiples = []

            for i in range(1,6):
                multiples.append(i * num) # calculates first 5 multiples

            QuestionText = f"List the first 5 multiples of {num}."
            Notes = "Give your answer in the form of a list: [3, 6, 9, 12, 15]"
            Answer = multiples  
            self.QuestionCreator(QuestionText, Answer, Notes, 1, 0)


        def Indices():
            a = r.randint(2, 10)
            x = r.randint(2, 7)
            Answer = a ** x
            QuestionText = f"Find {a}^{x}."  # q
            Notes = ""
            
            self.QuestionCreator(QuestionText, Answer, Notes, 4, 0)



        def Rounding():
            number = r.uniform(1, 100)  # random float number
            decimal_places = r.randint(1,4) # random number of decimal places, up to 4
            QuestionText = f"Round the number {number:.5f} to {decimal_places} decimal place(s)."
            Notes = ""
            Answer = f"{round(number, decimal_places):.{decimal_places}f}"  # round to the chosen decimal places
            self.QuestionCreator(QuestionText, Answer, Notes, 4, 0)


        def BIDMAS():
            a = r.randint(1, 50)
            b = r.randint(1, 50)
            c = r.randint(1, 10)
            expression = f"({a} + {b}) * {c}"
            QuestionText = f"Evaluate {expression}"
            Notes = ""
            Answer = (a + b) * c  # evaluate the expression using BIDMAS
            self.QuestionCreator(QuestionText, Answer, Notes, 5, 0)


        def Reciprocals(): # 1/x =
            a = r.randint(1,50) # producing a number whihc will be reciprocalled
            QuestionText = f"Find the reciprocal of {a}"
            Notes = "Give your answer to 2 d.p"


            Answer = f"{(1/a):.2f}"
            self.QuestionCreator(QuestionText, Answer, Notes, 2, 0)


        def HCF(): # highest common factor of 2 numbers
            divisor = r.randint(1,15) # generating a divisor for the value
            a = r.randint(3,15) # generating 2 numbers
            b = r.randint(16,25)


            # multiplying the values by divisor so a highest common factor can be fine
            a = a * divisor
            b = b * divisor



            QuestionText = f"Find the highest common factor of {a} and {b}." # question
            Notes = ""
            Answer = f"{math.gcd(a,b)}" # calculating gcd jsut in case they have a different higher common factor


            self.QuestionCreator(QuestionText, Answer, Notes, 7, 0) # sending back to question creation
 

        def LCM():  # lowest common multiple of 2 numbers
            # generating 2 numbers
            a = r.randint(3, 100)
            b = r.randint(3, 50)
            
           
            lcm = abs(a * b) // math.gcd(a, b) # lcm formula
            
            QuestionText = f"Find the lowest common multiple of {a} and {b}."
            Notes = ""
            Answer = f"{lcm}"
            
            self.QuestionCreator(QuestionText, Answer, Notes, 6, 0)


        def NegativeIndices(): # implied
            a = r.randint(2,4)
            e = r.randint(2,3)

            QuestionText = f"Find {a}^-{e}."
            notes = "Give your answer to 2 d.p if needed."
            Answer = f"{(a**(-e)):.2f}"

            self.QuestionCreator(QuestionText, Answer, notes, 6, 0)


        def SquareRoot(): # solve common square roots up to 225
            k = r.randint(1,16)

            QuestionText = f"Find the square root of {k**2}."
            Notes = "No calculator"
            Answer = k

            self.QuestionCreator(QuestionText, Answer, Notes, 1, 0)


        def StandardForm():  # convert large numbers to standard form

            large_number = r.randint(1_000_000, 1_000_000_000)  # between a million and billion
            
            n = len(str(large_number)) -1 # - 1 as diigt will start in 1s
            a = large_number / (10 ** n) # must be between 1 and 10
            
            QuestionText = f"Convert {large_number} to standard form."
            Notes = "Give your answer to 3 s.f, in the form 'a * 10^n'"
            Answer = f"{a:.2f} * 10^{n}"
            

            self.QuestionCreator(QuestionText, Answer, Notes, 7, 0)

        def FractionDecimalsPercentages(): # converting between 
            numerator = r.randint(1,15)
            denominator = r.randint(16,25)

            QuestionText = f"Convert {numerator}/{denominator} to a percentage."
            Answer = f"{((numerator/denominator) * 100):.2f}"
            Notes = "Give your answer to 2 d.p"

            self.QuestionCreator(QuestionText, Answer, Notes, 2, 0)
            

        def PercentOfValue(): # percentage of value
            perc = r.randint(1,100)
            value = r.randint(1,5000)

            QuestionText = f"Find {perc}% of {value}."
            Notes = "Give your answer to 2 d.p"
            Answer = f"{((perc/100) * value):.2f}"

            self.QuestionCreator(QuestionText, Answer, Notes, 3, 0)


        def Bounds(): 

            # producing lengthh, width, and uncertainty
            length = r.randint(5, 20)  
            width = r.randint(5, 20)  
            uncertainty = r.uniform(0.1, 1.0)  
            uncertainty = float(f"{uncertainty:.2f}")

            # calculating upper and lower bounds
            length_upper = length + uncertainty
            length_lower = length - uncertainty
            width_upper = width + uncertainty
            width_lower = width - uncertainty

            # calculating areas
            area_upper = (length_upper * width_upper)  # Maximum area
            area_lower = (length_lower * width_lower)  # Minimum area

            QuestionText = f"The length of a rectangle is {length} +/- {uncertainty} and the width is {width} +/- {uncertainty}. \nFind the upper and lower bounds of the area."
            Notes = "Give your answers to 2 d.p, in the form (upper,lower)"
            Answer = f"({area_upper:.2f},{area_lower:.2f})"

            # Step 5: Pass the question back to the question creation system
            self.QuestionCreator(QuestionText, Answer, Notes, 8, 0)


        def RecurringtoDecimal():  # implied: convert recurring decimal to fraction
            
            # producing the recurring digits, and the option for 1 or 2 d.p
            recurring_digit = r.randint(1, 9) 
            recurring_digit2 = r.randint(1, 9)
            decimal_places = r.randint(1, 2)  

            # 2 conditions, one for easier and one for harder
            if decimal_places == 1:  # Case for 0.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx...
                QuestionText = f"Convert 0.{recurring_digit}{recurring_digit}... to a fraction in its lowest form."
                numerator = recurring_digit
                denominator = 9
                gcd = math.gcd(numerator, denominator)  # gcd to simplify
                Answer = f"{numerator // gcd}/{denominator // gcd}"
                Grade = 6
                

            else:  # Case for 0.xyxyxyxy...
                QuestionText = f"Convert 0.{recurring_digit}{recurring_digit2}{recurring_digit}{recurring_digit2}... to a fraction in its lowest form."
                numerator = int(f"{recurring_digit}{recurring_digit2}") # converting the 2 digits into a single integer
                denominator = 99
                gcd = math.gcd(numerator, denominator)  # to simplify fraction
                Answer = f"{numerator // gcd}/{denominator // gcd}"  # Simplified fraction
                Grade = 8

            Notes = "Give your answer in its simplest form"
            
            self.QuestionCreator(QuestionText, Answer, Notes, Grade, 0) 

        

        def FractionIndices(): # ONLY fractional indices
            # creating the 3 values that will be used
            a = r.randint(2,7)
            b = r.randint(1,9)
            c = r.randint(2,9)

            # creating the question, notes and calculating the answer
            QuestionText = f"Find {a}^({b}/{c})."
            Notes = "Give your answer to 2 d.p"
            Answer = f"{(a**(b/c)):.2f}"


            self.QuestionCreator(QuestionText, Answer, Notes, 6, 0)

        

        def ConvertingSurds(): # converting a surd from the form a√b to √n √√√ looks like a tick
            a = r.randint(2,10)
            b = 4 # setting base case so while loop runs
            while b == 4 or b == 9: # preventing square numbers 
                b = r.randint(2,24)

            QuestionText = f"Convert {a}√{b} to the form √n."
            Notes = "Enter n as your answer"
            Answer = f"{(a**2) * b}"

            self.QuestionCreator(QuestionText, Answer, Notes, 8, 0)


        def Rationalising(): 

            # rationalise the denominator of a surd
            # a/(n - √b) * (n + √b)/(n + √b) = (an + a√b)/(n^2 -b)


            # Creating the 3 values that will be used
            a = r.randint(1, 10)  # Numerator coefficient
            n = a
            while math.gcd(a, n) != 1 :
                n = r.randint(6,49)  # Whole number in the denominator

            b = 4
            while b % 4 == 0 or b % 9 == 0: # preventing square numbers/divisibility by them
                b = r.randint(2,24)

            # Creating the question, notes and calculating the answer
            QuestionText = f"Rationalise  {a}/({n} - √{b})"
            Notes = "Enter your answer in the form (an + aroot(b))/p"
            
            # Rationalising the denominator
            numerator = f"{a*n} + {a}root({b})"
            denominator = f"{n**2 - b}"
            Answer = f"({numerator})/{denominator}"

            # Call the question creator method
            self.QuestionCreator(QuestionText, Answer, Notes, 9, 0)


        


        def ChoosingQuestion(): # function which chooses a question to be output randomly. This cannot be outside the
            choosable_questions = [OrderingIntegers, FractionsOfShape, SimplifyFractions, Multiples, Indices, Rounding, BIDMAS, Reciprocals, HCF, LCM, NegativeIndices, SquareRoot, StandardForm, FractionDecimalsPercentages, PercentOfValue, Bounds, RecurringtoDecimal, FractionIndices, ConvertingSurds, Rationalising]


            choice = r.choice(choosable_questions)

            choice()
        
        ChoosingQuestion()


    

    def Algebra(self):
        self.page_clearer(self)


        def FunctionMachine():

            ran_coefficient = self.random_integer(-100, 100) # generating the 3 random integers that will be used
            ran_coefficient2 = self.random_integer(0, 100)
            ran_coefficient3 = self.random_integer(-10, 10)


            functionout = (f"{ran_coefficient}x + {ran_coefficient2}") # creating the output function for the user

            result = ((ran_coefficient * ran_coefficient3) + ran_coefficient2) # the actual answer after substitution


            self.QuestionCreator(f"The function f(x) = {functionout}. \n Find the value of f({ran_coefficient3})", result, "Submit, then Next Question!", 2, 1)



        def GenerateSequence():
            a = self.random_integer(1,10) # initial value
            r = self.random_integer(1,15) # common difference 


            QuestionText = f"First 5 values of an arithmetic series are {a},"

            
            k = a
            for i in range (3):
                k += r

                QuestionText += f"{k},"


            QuestionText += "x. \n Find x."

            Answer = a + (4 * r)

            self.QuestionCreator(QuestionText, Answer, "", 2, 1)
            



        def ExpandSingleBrackets():
        # Generate random values for a, b, and c
            a = self.random_integer(-20, 20)
            b = self.random_integer(-9, 9)
            c = self.random_integer(0, 20)
            
            abx = a * b # first expanded term
            ac = a * c # second expanded term
      
            QuestionText = (f"Expand {a}({b}x + {c})") 
            Answer = (f"{abx}x + {ac}") # default answer
            
            if ac < 0:
                Answer = f"{abx}x - {abs(ac)}" # given that a or c is negative, the question is changed
            
            Notes = ("Give your answer in the form ax + b. Don't forget spaces!")
            
            # Call the QuestionCreator method to handle the question
            self.QuestionCreator(QuestionText, Answer, Notes, 4, 1)



        def Substitution():
            a = self.random_integer(1,20)
            b = self.random_integer(1, 9)
            c = self.random_integer(1, 20)
            d = self.random_integer(1,10)

            x_equation = f"{a}x + {b}"
            u_equation = f"{c}u + {d}"

            answer = f"{a * c}u + {(a*d) + b}"
            notes = "Give your answer in the form au + b"

            QuestionText = f"f(x) = {x_equation}. \nFind f({u_equation})"

            self.QuestionCreator(QuestionText, answer, notes, 4, 1)



        def GradientofLine(): 

            m = self.random_integer(1,50)
            c = self.random_integer(1,100)

            QuestionText = f"Find the gradient of the line with equation y = {m}x + {c}"

            notes = ""

            answer = m

            self.QuestionCreator(QuestionText, answer, notes, 2, 1)

        def SolvingEquations():
            a = self.random_integer(1,100)
            b = self.random_integer(1,15)
            c = self.random_integer(1,50)

            QuestionText  = f"{a} = {b}x + {c}"
            notes = "Give your answer to 2 d.p"
            Answer = ((a - c)/b)

            Answer = (f"{Answer:.2f}")

            self.QuestionCreator(QuestionText, Answer, notes, 4, 1)

        def RearrangeFormula():
            a = self.random_integer(1,15)
            b = self.random_integer(1,15)
            c = self.random_integer(1,10)

            QuestionText = f"Rearrange {a}y + {b} = {c}x such that y is the subject."
            Answer = f"({c}x - {b})/{a}"

            notes = "Give your in the form (ax - b)/c"

            self.QuestionCreator(QuestionText, Answer, notes, 4, 1)



        def Simple_nth_Term():
            # an + b
    
            a = self.random_integer(1,5)
            b = self.random_integer(1,10)
            c = b

            # f"Nth term {a}n + {b}. c = {c}")

            QuestionText = f"Find the nth term of {a + b}, "

            for n in range (2,5):
                c = (a*n + b)
                QuestionText += f"{c}, "

            QuestionText += "in the form an + b"
            notes = ""
            Answer = f"{a}n + {b}"

            self.QuestionCreator(QuestionText, Answer, notes, 5, 1)
                

        def Hard_nth_Term():
            a = self.random_integer(1,4)
            b = self.random_integer(1,5)
            c = self.random_integer(1,9)
            
            # nth term = an^2 + bn + c

            QuestionText = f"Find the nth term of {a + b + c}, "

            for n in range (2,6):
                term = (a*(n**2)) + (b * n) + c

                QuestionText += f"{term}, "

            QuestionText += "in the form an\u00B2 + bn + c"
            notes = "Give your answer in the form an^2 + bn + c, where a, b, and c are integers."

            Answer = f"{a}n^2 + {b}n + {c}"

            self.QuestionCreator(QuestionText, Answer, notes, 8, 1)


        def MidpointofLine():
            x1 = self.random_integer(-20,20)
            x2 = self.random_integer(-20,20)
            y1 = self.random_integer(-20,20)
            y2 = self.random_integer(-20,20)

            QuestionText = f"Two points on a straight line have coordinates ({x1}, {y1}) and ({x2}, {y2}). \nFind the coordinates of the midpoint of the line"
            Notes = "Give your answer to 2d.p (a, b)"
            Answer = f"({((x1 + x2) / 2):.2f}, {((y1 + y2) / 2):.2f})"

            self.QuestionCreator(QuestionText, Answer, Notes, 2, 1)

        def ExpandDoubleBrackets():
            a = self.random_integer(1, 5)
            b = self.random_integer(0,20)
            c = self.random_integer(0, 5)
            d = self.random_integer(0,20)

            # (ax + b)(cx + d)

            QuestionText = f"Expand and simplify ({a}x + {b})({c}x + {d})"
            Notes = f"Give your answer in the form ax^2 + bx + c."
            Answer = f"{a * c}x^2 + {(a * d) + (b * c)}x + {b * d}"

            self.QuestionCreator(QuestionText, Answer, Notes, 4, 1)
            

        def SolvingHarderEquations():
            a = self.random_integer(1, 10)
            b = self.random_integer(0,20)
            c = self.random_integer(0, 10)
            d = self.random_integer(0,20)

            # ax + b = cx + d

            QuestionText = f"Solve {a}x + {b} = {c}x + {d}"
            Notes = "Give your answer to 2dp"
            Answer = f"{(d-b)/(a-c):.2f}" # found a way to always set the answer to 2dp

            self.QuestionCreator(QuestionText, Answer, Notes, 4, 1)



        def SolveLinearInequalities():
            a = self.random_integer(11, 20)
            b = self.random_integer(0,20)
            c = self.random_integer(1, 10)
            d = self.random_integer(0,20)

            # ax + b = cx + d

            QuestionText = f"Solve {a}x + {b} < {c}x + {d}"
            Notes = "Give your answer to 2dp, and in the form x < / > / = (your answer)"
            Answer = f"x < {(d-b)/(a-c):.2f}" # found a way to always set the answer to 2dp

            self.QuestionCreator(QuestionText, Answer, Notes, 5, 1)


        def LinearSimultaneousEquations():
            # Generate random coefficients for the equations
            a = self.random_integer(1, 10)
            b = self.random_integer(1, 10)
            c = self.random_integer(1, 10)
            d = self.random_integer(1, 10)
            e = self.random_integer(1, 10)
            f = self.random_integer(1, 10)

            # Form the equations ax + by = c and dx + ey = f
            QuestionText = f"Solve the simultaneous equations:\n{a}x + {b}y = {c}\n{d}x + {e}y = {f}"
            Notes = "Give your answer in the form x = answer, y = answer. (Don't forget spaces). And give your answers to 2 d.p"

            # Solve the equations
            # ax + by = c
            # dx + ey = f

            # Solving for x:
            # 1) aex + bey = ce (multiplied by e)
            # 2) bdx + bey = bf # (multiplied by b)

            # 1 - 2
            # (ae - bd)x = ce - bf
            # x = (ce - bf) / (ae - bd)

            # ----
            # Solving for y
            # Rearrange equation 1
            # y = (c - ax) / b


            x = (((c * e) - (b * f)) / ((a * e) - (b * d)))
            y = ((c - (a * x)) / b)


            Answer = f"x = {x:.2f}, y = {y:.2f}"

            # Create the question
            self.QuestionCreator(QuestionText, Answer, Notes, 7, 1)


        def QuadraticSimultaneousEquations():
            # Generate random coefficients for the equations


            a = self.random_integer(10, 30)
            b = self.random_integer(1, 5)
            c = self.random_integer(1, 10)
            d = self.random_integer(1, 10)
            e = self.random_integer(1, 10)
            f = self.random_integer(1, 3)

            # Equations: ax + by = c
            #  dx^2 + ey + f = 0
            QuestionText = f"Solve the simultaneous equations:\n{a}x + {b}y = {c} \n{d}x\u00B2 + {e}y + {f} = 0" 
            Notes = "Give your answer as the sum of all the solutions. \nIf there are no real solutions, type: No real solutions"

            # Rearrange for y
            # ax + by = c
            # y = (c - ax) / b

            # Substitute y in the quadratic equation and solve for x
            # dx^2 + e((c - ax) / b) + f = 0

            # make the discriminant so we can check whether the roots are real

            # check Questions Log for algebra. done on paper 


            A = d
            B = (-a * e) / b
            C = ((e * c) / b) + f

            discriminant = B**2 - 4 * A * C

            if discriminant < 0:
                Answer = "No real solutions" # if no valid answers

            else:
                x1 = (-B + math.sqrt(discriminant)) / (2 * A) # quadratic formula for first x value
                x2 = (-B - math.sqrt(discriminant)) / (2 * A) # quadratic formula for second x value

                y1 = (c - a * x1) / b # # first y value associated with 1st x value
                y2 = (c - a * x2) / b # second y value associated with 2nd y value

                Answer = f"{(x1 + x2 + y1 + y2):.2f}"

            self.QuestionCreator(QuestionText, Answer, Notes, 9, 1) # grade 9 question


        def FactoriseSolveQuadratics():
            a = self.random_integer(1, 5) # x - a
            b = self.random_integer(6, 11) # x - b

            # (x - a)(x - b)
            # x^2 - (a+b)x + ab

            QuestionText = f"Factorise x\u00B2 - {a+b}x + {a*b}" # expands
            Notes = "Give your answer in the form (x - a)(x - b), where a < b. Don't forget the spaces."
            Answer = f"(x - {a})(x - {b})"

            self.QuestionCreator(QuestionText, Answer, Notes, 5, 1)


        def EquationofStraightLine():
            x1 = self.random_integer(1,20) # generate the 2 sets of coordiantes
            y1 = self.random_integer(1,20)

            x2 = self.random_integer(21,40)
            y2 = self.random_integer(40,80)

            QuestionText = f"Find the equation of the straight line joining the points \n({x1},{y1}) and ({x2}, {y2})" # output the question
            Notes = "Give your answer in the form \ny = mx + c,\nwhere all m, c are given to 2 d.p"
            

            m = (y2 - y1) / (x2 - x1) # calculate the gradient 
            c = y2 - (m * x2) # y intercept
            
            if c < 0:
                Answer = f"y = {m:.2f}x - {abs(c):.2f}" # adjust for negatives
            else:
                Answer = f"y = {m:.2f}x + {c:.2f}"

            # Create the question
            self.QuestionCreator(QuestionText, Answer, Notes, 5, 1, font_size=12)




        def TurningPointofQuadratic(): # find quadratic equation from coordinate turning points
            a = r.randint(1,20)
            b = r.randint(1,20)


            QuestionText = f"Find the equation of the quadratic with turning point ({a},{b})"
            Notes = "Give your answer in the form x^2 + bx + c."
            Answer = f"x^2 - {2*a}x + {a**2 + b}"

            self.QuestionCreator(QuestionText, Answer, Notes, 8, 1)



        def GeometricProgression():
            a = r.randint(2,5)  # initial value
            d = r.randint(2,4) # common ratio

            QuestionText = f"A geometric progression has initial value {a}, \nand common ratio {d}. \nFind the 5th term in the sequence."
            Answer = (a * d ** 4) # equation for geometric series
            Notes = ""

            self.QuestionCreator(QuestionText, Answer, Notes, 6, 1)
        


        def ExpandTripleBrackets(): # expanding triple brackets
            # generating the 3 values
            a = r.randint(1,6) #
            b = r.randint(1,6)
            c = r.randint(1,6)



            QuestionText = f"Expand (x - {a})(x - {b})(x - {c})"
            Notes = "Give your answer in the form ax^3 +/- bx^2 +/- cx +/- d"
            Answer = f"x^3 - {a + b + c}x^2 + {a*b + a*c + b*c}x - {a*b*c}" # using algabraic formula

            self.QuestionCreator(QuestionText, Answer, Notes, 6, 1)



        def EquationofCircle(): #²²²²²²²²
            rad = r.randint(1,100)

            QuestionText = f"Find the radius of the circle with equation x² + y² = {rad}"
            Notes = "Give your answer to 2 d.p"
            Answer = f"{math.sqrt(rad):.2f}"

            self.QuestionCreator(QuestionText, Answer, Notes, 5, 1)

        def PerpendicularBisector():
            # y = mx + c
            m1 = r.randint(1, 15)
            c1 = r.randint(1, 15)


            root = float(f"{-c1 / m1}") # where original line goes through the x axis


            QuestionText = f"Find the x-intercept of the \nperpendicular bisector of the line which goes through \nA({root}, 0) B(0, {c1})"

            # goes through the midpoint of AB
            midx = root / 2
            midy = c1/2

            m2 = -1 / m1 # perpendicular gradient

            c2 = midy + (midx / m1) # calculating the new y intercept

            Answer = f"{(-c2 / m2):.2f}" # x intercept when y = 0
            Notes = "Give your answer to 2 d.p"

            self.QuestionCreator(QuestionText, Answer, Notes, 9, 1) # g 9 question



        def CompleteSquare(): # ax^2 + bx + c. a = 1
            b = r.randint(1,5)
            b = b * 2 # makes it more convenient for halfing
            c = r.randint(25,50) # greater than the max value of b^2/4

            QuestionText = f"Complete the square on x² + {b}x + {c}"
            Notes = "Give your answer in the form (x + b)^2 + c, giving c to 2 d.p"
            Answer = f"(x + {int(b/2)})^2 + {int(-((b**2)/4) + c)}" # answer formatting

            self.QuestionCreator(QuestionText, Answer, Notes, 7, 1)


        def HarderCompleteSquare(): # ax^2 + bx + c. a > 1
            a = r.randint(2, 5)  # Choose a value for a greater than 1
            b = r.randint(2, 5)  
            b = (b * 2) + 1 # ensuring no common factor with a
            
            c = r.randint(13, 30) # c must be greater than 12.5 (b^2/4a)

            
            d = b/(2 * a) # finding term inside bracket
            e = c - (b ** 2 / (4 * a))  # term outside bracket

            QuestionText = f"Complete the square on {a}x² + {b}x + {c}"
            Notes = "Give your answer in the form a(x + d)^2 + e, giving d and e to 2 d.p"
            Answer = f"{a}(x + {d:.2f})^2 + {e:.2f}"  # Answer formatting with 2 decimal places
            
            self.QuestionCreator(QuestionText, Answer, Notes, 8, 1)



        def SolveAlgebraFractions():
            # generating all sets of values in the 
            a = r.randint(2,15)     
            b = r.randint(2,15)
            c = r.randint(2,15)
            d = r.randint(2,15)
            k = r.randint(2,15)

            x = ((d * k) - b)/(a - (c * k)) # rearranging and solving for x

            QuestionText = f"Solve ({a}x + {b})/({c}x + {d}) = {k}"
            Notes = "Give your answer to 2 d.p"
            Answer = f"{x:.2f}" # rounding to 2 d.p

            self.QuestionCreator(QuestionText, Answer, Notes, 7, 1)


        def QuadraticInequalities():
            a = r.randint(1,7) # generating thhe 2 factored numbers
            b = r.randint(8,12)
            # (x-a)(x-b) a < b
            QuestionText = f"Solve the quadratic inequality: \nx² - {a + b}x + {a * b} < 0"
            Notes = "Give your answer in the form x < a, x > b, where a < b, OR as a<x<b"
            Answer = f"{a}<x<{b}"

            self.QuestionCreator(QuestionText, Answer, Notes, 7, 1)



        def CompositeFunction():
            # creating f(x)
            a = r.randint(2,10)
            b = r.randint(2,10)
            # f(x) = ax + b

            # creating g(x)
            i = r.randint(2,5)
            j = r.randint(2,15)
            k = r.randint(2,20)

            QuestionText = f"f(x) = {a}x + {b}, g(x) = {i}x² + {j}x + {k}. Find g(f(x))."
            Notes = "Give your answer in the form ax^2 + bx + c"
            Answer = f"{(a**2) * i}x^2 + {(2 * a * b * i) + (a * j)}x + {(b**2 * i) + (b * j) + k}" # algebraically finding all the values

            self.QuestionCreator(QuestionText, Answer, Notes, 7, 1)

        def SolveCompositeFunction():
            # creating f(x)
            a = r.randint(2,10)
            b = r.randint(2,10)
            # f(x) = ax + b

            # creating g(x)
            i = r.randint(2,5)
            j = r.randint(40,100)
            k = r.randint(1,12) # k < j^2/4i # guarantees that the quadratic always has a solution

            # all coefficients
            w = (a**2) * i 
            y = (2 * a * b * i) + (a * j)
            z = (b**2 * i) + (b * j) + k
            # calculating discriminant
            discriminant = (y**2) - (4 * w * z)

            if discriminant < 0:
                Answer = "unreal"
            else:
                # Using quadratic formula to find roots
                x1 = (-y + math.sqrt(discriminant)) / (2 * w)
                x2 = (-y - math.sqrt(discriminant)) / (2 * w)
                Answer = f"x=({x1:.2f},{x2:.2f})"

            QuestionText = f"f(x) = {a}x + {b}, g(x) = {i}x² + {j}x + {k}. \nSolve g(f(x))."
            Notes = "Write your answer as x=(a,b). \nb > a. \nNo solutions: enter 'unreal"
            self.QuestionCreator(QuestionText, Answer, Notes, 9, 1)



        def ChoosingQuestion(): # function which chooses a question to be output randomly. This cannot be outside the
            completed_functions = [FunctionMachine, ExpandSingleBrackets, Substitution, SolvingEquations, GenerateSequence, GradientofLine, RearrangeFormula, Simple_nth_Term, RearrangeFormula, Hard_nth_Term, MidpointofLine, ExpandDoubleBrackets, SolvingHarderEquations, SolveLinearInequalities, LinearSimultaneousEquations, QuadraticSimultaneousEquations, FactoriseSolveQuadratics, EquationofStraightLine, TurningPointofQuadratic, ExpandTripleBrackets, GeometricProgression, EquationofCircle, PerpendicularBisector, CompleteSquare, HarderCompleteSquare, SolveAlgebraFractions, QuadraticInequalities, CompositeFunction, SolveCompositeFunction]

            choice = r.choice(completed_functions)
            choice()
        
        ChoosingQuestion()


    def Ratio(self):
        self.page_clearer(self.window)


        # self.QuestionCreator(QuestionText, Answer, Notes, 4, 1)

        def CurrencyExchange():
            a = r.uniform(1, 100)
            twodp_a = f"{a:.2f}"

            QuestionText = f"£1.00 is equivalent to $1.29 .\nConvert £{twodp_a} to $"
            Notes = ""
            Answer = float(twodp_a) * 1.29
            Answer_2dp = f"{Answer:.2f}"

            self.QuestionCreator(QuestionText, Answer_2dp, Notes, 4, 2)


            
        
        def Sharing():
            tot_money = r.randint(100, 1000)
            person_a = r.randint(1,10)
            person_b = r.randint(1,10)

            QuestionText = f"A and B share £{tot_money} in the ratio {person_a}:{person_b}. \nFind out how much person B gets."
            Notes = "Remember money rounds to 2 d.p"
            Answer = (((person_b) / (person_a + person_b)) * tot_money)
            Answer_2dp = f"{Answer:.2f}"

            self.QuestionCreator(QuestionText, Answer_2dp, Notes, 5, 2)


        def PerChange():
            initial = r.randint(1,10000)
            final = r.randint(1,100000)

            QuestionText = f"The cost of an item was £{initial}. \nA year later it cost £{final}. \nFind the percentage change in price."
            Notes = "Give your answer to 2 d.p"
            Answer = ((final - initial) / initial) * 100
            Answer_2dp = f"{Answer:.2f}"

            self.QuestionCreator(QuestionText, Answer_2dp, Notes, 2, 2, font_size = 18)



        def SimpleInterest():

            initial = r.randint(1,10000) # initial money in account
            no_of_years = r.randint(2,15) # how long the investment is for
            PerC = r.randint(1,10) # the simple percentage increase for the money

            QuestionText = f"£{initial} was invested for {no_of_years} years at {PerC}% simple interest. \nHow much interest was earned in total?" # output to user
            Notes = "" # none required
            Answer = (PerC / 100) * (initial) * (no_of_years) # calculation for simple interest formula
            Notes = "Give a unit"
            Answer_2dp = f"{Answer:.2f}" # money to 2 dp

            self.QuestionCreator(QuestionText, Answer_2dp, Notes, 5, 2) # informaion to create the question
            

        def SimilarShapes():
            initial = r.randint(1,10) # initial length of triangle
            scale_factor = r.randint(2,10) # new lenght of triangle

            QuestionText = f"A triangle has length {initial}cm on vertice AB.\n The triangle is enlarged by scale factor {scale_factor}. \nFind the new length of AB."  # question to be output
            Notes = ""
            Answer = f"{initial * scale_factor}cm" # calculation for new length

            self.QuestionCreator(QuestionText, Answer, Notes, 5, 2, shape = "right_triangle") # first time incorporating kwarg "shape"


        def CompoundInterestInc():
            initial = r.randint(1,10000) # initial money in account
            no_of_years = r.randint(2,15) # how long the investment is for
            PerC = r.randint(1,10) # the percentage increase for the money

            QuestionText = f"£{initial} was invested into a savings account, which appreciates by {PerC}% a year. \nHow much is in the saving account after {no_of_years} years?" # output to user
            Notes = "" # none required
            Answer = (initial * ((PerC / 100) + 1)**no_of_years) # caluclation for appreciating compound interest formula
            Answer_2dp = f"{Answer:.2f}" # money to 2 dp

            self.QuestionCreator(QuestionText, Answer_2dp, Notes, 6, 2, font_size = 15) # smaller font size for more text, grade 7 q
            
        
        def CompoundInterestDec():
            initial = r.randint(1,10000) # initial cost
            no_of_years = r.randint(2,15) # how long it is owned for
            PerC = r.randint(1, 10) # percentage depreciatiion

            QuestionText = f"A car cost £{initial} when new. It depreciates by {PerC}% a year. \nHow much is the car worth after {no_of_years} years?" # output to user
            Notes = "" # none required
            Answer = (initial * ((1 - PerC / 100))**no_of_years) # caluclation for depreciating compound interest formula
            Answer_2dp = f"{Answer:.2f}" # money to 2 dp

            self.QuestionCreator(QuestionText, Answer_2dp, Notes, 7, 2, font_size = 16) # smaller font size for more text, grade 7 q




        def DirectProportion():
            y = r.randint(2, 10) # value for y
            k = r.randint(1, 20) # constant of proportionality


            QuestionText = f"y is directly proportional to x. When y = {y}, x = {y * k}.\nFind the constant of proportionality." # output text
            Answer = k
            Notes = ""

            self.QuestionCreator(QuestionText, Answer, Notes, 6, 2)


        def HardDirectProportion():
            x = r.randint(2,10) # the value of x 
            k = r.randint(5,25) # constant of proportionality

            y = r.randint(11,25) # value of y

            newY = f"{math.sqrt(k * x):.4f}" # value of y given in the question with the x value associated with it
            newY = float(newY) # setting as float

            QuestionText = f"y\u00B2 is directly proportional to x. When x = {x}, y = {newY}. Find x when y = {y}" # output
            Answer = (y**2) / k # calculating the answer
            Notes = "Give your answer to 3 d.p" 
            Answer_3dp = f"{Answer:.3f}" # answer to 3 d.p

            self.QuestionCreator(QuestionText, Answer_3dp, Notes, 9, 2)




        def InverseProportion():
            x = r.randint(2, 10)  # value of 
            y = r.randint(11, 25)

            k = (y * x**2) # calculated k

            y2 = r.randint(3,17) # random value of y for user to find

            QuestionText = f"y is inversely proportional to x\u00B2. When y = {y}, x = {x}. Find x when y = {y2}" # question
            Notes = "Give your answer to 3 d.p"
            Answer = math.sqrt(k / y2) # calculating x when y = y2
            Answer_3dp = f"{Answer:.3f}" # producing answer to 3 d.p
            self.QuestionCreator(QuestionText, Answer_3dp, Notes, 9, 2) # passing parameters


        def ChoosingQuestion(): # function which chooses a question to be output randomly. This cannot be outside the
            choosable_questions = [CurrencyExchange, Sharing, PerChange, SimpleInterest, SimilarShapes, CompoundInterestInc, CompoundInterestDec, DirectProportion, HardDirectProportion, InverseProportion]
            
            completed_questions = [CurrencyExchange, Sharing, PerChange, CompoundInterestInc, CompoundInterestDec, SimpleInterest, SimilarShapes, DirectProportion, HardDirectProportion, InverseProportion]

            choice = r.choice(choosable_questions)

            choice()
        
        ChoosingQuestion()



    def Geometry(self):
        self.page_clearer(self)

        def InteriorAngle():
            n = r.randint(3,12) # n = no of sides the shape has

            QuestionText = f"What are the interior angles on a regular {n}-sided shape?" # q
            Answer = round(((n-2) * 180) / n) # formula for interior angles

            Notes = "Round your answer to the nearest whole number" # most are whole numbers with a few exceptions such as 7

            self.QuestionCreator(QuestionText, Answer, Notes, 5, 3) 


        def ExteriorAngle():
            n = r.randint(3,12) # no of sides

            QuestionText = f"What are the exterior angles on a regular {n}-sided shape?" # q
            Answer = round(360/n) # formula for exterior angles
            Notes = "Round your answer to the nearest whole number" # rounding requirement


            self.QuestionCreator(QuestionText, Answer, Notes, 4, 3) # parameters




        def AnglesOnLine():
            angle = r.randint(1,180) # setting original angle

            QuestionText = f"An angle on a straight line is {angle} degrees. \nFind the remaining angle." # q
            Answer = 180 - angle # calculation for result
            Notes = ""

            self.QuestionCreator(QuestionText, Answer, Notes, 2, 3)



        def ReflectionX():
            x = r.randint(-100,100) # original coordinates
            y = r.randint(-100, 100) 

            QuestionText = f"The coordinates ({x},{y}) are mapped to ({x}, {-1 * y}).\nIs this a reflection in the x-axis, y-axis or both?" # question
            Notes = "Give your answer as 'y', 'x', or 'both'"
            Answer = "x" # y value change so x reflection

            self.QuestionCreator(QuestionText, Answer, Notes, 2, 3) # parameters

        def ReflectionY():
            x = r.randint(-100,100) # original coordinates
            y = r.randint(-100, 100)

            QuestionText = f"The coordinates ({x},{y}) are mapped to ({-1 * x}, {y}).\nIs this a reflection in the x-axis, y-axis or both?" # question
            Notes = "Give your answer as 'y', 'x', or 'both'"
            Answer = "y" # y value change so x reflection

            self.QuestionCreator(QuestionText, Answer, Notes, 2, 3) 

        def ReflectionBoth():
            x = r.randint(-100,100) # original coordinates
            y = r.randint(-100, 100)

            QuestionText = f"The coordinates ({x},{y}) are mapped to ({-1 * x}, {-1 * y}).\nIs this a reflection in the x-axis, y-axis or both?" # question
            Notes = "Give your answer as 'y', 'x', or 'both'"
            Answer = "both" # both are changes so reflected in both

            self.QuestionCreator(QuestionText, Answer, Notes, 2, 3)


        def Translations():
            x = r.randint(-100,100) # original coordinates
            y = r.randint(-100, 100) 

            vectorX = r.randint(-10, 10) # vectir vals
            vectorY = r.randint(-10, 10)

            QuestionText = f"The point ({x}, {y}) is translated by vector [{vectorX}, {vectorY}].\nFind the new coordinates."
            Notes = "Give your answer in the form (a,b)."
            Answer = f"({x + vectorX},{y + vectorY})"

            self.QuestionCreator(QuestionText, Answer, Notes, 3, 3)


        def RectanglePerimeter():
            a = r.randint(1,50) # base
            b = r.randint(1,50) # heiught

            QuestionText = f"A rectangle has dimensions {a}x{b}. \nFind the perimeter."
            Notes = ""
            Answer = (2*a) + (2*b) # calc for perimeter of a shape

            self.QuestionCreator(QuestionText, Answer, Notes, 2, 3, shape = "rectangle")


        def RectangleArea():
            a = r.randint(1,50)
            b = r.randint(1,50)

            QuestionText = f"A rectangle has perimeter {2*a + 2*b}, and 2 side lengths with length {a}. \nFind the area." # slightly harder q need to figure out more information
            Notes = ""
            Answer = a * b # calc. for area of rectangle, but q. makes it harder as need to figure out remaining lenght

            self.QuestionCreator(QuestionText, Answer, Notes, 5, 3, shape = "rectangle") # passing shape

        def TriangleArea():
            base = r.randint(1, 50)
            height = r.randint(1, 50)

            QuestionText = f"A triangle has a base of {base} and a height of {height}. \nFind the area."
            Notes = "Give your answer to 2 d.p"
            Answer = 0.5 * base * height # calc for triangle area
            Answer2dp = f"{Answer:.2f}"
            self.QuestionCreator(QuestionText, Answer2dp, Notes, 3, 3, shape = "triangle")


        def ParallelogramArea():
            base = r.randint(1, 50) 
            height = r.randint(1, 50)

            QuestionText = f"A parallelogram has a base of {base} and a height of {height}. \nFind the area."
            Notes = ""
            Answer = base * height

            self.QuestionCreator(QuestionText, Answer, Notes, 3, 3)


        def TrapeziumArea():
            base1 = r.randint(1, 50) # 2 bases as both are required for area
            base2 = r.randint(1, 50)
            height = r.randint(1, 50)

            QuestionText = f"A trapezium has bases of {base1} and {base2}, and a height of {height}. \nFind the area."
            Notes = "Give your answer to 2 d.p"
            Answer = 0.5 * (base1 + base2) * height # calc for area of a trapezium
            Answer2dp = f"{Answer:.2f}"

            self.QuestionCreator(QuestionText, Answer2dp, Notes, 5, 3)


        def MetricConversions(): # m to cm
            
            meters = r.randint(1, 100)
            centimeters = meters * 100 # conversion rate

            QuestionText = f"Convert {meters} meters to centimeters."
            Notes = ""
            Answer = int(centimeters) # will be integer value

            self.QuestionCreator(QuestionText, Answer, Notes, 1, 3) # gr 1


        def SurfaceAreaofCuboid():
            l = r.randint(1, 50) # length
            w = r.randint(1, 50) # width
            h = r.randint(1, 50) # height


            QuestionText = f"A rectangular prism has dimensions {l}x{w}x{h}. \nFind its surface area." # rectangular prism = cuboid
            Notes = ""
            Answer = 2 * (l * w + l * h + w * h) # calculation for surface area of a rectangular prism

            self.QuestionCreator(QuestionText, Answer, Notes, 4, 3)


        def SurfaceAreaofSphere():
            rad = r.randint(1, 50) # radius
            pi = 3.14159265
            surface_area = 4 * pi * (rad ** 2) # formula for area of sphere

            QuestionText = f"A sphere has a radius of {rad}. \nFind its surface area."
            Notes = "Give your answer to 2 d.p"
            Answer = f"{surface_area:.2f}"

            self.QuestionCreator(QuestionText, Answer, Notes, 3, 3)


        def VolofCuboid():
            l = r.randint(1, 50) # length
            w = r.randint(1, 50) # width
            h = r.randint(1, 50) # height

            QuestionText = f"A cuboid has dimensions {l}x{w}x{h}. \nFind its volume."
            Notes = ""
            Answer = l * w * h

            self.QuestionCreator(QuestionText, Answer, Notes, 2, 3)


        def AreaofCircle():
            radius = r.randint(1, 50)
            area = 3.14159 * radius ** 2 # calculation for are of circle

            QuestionText = f"A circle has a radius of {radius}. \nFind the area."
            Notes = "Give your answer to 2 d.p"
            Answer = f"{area:.2f}"

            self.QuestionCreator(QuestionText, Answer, Notes, 2, 3, shape = "circle")


        def PerimeterofCircle():
            radius = r.randint(1, 50)
            perimeter = 2 * 3.14159 * radius # calc for per. of circle

            QuestionText = f"A circle has a radius of {radius}. \nFind the circumference."
            Notes = "Give your answer to 2 d.p"
            Answer = f"{perimeter:.2f}"

            self.QuestionCreator(QuestionText, Answer, Notes, 2, 3, shape = "circle")


        def AreaofSector():
            radius = r.randint(1, 50)
            x = r.randint(1, 360) # angle
            area_of_sector = (x / 360) * (3.14159 * (radius ** 2)) # x/360 * pi * r^2 = area of sector

            QuestionText = f"A sector of a circle has radius {radius} and an angle of {x}°. \nFind its area." # google symbols and can just copy them. Do this in future instead of \u... e.g 3⁵
            Notes = "Give your answer to 2 d.p"
            Answer = f"{area_of_sector:.2f}"

            self.QuestionCreator(QuestionText, Answer, Notes, 4, 3, shape = "circle")

        def AnglesinParallelLines(): # questions do not need multiple functions, can just use r.choice function as has been used for chjoosing questions, given that the grade of each question is the same
            angle = r.randint(10, 160)
            angle_type = r.choice(["corresponding", "alternate", "co-interior"]) # all 3 angle types
            
            if angle_type == "corresponding" or angle_type == "alternate": # both are the same 
                other_angle = angle
                grade = 4

            elif angle_type == "co-interior": # co-interior angles add up to 180 deg
                other_angle = 180 - angle
                grade = 5

            
            QuestionText = f"Two angles have the {angle_type} property. One angle is {angle}° \nFind the {angle_type} angle."
            Answer = other_angle

            Notes = ""

            self.QuestionCreator(QuestionText, Answer, Notes, grade, 3)


        def AnglesinTriangle():
            a = r.randint(30, 80) # a, b must be lesss than 90 otherwise c could be 0 and no triangle
            b = r.randint(30, 80)
            c = 180 - (a + b) # all 3 angles in a triangle

            QuestionText = f"A triangle has angles of {a}° and {b}°. \nFind the third angle."
            Notes = ""
            Answer = c

            self.QuestionCreator(QuestionText, Answer, Notes, 3, 3, shape = "triangle")


        def Bearings():
            start_bearing = r.randint(0, 360)
            angle_change = r.randint(0,360)

            QuestionText = f"A plane flies on a bearing of {start_bearing}°, then turns {angle_change}° clockwise. \nWhat is its new bearing?"
            Notes = ""
            Answer = (start_bearing + angle_change) % 360 # starts from vertically upwards, and measures clockwise  must be within 360 deg.

            self.QuestionCreator(QuestionText, Answer, Notes, 5, 3)


        def Pythagoras():
            options = ["hyp", "base"]
            x = r.choice(options)

            if x == "hyp": # find hypotenuse
                base = r.randint(1, 100) # base and heihgt can be anything
                height = r.randint(1, 100)
                Answer = (base**2 + height**2)**0.5 # c = (a^2 + b^2)^1/2
                QuestionText = f"Find the hypotenuse of a right triangle with base {base} and height {height}."
                Grade = 4 # lower grade question

            if x == "base": # finding base of triangle
                hypotenuse = r.randint(1, 100)
                height = r.randint(1, hypotenuse - 1) # restriction on height as it must be less than the hypotenuse
                Answer = (hypotenuse**2 - height**2)**0.5 # b = (c^2 - a^2)**0.5

                QuestionText = f"Find the base of a right triangle with hypotenuse {hypotenuse} and height {height}."
                Grade = 5

            Notes = "Give your answer to 2 d.p"
            Answer2dp = f"{Answer:.2f}"  # Rounding the answer for simplicity

            self.QuestionCreator(QuestionText, Answer2dp, Notes, Grade, 3, shape = "right_triangle")


        def Enlargement():
            scale_factor = r.randint(1, 30)
            original_length = r.randint(5, 20)

            QuestionText = f"A square has an original lengths of {original_length}.\nIt is enlarged by length scale factor {scale_factor}.\nWhat is it's new area?"
            Notes = ""
            Answer = (original_length**2 * scale_factor **2) # area * sf ^2

            self.QuestionCreator(QuestionText, Answer, Notes, 6, 3, shape = "square")



        def SimpleVectors():

            x1, y1 = r.randint(1, 100), r.randint(1, 100) # 2 random vectors
            x2, y2 = r.randint(1, 100), r.randint(1, 100)

            QuestionText = f"Find the sum of the vectors ({x1}, {y1}) and ({x2}, {y2})" # add vectors together
            Notes = "Give your answer in the form (a,b)"
            Answer = f"({x1 + x2},{y1 + y2})"

            self.QuestionCreator(QuestionText, Answer, Notes, 2, 3)

        def HarderVectors():

            x, y = r.randint(1, 100), r.randint(1, 100) # generate 2 random vectors

            MagA = (x**2 + y**2)**0.5 # magnitude of vector calculation
            Angle = math.degrees(math.atan2(y, x)) # tan inverse y/x in degrees
            

            QuestionText = f"Find the magniude of the vector ({x}, {y}), and its angle to the horizontal."
            Notes = "Give your answer in the form '(magnitude,angle)' both to 2 d.p" # format
            Answer = f"({MagA:.2f},{Angle:.2f})" 

            self.QuestionCreator(QuestionText, Answer, Notes, 7, 3)



        def CircleTheorems(): # 4 of the circle theorems. Hard to word the rest
            theorem_type = r.choice(["central_angle", "inscribed_angle", "angle_in_semi_circle", "cyclic_quadrilateral"])
            
            if theorem_type == "central_angle": # central angle
                angle_at_center = r.randint(30, 150) # creating the angle at the center
                angle_at_circumference = angle_at_center / 2 # Theorem: The angle at the center is twice the angle at the circumference.
                QuestionText = f"Find the angle subtended at the circumference if the angle subtended at the center is {angle_at_center}°." # q
                Answer = f"{angle_at_circumference:.1f}" # formatting
                Notes = "Give your answer to 1 d.p" # odd number being halved
            
            elif theorem_type == "inscribed_angle":
                angle_at_circumference = r.randint(30, 150) # creating angle at the circumference
                angle_at_center = 2 * angle_at_circumference # The angle at the center is twice the angle at the circumference. just the opposite of central angle
                QuestionText = f"Find the angle subtended at the center if the angle subtended at the circumference is {angle_at_circumference}°." # q
                Answer = angle_at_center 
                Notes = ""

            elif theorem_type == "angle_in_semi_circle": 

                QuestionText = "What is the angle subtended by a diameter in a circle?" # angle subtended by a diameter is a right angle.
                Answer = 90 # always
                Notes = ""

            elif theorem_type == "cyclic_quadrilateral": 
                angle = r.randint(30, 120) # creating first angle
                opposite = 180 - angle # answer angle

                QuestionText = f"In a cyclic quadrilateral, one angle is {angle}, what is the opposite angle?." # The sum of the opposite angles in a cyclic quadrilateral is 180 deg
                Answer = opposite
                Notes = ""

            
            self.QuestionCreator(QuestionText, Answer, Notes, 7, 3, shape="circle", font_size = 18)


        def SinCosTan():
            theorem_type = r.choice(["find_side", "find_angle"])  # either finding an angle or side
            trig = r.choice(["sin", "cos", "tan"])  # which trigonometric function will be used

            if theorem_type == "find_side":
                angle = r.randint(15, 75)  # creating angle
                hypotenuse = r.randint(10, 20)  # hypotenuse length
                opposite = hypotenuse * math.sin(math.radians(angle))  # calculating opposite
                adjacent = hypotenuse * math.cos(math.radians(angle))  # calculating adjacent
                


                if trig == "sin":
                    QuestionText = f"A right triangle has hypotenuse length {hypotenuse}, and angle {angle}°.\nFind the length of the opposite side to the angle."
                    Answer = f"{opposite:.2f}"
                elif trig == "cos":
                    QuestionText = f"A right triangle has hypotenuse length {hypotenuse}, and angle {angle}°.\nFind the length of the adjacent side to the angle."
                    Answer = f"{adjacent:.2f}"
                elif trig == "tan":
                    QuestionText = f"A right triangle has angle {angle}° and adjacent side length {adjacent:.3f}.\nFind the length of the opposite side."
                    Answer = f"{opposite:.2f}"

            elif theorem_type == "find_angle":
                opposite = r.randint(5, 15)  # opposite and adjacent side lengths
                adjacent = r.randint(5, 15)
                hypotenuse = (opposite**2 + adjacent**2)**0.5  # calculating hypotenuse
                Notes = ""

                if trig == "sin":
                    angle = math.degrees(math.asin(opposite / hypotenuse)) # calculating the necessary angle
                    QuestionText = f"A right triangle has hypotenuse length {hypotenuse:.3f}, and the opposite side to the angle is {opposite}.\nFind the angle."
                elif trig == "cos":
                    angle = math.degrees(math.acos(adjacent / hypotenuse))
                    QuestionText = f"A right triangle has hypotenuse length {hypotenuse:.3f}, and the adjacent side to the angle is {adjacent}.\nFind the angle."
                elif trig == "tan":
                    angle = math.degrees(math.atan(opposite / adjacent))
                    QuestionText = f"A right triangle has opposite side length {opposite} and adjacent length {adjacent}.\nFind the angle."

                Answer = f"{angle:.2f}"

            
            Notes = f"Give your answer to 2 d.p"

            self.QuestionCreator(QuestionText, Answer, Notes, 6, 3, shape="right_triangle", font_size=18)



        def ExactTrigValues():
            angles = [0, 30, 45, 60, 90]
            trig_functions = ['sin', 'cos', 'tan']
            
            exact_values = { # using a dictionary for the first time
                'sin': {0: '0', 30: '1/2', 45: 'root(2)/2', 60: 'root(3)/2', 90: '1'},
                'cos': {0: '1', 30: 'root(3)/2', 45: 'root(2)/2', 60: '1/2', 90: '0'},
                'tan': {0: '0', 30: 'root(3)/3', 45: '1', 60: 'root(3)', 90: 'undefined'}
            }


            angle = r.choice(angles) # choosing a random combination
            trig_function = r.choice(trig_functions)

            QuestionText = f"What is the exact value of {trig_function}({angle}°)?" #q
            Answer = exact_values[trig_function][angle] # using the dictionary to find the answer
            Notes = "No calculator. \nUse exact values.\nExamples: 'root(2)/4, 1/4, undefined"

            self.QuestionCreator(QuestionText, Answer, Notes, 7, 3, shape = "triangle")

        def SinRule():
            find = r.choice(["side", "angle"]) # choice between finding a side or an angle, similar to previous questions
            
            # sinA/a = sinB/b
            # not generating the same angles for both as it would generate unpleasant numbers as discovered in previous question


            if find == "side": # user must find the side
                A = r.randint(30, 80)  # Angle A
                B = r.randint(30, 80)  # Angle B
                a = r.randint(5, 20)  # Side a opposite angle A
                b = a * (math.sin(math.radians(B)) / math.sin(math.radians(A)))  # finding b using sin rule


                QuestionText = f"A triangle has angle A = {A}°, angle B = {B}°, and side a = {a}. \nFind the length of side b."
                Answer = f"{b:.2f}" #formatting
                Notes = "Give your answer to 2 d.p"
                grade = 7


            elif find == "angle":
                a = r.randint(5, 20)  # Side a
                b = r.randint(5, 20)  # Side b
                A = r.randint(30, 80)  # Angle A in degrees
                B = math.degrees(math.asin(b * math.sin(math.radians(A)) / a))  # Using the sine rule to find angle B


                QuestionText = f"A triangle has side a = {a}, side b = {b}, and angle A = {A}°.\nFind angle B."
                Answer = f"{B:.2f}"
                Notes = "Give your answer to 2 d.p"
                grade = 8


            self.QuestionCreator(QuestionText, Answer, Notes, grade, 3, shape="triangle", font_size = 15)


        def CosineRule():
                find = r.choice(["side", "angle"]) # side or angle like previously
                
                if find == "side":
                    a = r.randint(5, 20) # side a
                    b = r.randint(5, 20) # side b
                    C = r.randint(30, 120)  # Angle C in degrees
                    c = (a**2 + b**2 - 2*a*b*math.cos(math.radians(C)))**0.5  # c = sqrt(b^2 + c^2 - 2bcCosC)


                    QuestionText = f"A triangle has side a = {a}, side b = {b}, and angle C = {C}°. \nFind the length of c"
                    Answer = f"{c:.2f}"
                    Notes = "Give your answer to 2 d.p"
  




                elif find == "angle":
                    a = r.randint(5, 20)
                    b = r.randint(5, 20)
                    c = r.randint(5, 20)
                    C = math.degrees(math.acos((a**2 + b**2 - c**2) / (2*a*b)))  # C = acos(a^2 + b^2 - c^2 / 2ab)


                    QuestionText = f"A triangle has side a = {a}, side b = {b}, and side c = {c}. \nFind angle C"
                    Answer = f"{C:.2f}"
                    Notes = "Give your answer to 2 d.p"



                self.QuestionCreator(QuestionText, Answer, Notes, 9, 3, shape="triangle", font_size = 15)

        def HalfabSinc():

                a = r.randint(5, 20) # randomly generate 2 sides
                b = r.randint(5, 20)
                C = r.randint(30, 150)  # Angle C in degrees

                area = 0.5 * a * b * math.sin(math.radians(C))

                QuestionText = f"Find the area of a triangle where side a = {a}, side b = {b}, and angle C = {C}°." # question
                Answer = f"{area:.2f}"
                Notes = "Give your answer to 2 d.p"


                self.QuestionCreator(QuestionText, Answer, Notes, 5, 3, shape="triangle")


        def ThreeDPythagoras():
            # dimensions of cuboid
            x = r.randint(1, 20)
            y = r.randint(1, 20)
            z = r.randint(1, 20)

            # calculating diagonal length
            diagonal = math.sqrt(x**2 + y**2 + z**2)

            # Formulate the question
            QuestionText = f"A cuboid has side lengths of {x}, {y}, and {z}. \nFind the length of the diagonal connecting opposite corners."
            Answer = f"{diagonal:.2f}"
            Notes = "Give your answer to 2 d.p"
 

            self.QuestionCreator(QuestionText, Answer, Notes, 7, 3)




        def ChoosingQuestion(): # function which chooses a question to be output randomly. This cannot be outside the
            choosable_questions = [InteriorAngle, ExteriorAngle, AnglesOnLine, ReflectionX, ReflectionY, ReflectionBoth, Translations, RectanglePerimeter, RectangleArea, TriangleArea, ParallelogramArea, TrapeziumArea, MetricConversions, SurfaceAreaofCuboid, SurfaceAreaofSphere, VolofCuboid, AreaofCircle, PerimeterofCircle, AreaofSector, AnglesinParallelLines, AnglesinTriangle, Bearings, Pythagoras, Enlargement, SimpleVectors, HarderVectors, CircleTheorems, SinCosTan, ExactTrigValues, SinRule, CosineRule, HalfabSinc, ThreeDPythagoras]

            choice = r.choice(choosable_questions)

            choice()
        
        ChoosingQuestion()

    def Probability(self):
        self.page_clearer(self)


        def CalculatingProbability(): # self, QuestionText, Answer, Notes, grade, topic_id, **kwargs --> font_size, shape = 
            red = r.randint(1,15)
            blue = r.randint(2,18)
            total = blue + red

            QuestionText = f"There are {red} red and {blue} blue counters in a bag. \nFind the probability of taking 2 blue counters out without replacement."
            Notes = "Give your answer to 2 d.p"
            Answer = ((blue / total) * ((blue - 1) / (total - 1))) # calculating conditional probability
            Answer_2dp = f"{Answer:.2f}"

            self.QuestionCreator(QuestionText, Answer_2dp, Notes, 6, 4, font_size = 15)



        def MutualExclusivity():
            perc1 = r.randint(1, 10)  # Probability of A
            perc2 = r.randint(1, 10)  # Probability of B

            # mutually exclusive, add  probabilities


            QuestionText = f"The probability of A is {perc1}% and the probability of B is {perc2}%. \nA and B are mutually exclusive. Find the probability A OR B"
            Notes = "Give your answer as a decimal to 2 d.p"
            Answer = perc1 / 100 + perc2 / 100 # sum of mutually exclusive events
            Answer_2dp = f"{Answer:.2f}" # to 2 d.p

            self.QuestionCreator(QuestionText, Answer_2dp, Notes, 5, 4, font_size=15) # passing parameters



        def PieCharts():
            angle = r.randint(1,360) # some proportion of the pie chart
            people = r.randint(20,40) # no of students

            QuestionText = f"In a class, there are {people} students. \nThe proportion of boys and girls are placed on a pie chart. \nBoys take up {angle} degrees. \nHow many girls are there?" # question
            Notes = "" # no notes needed
            Answer = round(((360-angle)/360) * people) # calculating the answer.

            self.QuestionCreator(QuestionText, Answer, Notes, 7, 4, font_size = 15, shape = "circle") # parameters




        def ChoosingQuestion(): # function which chooses a question to be output randomly.
        
            choosable_questions = [CalculatingProbability, MutualExclusivity, PieCharts]

            
            choice = r.choice(choosable_questions)

            choice()
        
        ChoosingQuestion()


    def Statistics(self):

        self.page_clearer(self)


        def Mean():
            values_list = []

            for i in range(0,5):
                values_list.append(r.randint(1,100)) # adding random values to the list

            mean = sum(values_list) / 5 # finding the mean
                
            QuestionText = f"Find the mean of  {values_list}" # question
            Notes = "Round your answer to 2 d.p" # format to answer
            Answer = f"{mean:.2f}" # rounding to 2 d.p
                
            self.QuestionCreator(QuestionText, Answer, Notes, 2, 5) # parameters sent


        def Median():
            values_list = []
            
            for i in range(0,5):
                values_list.append(r.randint(1,100)) # adding random values to the list

            sorted_list = self.Quicksort(values_list) # sorting the values using the quicksort
            median = sorted_list[2] # middle of the sorted list

            QuestionText = f"Find the median of  {values_list}" # question
            Notes = "" # no format needed
            Answer = f"{median}" 

            self.QuestionCreator(QuestionText, Answer, Notes, 2, 5)

        def Mode():
            values_list = []

            for i in range (0,5):
                values_list.append(r.randint(1,100)) # adding to list

            values_list.append(r.choice(values_list)) # duplicating a value and adding it to the end of the list for a mode value

            QuestionText = f"Find the mode of {values_list}"
            Answer = values_list[5] # the repeated value will be at the end
            Notes = ""
            
            self.QuestionCreator(QuestionText, Answer, Notes, 1, 5)


        def Range():
            values_list = []
            
            for i in range(0,5):
                values_list.append(r.randint(1,100)) # adding random values to the list

            sorted_list = self.Quicksort(values_list) # sorting the values using the quicksort

            QuestionText = f"Find the range of {values_list}" # question
            Answer = (sorted_list[4] - sorted_list[0]) # diff between largest and smallest val. in sorted list
            Notes = ""

            self.QuestionCreator(QuestionText, Answer, Notes, 1, 5) # parameters


            

        def ChoosingQuestion(): # function which chooses a question to be output randomly.
            choosable_questions = [Mean, Median, Mode, Range]


            choice = r.choice(choosable_questions)

            choice()
        
        ChoosingQuestion()




class Teacher:
    def __init__(self, window, cursor, username):
        self.username = username
        self.cursor = cursor
        self.window = window


        teacher_id_query = "SELECT TeacherID FROM Teachers WHERE Username = ?" # getting the teacher ID using the given username
        cursor.execute(teacher_id_query, (self.username,))


        self.teacher_id = cursor.fetchone()[0] # taking the first variable as tuples are given

        teachers_class_query = "SELECT ClassID FROM Class WHERE TeacherID = ?" # query to get the ClassIDs of all the classes a teacher has
        cursor.execute(teachers_class_query, (self.teacher_id,))
        self.teachers_classes_id = cursor.fetchall() # all stored in a tuple here.

   
        self.page_clearer()

        self.home_page()



    def page_clearer(self):
        for widget in self.window.winfo_children():
            widget.destroy()



    def leaderboard(self, class_id):
        self.page_clearer()  # Empties the window

        ViewStudentsStatement = "SELECT StudentID, FirstName, Username FROM Students WHERE ClassID = ?" # retrieves the necessary information from table
        self.cursor.execute(ViewStudentsStatement, (class_id,)) 
        students_info = self.cursor.fetchall()

        treeview_data = []  # holding all data for the leaderboard

        for student in students_info: # iterating over all the students within the set class
            student_id = student[0] # since it is a tuple: [StudentID, FirstName, Username]
            first_name = student[1]
            username = student[2]

            # Getting the number of correct answers for the specified student
            self.cursor.execute("SELECT COUNT(*) FROM Result WHERE StudentID = ? AND Correct = 1", (student_id,)) # condition for when they are correct, counting ther number of rows
            correct_count = self.cursor.fetchone()[0] # first value as tuple

            # Getting the total number of answers from specified student
            self.cursor.execute("SELECT COUNT(*) FROM Result WHERE StudentID = ?", (student_id,)) # no condition to find the number of questions done
            total_count = self.cursor.fetchone()[0] # fetching the first value as tuple

            if total_count > 0:  # Preventing division by zero
                percentage_correct = ((correct_count / total_count) * 100)  # Percentage correct calculation
            else:
                percentage_correct = 0

            treeview_data.append((first_name, username, correct_count, total_count, f"{percentage_correct:.2f}%")) # adding all the data that was just calculated/selected


        # configuring treeview
        student_tree = ttk.Treeview(self.window, columns=("FirstName", "Username", "Correct", "Total", "Percentage Correct"), style="Custom.Treeview", show="headings")

        student_tree.heading("FirstName", text="FirstName") # all the headings 
        student_tree.heading("Username", text="Username")
        student_tree.heading("Correct", text="Correct")
        student_tree.heading("Total", text="Total")
        student_tree.heading("Percentage Correct", text="Percentage Correct")

        student_tree.column("FirstName", width=150) # setting the width of the columns
        student_tree.column("Username", width=150)
        student_tree.column("Correct", width=100)
        student_tree.column("Total", width=100)
        student_tree.column("Percentage Correct", width=150)

        # Inserting data
        for row in treeview_data:
            student_tree.insert("", tk.END, values=row) # adding into the tree

        student_tree.pack(fill=tk.BOTH, expand=True) # filling up the screen

        # go back to home_screen
        back_button = ctk.CTkButton(self.window, text="Back", command=self.home_page, fg_color="#4169E1")
        back_button.pack(padx=10, pady=15)



    def ModifyClass(self):  # function which allows the Teacher to modify any classes they have

        self.page_clearer()

        new_class = ctk.CTkFrame(self.window)  # frame which contains the widgets
        new_class.pack(padx=20, pady=20, fill="both", expand=True)  # padding and expands

        title_text = ctk.CTkLabel(new_class, text="Welcome to Class Modification", font=("Calibri", 32, "bold"))  # setting title
        title_text.pack(padx=0.03 * screen_width, pady=0.05 * screen_height)  # Added more top padding 

    

        # Class name entry field
        classname_label = ctk.CTkLabel(new_class, text="Enter Class Name:", font=("Arial", 16))
        classname_label.pack(pady=(0.01 * screen_height, 0.005 * screen_height))  

        classname_entry = ctk.CTkEntry(new_class, width=0.15 * screen_width, font=("Arial", 14))  # Added width 
        classname_entry.pack(pady=(0, 0.01 * screen_height))  

        def Modification(option):  # function which changes the database according to the button pressed
            if classname_entry.get() == "":
                messagebox.showinfo("No data entered", "Please enter a class name")

            elif len(classname_entry.get()) > 15:
                messagebox.showinfo("Too long", "Class must be shorter than 16 characters")

            else:
                if option == "create":
                    messagebox.showinfo("New Class", "A new class has been created! Re login for it to take effect.")
                    self.cursor.execute("INSERT INTO Class (TeacherID, ClassName) VALUES (?, ?)", (self.teacher_id, classname_entry.get()))
                    conn.commit()

                elif option == "destroy":
                    self.cursor.execute("DELETE FROM Class WHERE ClassName = ?", (classname_entry.get(),))
                    conn.commit()

        # Create and delete buttons aligned horizontally
        button_frame = ctk.CTkFrame(new_class)
        button_frame.pack()

        # warning telling teacher to relogin for Class creation to show up
        relogname_label = ctk.CTkLabel(new_class, text="Relogin for class creation to take effect", font=("Arial", 16))
        relogname_label.pack(pady=(0.01 * screen_height, 0.005 * screen_height))  

        # button creating class with classname from entry box
        createbutton = ctk.CTkButton(button_frame, text="Create New Class", width=0.03 * screen_width, command=lambda: Modification("create"))
        createbutton.grid(row=0, column=0, padx=0.01 * screen_width)  # aligning

        # button destroying class with classname from entry box
        deletebutton = ctk.CTkButton(button_frame, text="Delete Existing Class", width=0.03 * screen_width, command=lambda: Modification("destroy"))
        deletebutton.grid(row=0, column=1, padx=0.01 * screen_width)

        # button leading back to the teacher home page
        back_button = ctk.CTkButton(new_class, text="Back",fg_color="#4169E1", width=150, command=lambda: self.home_page())
        back_button.pack(pady=10)  # Added space below the buttons

        # calling all the class names and associated classIDs
        self.cursor.execute("SELECT ClassID, ClassName FROM Class WHERE TeacherID = ?", (self.teacher_id,))
        class_data = self.cursor.fetchall()

        # Creating the Treeview for displaying class data
        classesTree = ttk.Treeview(new_class, columns=("ClassID", "ClassName"), show="headings")
        classesTree.heading("ClassID", text="Class ID")
        classesTree.heading("ClassName", text="Class Name")

        classesTree.column("ClassID", width=int(0.05 * screen_width), anchor="center")  # Centering text
        classesTree.column("ClassName", width=int(0.1 * screen_width), anchor="center")  # Centering text

        # inputting the data extracted from the database
        for class_ in class_data:
            classesTree.insert("", "end", values=class_)

        classesTree.pack(pady=0.005 * screen_height, padx= 0.005 * screen_width, fill="both", expand=True)  # expands



    


    def ClassInformation(self, class_id):
        
        # getting the information for all students in the specified class
        student_query = "SELECT StudentID, FirstName, LastName FROM Students WHERE ClassID = ?" 
        self.cursor.execute(student_query, (class_id,))
        students = self.cursor.fetchall()

        names_list = [] # list of names
        correct_list = [] # list of correct answers for eachs tudent
        total_list = [] # total questions answered by each student
        percentage_list = [] # percentage of questions correct per student

        for student_id, first_name, last_name in students: # iterating through the above
            full_name = f"{first_name} {last_name[0]}" # first name + first letter of last

            correct_query = "SELECT COUNT(*) FROM Result WHERE StudentID = ? AND Correct = 1" # counts all correct answers
            self.cursor.execute(correct_query, (student_id,))
            count = self.cursor.fetchone()[0]

            total_query = "SELECT COUNT(*) FROM Result WHERE StudentID = ?" # counts total questions done
            self.cursor.execute(total_query, (student_id,))
            total = self.cursor.fetchone()[0]

            names_list.append(full_name) # adding to lists
            correct_list.append(count)
            total_list.append(total)

            if total > 0:
                percentage_list.append((count / total) * 100)
            else:
                percentage_list.append(0) # preventing division by 0 / run-time error



        second_frame = ctk.CTkFrame(self.window)
        second_frame.pack()

        correct_graph = ctk.CTkCanvas(second_frame) #graph showing the correct questions answered per student
        self.graph_maker(correct_graph, names_list, correct_list, "Correct Questions Answered Per Student")
        correct_graph.pack(side = "left")


        total_graph = ctk.CTkCanvas(second_frame) # graph showing the total no. of questions answered per student
        self.graph_maker(total_graph, names_list, total_list, "Total Questions Answered per Student")
        total_graph.pack(side = "left")

        percentage_graph = ctk.CTkCanvas(second_frame) # graph showing percentage correct per topic per student.
        self.graph_maker(percentage_graph, names_list, percentage_list, "Percentage Correct per Student")
        percentage_graph.pack(side = "left")


        button_frame = ctk.CTkFrame(self.window)


        back_button = ctk.CTkButton(button_frame, text="Back",fg_color="#4169E1", command = lambda: [self.window.destroy(), StartCode()]) # goes back to login page
        back_button.pack(side="left", padx=10, pady=15)

        ViewStudentsButton = ctk.CTkButton(button_frame, text = "View Students", command = lambda: self.ViewStudentsPage(class_id)) # views all information about students
        ViewStudentsButton.pack(padx=10, pady=15, side = "left")

        Viewleaderboard_button = ctk.CTkButton(button_frame, text = "Leaderboard", command = lambda: self.leaderboard(class_id)) # button which calls the leaderboard function
        Viewleaderboard_button.pack(side = "left" ,padx=10, pady=15)        

        # Button which leads to the modify class page
        CreateClassButton = ctk.CTkButton(button_frame, text = "Modify Class", command = lambda: self.ModifyClass())
        CreateClassButton.pack(padx = 10, pady = 15, side = "left")

        ChangeDetailsButton = ctk.CTkButton(button_frame, text = "Change Details", command = lambda: self.Change_Details())
        ChangeDetailsButton.pack(padx = 10, pady = 15, side = "left")

        button_frame.pack(side = "top", padx=10, pady=15)



    def graph_maker(self, graph, x_values, y_values, Title): # add x and y values from database as parameters


        facecolor_var = "white" # setting to a variable to allow customization


        Fig = Figure(figsize = (4,3.5), dpi = 100, facecolor = facecolor_var) # making the object Figure where the graph will be placed
        axis = Fig.add_subplot(111) # making the axis. Setting 1 row, 1 column, and adding 1 subplot




       # bar_color = "" # setting to a variable so it can be adjusted later


        axis.bar(x_values, y_values) # using a bar chart and plotting the x and ys.
        axis.set_facecolor(facecolor_var)
        axis.tick_params(axis='x', rotation=15, labelsize = 9) # adjusting these values to get the words to fit on the axis
        axis.set_title(Title) # setting a title for the graph




        canvas = FigureCanvasTkAgg(Fig, master=graph) # making the canvas where the graph will go
        canvas.draw() # drawing the graph
        canvas.get_tk_widget().pack(side="left", padx=3) # packing the graph itself


    def home_page(self):
        self.page_clearer()
        

        self.window.title(f"Welcome {self.username}") # setting the title


        teacher_name = '''
        SELECT FirstName, LastName FROM Teachers WHERE Username = ?
'''
       
        self.cursor.execute(teacher_name, (self.username,))


        result = self.cursor.fetchone() # placing the teacher's full name into a variable to add to the label.



        mainframe = ctk.CTkFrame(self.window) # creating the frame where the buttons, labels, and graphs will be placed
        mainframe.pack(pady = 5)



        welcome = ctk.CTkLabel(mainframe, text=f"Welcome, {result[0]} {result[1]}", font = ("Times", 40, 'bold'), text_color="blue") # setting a label which welcomes the user. result 0 is first naem result 1 is lastname
        welcome.pack(pady = 30, padx = 15) 

        side_frame = ctk.CTkFrame(self.window)
        side_frame.pack()


        def CallGraphs(class_id): # function  which calls the graph maker 
            all_data = self.ClassInformation(class_id)
            

        class_array = []

        for i in range(len(self.teachers_classes_id)):  # iterating through all classes
            class_id = self.teachers_classes_id[i][0]  # class ID for the current button

            classname_q = "SELECT ClassName FROM Class WHERE ClassID = ?" # getting the classname from the associated classID
            self.cursor.execute(classname_q, (class_id,)) 
            result = self.cursor.fetchone()
            
            if result is None:
                print (f"No class found for class with classID {class_id}")

            else:
                Class_name = result[0]
            
                # Create a button for each class
                button = ctk.CTkButton(
                    side_frame, 
                    text=f"Class {Class_name}", 
                    command=lambda id=class_id: [self.home_page(), CallGraphs(id)],  # Use lambda for current class_id otherwise problems with not retaining the correct id
                    width=0.02 * screen_width, 
                    height=0.02 * screen_height
                )
                button.pack(padx=0.005 * screen_width, pady=0.005 * screen_height, side = "left")
                class_array.append(button)






    def ViewStudentsPage(self, classid):

        self.page_clearer() # empties the window


        ViewStudentsStatement = "SELECT * FROM Students WHERE ClassID = ?" # SQL statement retrieving all information about the students in the specified class
        self.cursor.execute(ViewStudentsStatement, (classid,))  # Executes the SQL query with the provided class ID

        viewinformation = self.cursor.fetchall()


        table_frame = ctk.CTkScrollableFrame(self.window, width = 1200) # creating a scrollable frame for the table to go into 


        student_tree = ttk.Treeview(table_frame, columns=("StudentID", "ClassID", "FirstName", "LastName", "DoB", "Username", "Password"), show="headings") # defining the tree

    
        student_tree.heading("StudentID", text="StudentID") # creating the rows and columns for the tree. COULD BE MADE MORE EFFICIENT USING LOOP
        student_tree.heading("ClassID", text="ClassID")
        student_tree.heading("FirstName", text="FirstName")
        student_tree.heading("LastName", text="LastName")
        student_tree.heading("DoB", text="DoB")
        student_tree.heading("Username", text="Username")
        student_tree.heading("Password", text="Password")
    
        student_tree.column("StudentID")
        student_tree.column("ClassID")
        student_tree.column("FirstName")
        student_tree.column("LastName")
        student_tree.column("DoB")
        student_tree.column("Username")
        student_tree.column("Password")

        for row in viewinformation:
            student_tree.insert("", tk.END, values = row) # inputting values into the tree



        student_tree.pack(fill = tk.BOTH) 

        table_frame.pack(side = "top", pady = 15, padx = 20)

        back_button = ctk.CTkButton(self.window, text = "Back", command = self.home_page, fg_color="#4169E1") #
        back_button.pack(padx = 10, pady = 15) # creating a back button to go to the homepage





    def StudentGraphs(self):
        self.page_clearer(self.window)

        back_button = ctk.CTkButton(self.window, text = "Back", command = self.home_page, fg_color="#4169E1") #
        back_button.pack(padx = 10, pady = 15) # creating a back button to go to the homepage


    def Change_Details(self): # function which allows the user to change their details
        self.page_clearer()


        # frame to store widgets
        mainframe = ctk.CTkFrame(self.window) 
        mainframe.pack(pady = 0.1 * screen_height)

        # # Comboxbox which shows all available classes
        # class_names = [] # list which will contain all class names
        # cursor.execute("SELECT ClassName FROM Class") 
        # c = cursor.fetchall() # getting all the classnames

        # for row in c:
        #     class_names.append(row[0]) # appending to end of lsit

        title_text = ctk.CTkLabel(mainframe, text="Welcome to Change Details!", font=("Calibri", 32, "bold")) # setting title
        title_text.grid(row = 0, column = 0, columnspan = 3, padx = 0.02 * screen_width, pady = 0.02 * screen_height)


        # Password and Re-entry Password
        self.passw_enter = ctk.CTkEntry(mainframe ,  width=200,  placeholder_text = "Current password", show = "*")
        self.passw_enter.grid(row=1, column=1, padx = 10 ,pady = 10, sticky = "ew", columnspan = 2) # sticky goes ew, meaning east west expansion for when the window is expanded.#
    
        # entering the new password
        self.newpass_enter = ctk.CTkEntry(mainframe ,  width=200, placeholder_text = "New Password" , show = "*")
        self.newpass_enter.grid(row=3, column=1, padx = 10 ,pady = 10, sticky = "ew") # sticky goes ew, meaning east west expansion for when the window is expanded.

        # re entering the new password
        self.renewpass_enter = ctk.CTkEntry(mainframe ,  width=200, placeholder_text = "Re-enter" , show = "*")
        self.renewpass_enter.grid(row=3, column=2, padx = 10 ,pady = 10, sticky = "ew") # sticky goes ew, meaning east west expansion for when the window is expanded.

        self.ShowPasswords = ctk.CTkCheckBox(
            mainframe, 
            text="Show Passwords", 
            command=lambda: [
                self.newpass_enter.configure(show="" if self.newpass_enter.cget("show") == "*" else "*"),
                self.renewpass_enter.configure(show="" if self.renewpass_enter.cget("show") == "*" else "*")
            ]
        )
        self.ShowPasswords.grid(row=4, columnspan=4, pady=10)

        # buttong to update details
        update_button = ctk.CTkButton(mainframe, text="Update Details", command=self.update_details)
        update_button.grid(row=5, column=2, pady=10)

        # button to go back to the home page
        back_button = ctk.CTkButton(mainframe, text = "Back", command = self.home_page, fg_color="#4169E1")
        back_button.grid(row = 5, column = 1, pady=10)


    def update_details(self): # function which makes the database changes and verifies everything
        old_password = self.passw_enter.get() # getting the password input
        new_password = self.newpass_enter.get() # getting the new password input
        reenter_password = self.renewpass_enter.get() # getting the re entry input


        # current password from database
        self.cursor.execute("SELECT Password FROM Teachers WHERE TeacherID = ?", (self.teacher_id,))
        result = self.cursor.fetchone()
        current_password = result[0] # changing from tuple to the password itself


        con = True
        # Check if the old password is correct
        if old_password != current_password:
            self.passw_enter.configure(fg_color="#f8d7da")
            self.passw_enter.configure(placeholder_text = "The old password is incorrect.")
            messagebox.showinfo("Error", "The password is incorrect")
            con = False


        # Check if the new passwords match
        if new_password != reenter_password:
            self.newpass_enter.configure(fg_color="#f8d7da")
            self.renewpass_enter.configure(fg_color="#f8d7da")
            self.newpass_enter.configure(placeholder_text = "Passwords do not match")
            self.renewpass_enter.configure(placeholder_text = "Passwords do not match")
            messagebox.showinfo("Error", "Passwords do not match")
            con = False

        print (len(new_password))
        if len(new_password) < 9:
            self.newpass_enter.configure(fg_color="#f8d7da")
            self.renewpass_enter.configure(fg_color="#f8d7da")
            self.newpass_enter.configure(placeholder_text = "Password must be > 8 characters long")
            self.renewpass_enter.configure(placeholder_text = "Password must be > 8 characters long")
            messagebox.showinfo("Error", "Password must be > 8 characters long")
            con = False

        # if continue is true after all the validation then update the password and class
        if con == True:
            self.cursor.execute("UPDATE Teachers SET Password = ? WHERE TeacherID = ?", (new_password, self.teacher_id))
            conn.commit()
            messagebox.showinfo("Change Complete", f"Password: {new_password}.")

def StartCode():
    app = AdjustMaths()
    app.run()


StartCode()




