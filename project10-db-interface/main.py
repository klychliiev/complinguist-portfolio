import tkinter as tk
from tkinter import ttk
import sqlite3

# Create the main window
window = tk.Tk()
window.title("Кличлієв Кирило, група №2, ЛР №2")

# Create a button
button = ttk.Button(window, text="Отримати парадигми")
button.grid(row=0, column=2, padx=10, pady=10)

# Create a label
label = ttk.Label(window, text="Sample Label")
label.grid(row=0, column=0, padx=10, pady=10)

# Create a combobox
combo_var = tk.StringVar()
combo = ttk.Combobox(window, textvariable=combo_var)
combo.grid(row=1, column=0, padx=10, pady=10, sticky='n')

# Create a treeview (table)
columns = ('ID', 'sgN', 'plL')
tree = ttk.Treeview(window, columns=columns, show='headings')
tree.grid(row=1, column=1, columnspan=3, padx=10, pady=10)

tree.heading("ID", text="ID")
tree.heading("sgN", text="sgN")
tree.heading("plL", text="plL")

# Connect to the SQLite database
DATABASE_PATH = "pol_lab07.s3db"
conn = sqlite3.connect(DATABASE_PATH)
cursor = conn.cursor()

# Function to execute the first SQL query
def get_sgn_word():
    query = "SELECT sgN FROM tnoun LIMIT 1"
    cursor.execute(query)
    result = cursor.fetchone()
    label.config(text=result[0])

get_sgn_word()

# Function to execute the second SQL query
def get_word_starting_with_g():
    query = "SELECT sgN FROM tnoun WHERE sgN LIKE 'g%' LIMIT 1"
    cursor.execute(query)
    result = cursor.fetchone()
    label.config(text=result[0])

get_word_starting_with_g()

# Function to fill the table with data
def fill_table():
    query = "SELECT id, sgN, plL FROM tnoun LIMIT 12"
    cursor.execute(query)
    data = cursor.fetchall()
    for i, row in enumerate(data, start=1):
        tree.insert('', tk.END, values=(i, row[1], row[2]))

button.config(command=fill_table)

# Function to fill the table with data and dashes
def fill_dashes():
    query = "SELECT id, sgN, plL FROM tnoun LIMIT 12"
    cursor.execute(query)
    data = cursor.fetchall()
    for i, row in enumerate(data, start=1):
        other_case = row[2] if row[2] else "-"
        tree.insert("", i, values=(i, row[1], other_case))

button.config(command=fill_dashes)

# Function to load words starting with 'g' into the combobox
def load_tnoun_to_combo():
    query = "SELECT sgN FROM tnoun WHERE sgN LIKE 'g%'"
    cursor.execute(query)
    tnoun = cursor.fetchall()
    combo['values'] = [word[0] for word in tnoun]

load_tnoun_to_combo()

# Start the main loop
window.mainloop()

# Close the database connection
conn.close()
