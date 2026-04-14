# About this Assignment
# This assignment is part of the module on database fundamentals and basic data management in Python; and it reflects the kind of foundational programming work that many real-world applications require.

# It is designed to give you hands-on experience with implementing Create, Read, Update, and Delete (CRUD) operations using a local SQLite database. 
# Through this task, you'll strengthen your understanding of how databases are integrated into software applications and how Python can be used to manage persistent data storage.

# By completing this assignment, you will practice:

# Setting up and connecting to a local SQLite database
# Designing and managing a data table
# Writing Python functions that perform core database operations
# Creating a simple command-line interface for user interaction
# Ensuring your application handles errors and invalid inputs effectively
# Course Learning Outcomes
# The following course learning outcomes are assessed in this assignment:

# Create Python code that interacts with databases
# Use libraries and packages for a Python project
# Related Lessons
# Basic CRUD application in Python
# Practical Application in Python: Using Loops
# SQLite Databases: Definition, Tools & Commands
# Defining & Calling a Function in Python
# Function Arguments in Python: Definition & Examples
# Data Validation & Exception Handling in Python
# Prompt
# In this assignment, you will create a Python program that allows a user to manage student records stored in an SQLite database. You'll design a menu-driven, command-line application that supports all basic CRUD operations. This assignment focuses on modular design and robust error handling, helping you build clean, maintainable code that interacts smoothly with a persistent data layer.

# Your program should:

# 1) Connect to an SQLite database file. If the database does not already exist, your program should create it.

# 2) Define and create a table named students with the following columns: id (INTEGER, primary key), name (TEXT), grade (TEXT), and email (TEXT).

# 3) Provide a simple text-based menu that allows the user to:

# Add a new student record
# View all existing student records
# Update an existing student's information
# Delete a student record
# Exit the program
# 4) Implement each database operation in a separate Python function for clarity and reusability.

# 5) Validate user inputs (e.g., ensure email contains an '@' symbol, ID is an integer, prompt user for confirmation before deleting a record).

# 6) Use try-except blocks to handle possible runtime errors such as failed database operations or invalid user input.

# 7) Ensure all changes are saved persistently in the .db file so that records are retained between sessions.

import sqlite3
from tabulate import tabulate
import re

def create_student_table (): 
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            grade INTEGER NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    print('Student data table was created successfully!')
    

def add_student ():
    # each student will have a full name, fn, ln, email, studentid,
    fullName = input("Enter the new students full name\n")
    if re.match(r'^[a-zA-Z]+\s+[a-zA-Z]+$', fullName):
        firstName, lastName = fullName.split()
    else:
        print("Please enter exactly two names")
        return
    email = f"{firstName}.{lastName}@uni.edu"
    studentID = generate_student_id()
    
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    grade = input("Enter student's grade(1-4)\n")
    
    if not re.match(r'^[1-4]$', grade):
        print("invalid grade, must be 1-4")
        return
    try: 
        cursor.execute(''' 
                       INSERT INTO students
                       VALUES(?, ?, ?, ?, ?, ?)
                       ''', 
                       (studentID, fullName, firstName, lastName, grade, email ))
        conn.commit()
        print('Student was added!')
    except  sqlite3.IntegrityError as e:
        print(f"Error adding student: {e}")
    finally: 
        conn.close()
        view_all_students()

        
def generate_student_id ():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute('SELECT student_id FROM students ORDER BY student_id DESC LIMIT 1')
    result = cursor.fetchone()

    if result is None: 
        return "STU001"
    else: 
        last_id = result[0]
        number = int(last_id[3:])
        return f"STU{number + 1:03d}"


def view_all_students():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students ORDER BY student_id DESC')
    students = cursor.fetchall()
    # print(f"ID FN LN EMAIL")
    headers = ["ID", "Full Name", "First name", "Last name", "Grade", "Email"]
    print(f"\n{tabulate(students, headers=headers, tablefmt='grid')}")
    conn.close()

def update_student ():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    student_id = input("Enter student id's information you would like to update\n")
    cursor.execute('SELECT * FROM students WHERE student_id = ?', (student_id,))
    result = cursor.fetchone()
    if result is None:
        print(f"Student with {student_id} does not exist")
        conn.close()
        return 
    else:
        print(f"Lets update this {student_id} student's information")
        info_update = input('What information would you like to update (name, grade, email)?\n')
        if info_update == "name":
            new_value = input('Enter updated full name\n')
            if re.match(r'^[a-zA-Z\s]+$', new_value):
                name_parts = new_value.split(' ')
                if len(name_parts) >= 2:
                    cursor.execute("UPDATE students SET name = ? WHERE student_id = ? ", (new_value, student_id))
                    cursor.execute("UPDATE students SET first_name = ?, last_name = ? WHERE student_id = ?", (name_parts[0], name_parts[1], student_id))
                    conn.commit()
                    conn.close()
                    view_all_students()
                else:
                    print("Name must include first and last name")
                    conn.close()
                    return
            else:
                print("Invalid name input, please make you are only using alphabetical letters")
                conn.close()
                view_all_students()
                return
        elif info_update == "grade":
           new_value = input('Enter updated grade\n')
           if re.match(r'^[1-4]$', new_value):
            cursor.execute("UPDATE students SET grade = ? WHERE student_id = ? ", (new_value, student_id))
            conn.commit()
            conn.close()
            view_all_students()
           else:
               print("Invalid grade input. Please enter 1-4")
               conn.close()
               view_all_students()
               return
        elif info_update == "email":
            new_value = input('Enter updated email\n')
            if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', new_value):
                cursor.execute("UPDATE students SET email = ? WHERE student_id = ? ", (new_value, student_id))
                conn.commit()
                conn.close()
                view_all_students()
            else:
               print("Invalid email input. Please make sure email has @")
               conn.close()
               view_all_students()
               return
        else:
            print("Invalid option: Choose name, or email")
            conn.close()
            view_all_students()
            return
    print(f"Student {student_id} was updated")
    

def delete_student ():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    student_id = input("Enter the student's id that you would like to delete\n")
    cursor.execute('SELECT name FROM students WHERE student_id = ?', (student_id,)) 
    result = cursor.fetchone()
    if result is None:
        print("Student does not exists")
        conn.close()
        return
    else: 
        confirm_input = input(f"Confirm you would like to DELETE (yes/no) {student_id}\n")
        if confirm_input == "yes":
            cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
            conn.commit()
            conn.close()
            print(f"Student {student_id} was DELETED succesfully!")
        else: 
            print("Deletion cancelled")
            conn.close()
            return
   
    view_all_students()

    

def main_prompt(): 
    while True: 
        op = input("What would like to do: (add/delete/update/view all/exit) student records\n").lower().strip()
        if op == "add": 
            add_student()
        elif op == "delete":
            delete_student()
        elif op == "update": 
            update_student()
        elif op == "view all":
            view_all_students()
        elif op == "exit":
            break
        else:
            print("Invalid input command! Please use: add, delete, update, or quit\n") 

def main ():
    try: 
        with sqlite3.connect("students.db") as conn:
            print(f"Opened SQLite database with version {sqlite3.sqlite_version} successfully.")
        create_student_table()
        main_prompt()
        view_all_students()

    except sqlite3.OperationalError as e:
        print("Failed to open database, create one:", e)

        
main()