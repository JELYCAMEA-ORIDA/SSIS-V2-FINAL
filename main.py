import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Create a connection to the database
conn = sqlite3.connect("SSISv2.db")
cursor = conn.cursor()

# Create the Students table if it doesn't exist
cursor.execute("""CREATE TABLE IF NOT EXISTS Students (
                    ID TEXT PRIMARY KEY,
                    Name TEXT,
                    Gender TEXT,
                    YearLevel INTEGER,
                    CourseCode TEXT)""")

# Create the Courses table if it doesn't exist
cursor.execute("""CREATE TABLE IF NOT EXISTS Courses (
                    Code TEXT PRIMARY KEY,
                    Name TEXT)""")

# Create the main window
window = tk.Tk()
window.title("SSIS")
window.geometry("800x600")

# Create the tab control
tab_control = ttk.Notebook(window)

# Create the Student tab
student_tab = ttk.Frame(tab_control)
tab_control.add(student_tab, text="STUDENT DATA")

# Create the Course tab
course_tab = ttk.Frame(tab_control)
tab_control.add(course_tab, text="COURSE DATA")

tab_control.pack(expand=True, fill="both")

# Create a table to display the student records
student_table = ttk.Treeview(student_tab, columns=("ID", "Name", "Gender", "Year Level", "Course Code"),
                             show="headings")

student_table.heading("ID", text="ID")
student_table.heading("Name", text="Name")
student_table.heading("Gender", text="Gender")
student_table.heading("Year Level", text="Year Level")
student_table.heading("Course Code", text="Course Code")

student_table.pack(fill="both", expand=True)

# Create a table to display the course records
course_table = ttk.Treeview(course_tab, columns=("Code", "Name"), show="headings")

course_table.heading("Code", text="Code")
course_table.heading("Name", text="Name")

course_table.pack(fill="both", expand=True)


def add_record():
    selected_tab = tab_control.index(tab_control.select())

    if selected_tab == 0:  # Student tab is selected
        # Create a new window for entering student details
        add_window = tk.Toplevel(window)
        add_window.title("Add Student")
        add_window.geometry("400x300")

        # Create labels and entry fields for student details
        id_label = ttk.Label(add_window, text="ID Number:", font=("Arial", 13))
        id_label.pack()
        id_entry = ttk.Entry(add_window, font=("Arial", 13))
        id_entry.pack()

        name_label = ttk.Label(add_window, text="Name:", font=("Arial", 13))
        name_label.pack()
        name_entry = ttk.Entry(add_window, font=("Arial", 13))
        name_entry.pack()

        gender_label = ttk.Label(add_window, text="Gender:", font=("Arial", 13))
        gender_label.pack()
        gender_combobox = ttk.Combobox(add_window, values=["Female", "Male"], font=("Arial", 11))
        gender_combobox.pack()

        year_label = ttk.Label(add_window, text="Year Level:", font=("Arial", 13))
        year_label.pack()
        year_entry = ttk.Entry(add_window, font=("Arial", 13))
        year_entry.pack()

        course_label = ttk.Label(add_window, text="Course Code:", font=("Arial", 13))
        course_label.pack()

        # Get the course codes from the database
        cursor.execute("SELECT Code FROM Courses")
        course_codes = [row[0] for row in cursor.fetchall()]

        course_combobox = ttk.Combobox(add_window, values=course_codes, font=("Arial", 11))
        course_combobox.pack()

        # Function to handle the "Save" button command for adding a student
        def save_record():
            # Get the entered values
            id_number = id_entry.get()
            name = name_entry.get()
            gender = gender_combobox.get()
            year_level = year_entry.get()
            course_code = course_combobox.get()

            # Insert the student record into the database
            cursor.execute("INSERT INTO Students VALUES (?, ?, ?, ?, ?)",
                           (id_number, name, gender, year_level, course_code))
            conn.commit()

            # Insert the student record into the table
            student_table.insert("", tk.END, values=(id_number, name, gender, year_level, course_code))

            # Close the add window
            add_window.destroy()

        # Create a button to save the student record
        save_button = ttk.Button(add_window, text="Save", command=save_record, style="Larger.TButton")
        save_button.pack(pady=10)

    elif selected_tab == 1:  # Course tab is selected
        # Create a new window for entering course details
        add_window = tk.Toplevel(window)
        add_window.title("Add Course")
        add_window.geometry("400x200")

        # Create labels and entry fields for course details
        code_label = ttk.Label(add_window, text="Code:", font=("Arial", 13))
        code_label.pack()
        code_entry = ttk.Entry(add_window, font=("Arial", 13))
        code_entry.pack()

        name_label = ttk.Label(add_window, text="Name:", font=("Arial", 13))
        name_label.pack()
        name_entry = ttk.Entry(add_window, font=("Arial", 13))
        name_entry.pack()

        # Function to handle the "Save" button command for adding a course
        def save_record():
            # Get the entered values
            code = code_entry.get()
            name = name_entry.get()

            # Check if the code already exists in the database
            cursor.execute("SELECT * FROM Courses WHERE Code = ?", (code,))
            existing_course = cursor.fetchone()

            if existing_course:
                messagebox.showerror("Error", "Course with the given code already exists.")
                return

            # Insert the course record into the database
            cursor.execute("INSERT INTO Courses VALUES (?, ?)", (code, name))
            conn.commit()

            # Insert the course record into the table
            course_table.insert("", tk.END, values=(code, name))

            # Close the add window
            add_window.destroy()

        # Create a button to save the course record
        save_button = ttk.Button(add_window, text="Save", command=save_record, style="Larger.TButton")
        save_button.pack(pady=10)

def search_record():
    selected_tab = tab_control.index(tab_control.select())

    if selected_tab == 0:  # Student tab is selected
        # Create a new window for searching student details
        search_window = tk.Toplevel(window)
        search_window.title("Search Student")
        search_window.geometry("400x200")

        # Create a label and entry field for searching student by ID
        id_label = ttk.Label(search_window, text="Enter ID Number:", font=("Arial", 13))
        id_label.pack()
        id_entry = ttk.Entry(search_window, font=("Arial", 13))
        id_entry.pack()

        # Function to handle the "Search" button command for searching a student
        def search_student():
            # Get the entered ID number
            id_number = id_entry.get()

            # Search for the student in the database
            cursor.execute("SELECT * FROM Students WHERE ID = ?", (id_number,))
            student = cursor.fetchone()

            if student:
                # Clear existing records in the table
                student_table.delete(*student_table.get_children())

                # Insert the student record into the table
                student_table.insert("", tk.END, values=student)
            else:
                # Student not found
                messagebox.showinfo("Student Not Found", "No student with the given ID number found.")

            # Close the search window
            search_window.destroy()

        # Create a button to search for a student
        search_button = ttk.Button(search_window, text="Search", command=search_student, style="Larger.TButton")
        search_button.pack(pady=10)

    elif selected_tab == 1:  # Course tab is selected
        # Create a new window for searching course details
        search_window = tk.Toplevel(window)
        search_window.title("Search Course")
        search_window.geometry("400x200")

        # Create a label and entry field for searching course by code
        code_label = ttk.Label(search_window, text="Enter Code:", font=("Arial", 13))
        code_label.pack()
        code_entry = ttk.Entry(search_window, font=("Arial", 13))
        code_entry.pack()

        # Function to handle the "Search" button command for searching a course
        def search_course():
            # Get the entered code
            code = code_entry.get()

            # Search for the course in the database
            cursor.execute("SELECT * FROM Courses WHERE Code = ?", (code,))
            course = cursor.fetchone()

            if course:
                # Clear existing records in the table
                course_table.delete(*course_table.get_children())

                # Insert the course record into the table
                course_table.insert("", tk.END, values=course)
            else:
                # Course not found
                messagebox.showinfo("Course Not Found", "No course with the given code found.")

            # Close the search window
            search_window.destroy()

        # Create a button to search for a course
        search_button = ttk.Button(search_window, text="Search", command=search_course, style="Larger.TButton")
        search_button.pack(pady=10)

def update_record():
    selected_tab = tab_control.index(tab_control.select())

    if selected_tab == 0:  # Student tab is selected
        # Get the selected student record
        selected_item = student_table.selection()
        if not selected_item:
            messagebox.showerror("Error", "No student record selected.")
            return

        # Get the values from the selected row
        id_number = student_table.item(selected_item, "values")[0]
        name = student_table.item(selected_item, "values")[1]
        gender = student_table.item(selected_item, "values")[2]
        year_level = student_table.item(selected_item, "values")[3]
        course_code = student_table.item(selected_item, "values")[4]

        # Create a new window for updating student details
        update_window = tk.Toplevel(window)
        update_window.title("Update Student")
        update_window.geometry("400x300")

        # Create labels and entry fields for student details
        id_label = ttk.Label(update_window, text="ID Number:", font=("Arial", 13))
        id_label.pack()
        id_entry = ttk.Entry(update_window, font=("Arial", 13))
        id_entry.insert(tk.END, id_number)  # Set the current ID number
        id_entry.configure(state="readonly")  # Disable editing
        id_entry.pack()

        name_label = ttk.Label(update_window, text="Name:", font=("Arial", 13))
        name_label.pack()
        name_entry = ttk.Entry(update_window, font=("Arial", 13))
        name_entry.insert(tk.END, name)  # Set the current name
        name_entry.pack()

        gender_label = ttk.Label(update_window, text="Gender:", font=("Arial", 13))
        gender_label.pack()
        gender_combobox = ttk.Combobox(update_window, values=["Female", "Male"], font=("Arial", 11))
        gender_combobox.set(gender)  # Set the current gender
        gender_combobox.pack()

        year_label = ttk.Label(update_window, text="Year Level:", font=("Arial", 13))
        year_label.pack()
        year_entry = ttk.Entry(update_window, font=("Arial", 13))
        year_entry.insert(tk.END, year_level)  # Set the current year level
        year_entry.pack()

        course_label = ttk.Label(update_window, text="Course Code:", font=("Arial", 13))
        course_label.pack()
        course_entry = ttk.Entry(update_window, font=("Arial", 13))
        course_entry.insert(tk.END, course_code)  # Set the current course code
        course_entry.pack()

        # Function to handle the "Update" button command for updating a student
        def update_student():
            # Get the entered values
            name = name_entry.get()
            gender = gender_combobox.get()
            year_level = year_entry.get()
            course_code = course_entry.get()

            # Update the student record in the database
            cursor.execute("UPDATE Students SET Name = ?, Gender = ?, YearLevel = ?, CourseCode = ? WHERE ID = ?",
                           (name, gender, year_level, course_code, id_number))
            conn.commit()

            # Update the student record in the table
            student_table.item(selected_item, values=(id_number, name, gender, year_level, course_code))

            # Close the update window
            update_window.destroy()

        # Create a button to update the student record
        update_button = ttk.Button(update_window, text="Update", command=update_student, style="Larger.TButton")
        update_button.pack(pady=10)

    elif selected_tab == 1:  # Course tab is selected
        # Get the selected course record
        selected_item = course_table.selection()
        if not selected_item:
            messagebox.showerror("Error", "No course record selected.")
            return

        # Get the values from the selected row
        code = course_table.item(selected_item, "values")[0]
        name = course_table.item(selected_item, "values")[1]

        # Create a new window for updating course details
        update_window = tk.Toplevel(window)
        update_window.title("Update Course")
        update_window.geometry("400x200")

        # Create labels and entry fields for course details
        code_label = ttk.Label(update_window, text="Code:", font=("Arial", 13))
        code_label.pack()
        code_entry = ttk.Entry(update_window, font=("Arial", 13))
        code_entry.insert(tk.END, code)  # Set the current code
        code_entry.configure(state="readonly")  # Disable editing
        code_entry.pack()

        name_label = ttk.Label(update_window, text="Name:", font=("Arial", 13))
        name_label.pack()
        name_entry = ttk.Entry(update_window, font=("Arial", 13))
        name_entry.insert(tk.END, name)  # Set the current name
        name_entry.pack()

        # Function to handle the "Update" button command for updating a course
        def update_course():
            # Get the entered values
            name = name_entry.get()

            # Update the course record in the database
            cursor.execute("UPDATE Courses SET Name = ? WHERE Code = ?", (name, code))
            conn.commit()

            # Update the course record in the table
            course_table.item(selected_item, values=(code, name))

            # Close the update window
            update_window.destroy()

        # Create a button to update the course record
        update_button = ttk.Button(update_window, text="Update", command=update_course, style="Larger.TButton")
        update_button.pack(pady=10)

def delete_record():
    selected_tab = tab_control.index(tab_control.select())

    if selected_tab == 0:  # Student tab is selected
        # Get the selected student record
        selected_item = student_table.selection()
        if not selected_item:
            messagebox.showerror("Error", "No student record selected.")
            return

        # Confirm the deletion
        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete the selected student?")
        if not confirm:
            return

        # Get the ID number of the selected student
        id_number = student_table.item(selected_item, "values")[0]

        # Delete the student record from the database
        cursor.execute("DELETE FROM Students WHERE ID = ?", (id_number,))
        conn.commit()

        # Delete the student record from the table
        student_table.delete(selected_item)

    elif selected_tab == 1:  # Course tab is selected
        # Get the selected course record
        selected_item = course_table.selection()
        if not selected_item:
            messagebox.showerror("Error", "No course record selected.")
            return

        # Confirm the deletion
        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete the selected course?")
        if not confirm:
            return

        # Get the code of the selected course
        code = course_table.item(selected_item, "values")[0]

        # Delete the course record from the database
        cursor.execute("DELETE FROM Courses WHERE Code = ?", (code,))
        conn.commit()

        # Delete the course record from the table
        course_table.delete(selected_item)

        # Delete the students with the same course code from the database
        cursor.execute("DELETE FROM Students WHERE CourseCode = ?", (code,))
        conn.commit()


def list_records():
    selected_tab = tab_control.index(tab_control.select())

    if selected_tab == 0:  # Student tab is selected
        # Clear the current student table
        student_table.delete(*student_table.get_children())

        # Fetch all student records from the database
        cursor.execute("SELECT * FROM Students")
        students = cursor.fetchall()

        # Insert the student records into the table
        for student in students:
            student_table.insert("", tk.END, values=student)

    elif selected_tab == 1:  # Course tab is selected
        # Clear the current course table
        course_table.delete(*course_table.get_children())

        # Fetch all course records from the database
        cursor.execute("SELECT * FROM Courses")
        courses = cursor.fetchall()

        # Insert the course records into the table
        for course in courses:
            course_table.insert("", tk.END, values=course)

# Create a frame to hold the buttons
buttons_frame = ttk.Frame(window)
buttons_frame.pack(side="top", pady=10)

# Create the CRUDL buttons
button_style = ttk.Style()
button_style.configure("Larger.TButton", font=("TkDefaultFont", 12), width=15)
button_width = 15

add_button = ttk.Button(buttons_frame, text="Add", command=add_record, style="Larger.TButton")
add_button.pack(side="left", padx=10)

search_button = ttk.Button(buttons_frame, text="Search", command=search_record, style="Larger.TButton")
search_button.pack(side="left", padx=10)

delete_button = ttk.Button(buttons_frame, text="Delete", command=delete_record, style="Larger.TButton")
delete_button.pack(side="left", padx=10)

update_button = ttk.Button(buttons_frame, text="Update", command=update_record, style="Larger.TButton")
update_button.pack(side="left", padx=10)

list_button = ttk.Button(buttons_frame, text="List", command=list_records, style="Larger.TButton")
list_button.pack(side="left", padx=10)

# Start the Tkinter event loop
window.mainloop()

# Close the database connection
conn.close()
