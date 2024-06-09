import tkinter as tk
from tkinter import ttk
import sqlite3
import webbrowser

# Create and populate the SQLite database
def create_database():
    conn = sqlite3.connect('swed-ukr.db')
    cur = conn.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS vocab
                (id INTEGER PRIMARY KEY,
                category TEXT,
                swedish_word TEXT,
                ukrainian_word TEXT)''')

    word_data = [
        (1, 'numbers', 'ett', 'один'),
        (2, 'food', 'äpple', 'яблуко'),
        (3, 'countries', 'Sverige', 'Швеція'),
        (4, 'colors', 'röd', 'червоний'),
        (5, 'animals', 'hund', 'собака'),
        (6, 'professions', 'läkare', 'лікар'),
        (7, 'weather', 'sol', 'сонце'),
        (8, 'transportation', 'bil', 'автомобіль'),
        (9, 'numbers', 'två', 'два'),
        (10, 'food', 'mjölk', 'молоко'),
        (11, 'countries', 'Norge', 'Норвегія'),
        (12, 'colors', 'blå', 'синій'),
        (13, 'animals', 'katt', 'кіт'),
        (14, 'professions', 'kock', 'кухар'),
        (15, 'weather', 'regn', 'дощ'),
        (16, 'transportation', 'cykel', 'велосипед'),
        (17, 'numbers', 'tre', 'три'),
        (18, 'food', 'bröd', 'хліб'),
        (19, 'countries', 'Ukraina', 'Україна'),
        (20, 'colors', 'gul', 'жовтий'),
        (21, 'animals', 'fågel', 'птах'),
        (22, 'professions', 'polis', 'поліцейський'),
        (23, 'weather', 'moln', 'хмара'),
        (24, 'transportation', 'buss', 'автобус'),
        (25, 'numbers', 'fyra', 'чотири'),
        (26, 'food', 'ost', 'сир'),
        (27, 'countries', 'Finland', 'Фінляндія'),
        (28, 'colors', 'vit', 'білий'),
        (29, 'animals', 'kanin', 'кролик'),
        (30, 'professions', 'ingenjör', 'інженер'),
        (31, 'weather', 'vind', 'вітер'),
        (32, 'transportation', 'tåg', 'потяг'),
        (33, 'numbers', 'fem', 'п’ять'),
        (34, 'food', 'köttbullar', 'котлети'),
        (35, 'countries', 'Danmark', 'Данія'),
        (36, 'colors', 'grön', 'зелений'),
        (37, 'animals', 'ko', 'корова'),
        (38, 'professions', 'lärare', 'вчитель'),
        (39, 'weather', 'snö', 'сніг'),
        (40, 'transportation', 'flygplan', 'літак'),
        (41, 'numbers', 'sex', 'шість'),
        (42, 'food', 'pasta', 'паста'),
        (43, 'countries', 'Spanien', 'Іспанія'),
        (44, 'colors', 'svart', 'чорний'),
        (45, 'animals', 'häst', 'кінь'),
        (46, 'professions', 'fotograf', 'фотограф'),
        (47, 'weather', 'regnjacka', 'плащ'),
        (48, 'transportation', 'motorcykel', 'мотоцикл'),
        (49, 'numbers', 'sju', 'сім'),
        (50, 'food', 'ris', 'рис')
    ]

    cur.executemany("INSERT INTO vocab VALUES(?,?,?,?)", word_data)
    conn.commit()
    conn.close()

# Fetch data from the database
def fetch_data():
    conn = sqlite3.connect('swed-ukr.db')
    cursor = conn.cursor()
    query = "SELECT * FROM vocab ORDER BY swedish_word COLLATE NOCASE"
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

# Clear the table
def clear_table():
    for i in tree.get_children():
        tree.delete(i)

# Fill the table with data
def fill_table(data):
    for idx, row in enumerate(data):
        tree.insert('', 'end', values=(idx + 1, row[1], row[2], row[3]))

# Handle combobox selection change
def on_combobox_change(event):
    selected_category = combo_box.get()
    clear_table()
    conn = sqlite3.connect('swed-ukr.db')
    cursor = conn.cursor()
    query = "SELECT * FROM vocab WHERE category = ? ORDER BY swedish_word COLLATE NOCASE"
    cursor.execute(query, (selected_category,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    fill_table(rows)

# Handle table selection change
def on_tree_select(event):
    item = tree.focus()
    values = tree.item(item, 'values')
    if values:
        swedish_word = values[2]
        ukrainian_word = values[3]
        label1.config(text=f"{swedish_word} - {ukrainian_word}")

# Create the SQLite database
create_database()

# Main application window
root = tk.Tk()
root.title("Кличлієв Кирило, група №2, ЛР№3")

# Notebook for tabs
notebook = ttk.Notebook(root)
tab1 = tk.Frame(notebook)
tab2 = tk.Frame(notebook)
notebook.add(tab1, text='Словник')
notebook.add(tab2, text='Про автора')
notebook.pack(fill='both', expand=True)

# Elements for tab1 (Dictionary)
label1 = tk.Label(tab1, text='Обране слово буде відображене тут')
label1.pack(padx=20, pady=20)

# Combobox in tab1
conn = sqlite3.connect('swed-ukr.db')
cur = conn.cursor()
cur.execute("SELECT DISTINCT category FROM vocab")
unique_values = [value[0] for value in cur.fetchall()]
conn.close()

combo_box = ttk.Combobox(tab1, values=unique_values)
combo_box.pack(padx=20, pady=10)
combo_box.set("Оберіть категорію слів")

# Treeview (table) in tab1
tree = ttk.Treeview(tab1, columns=('id', 'category', 'swedish_word', 'ukrainian_word'), show='headings')
tree.heading('#0', text='ID')
tree.heading('id', text='ID')
tree.heading('category', text='Category')
tree.heading('swedish_word', text='Swedish Word')
tree.heading('ukrainian_word', text='Ukrainian Word')
tree.pack(fill='both', expand=True)

# Scrollbar for the table
scrollbar = ttk.Scrollbar(tab1, orient="vertical", command=tree.yview)
scrollbar.pack(side="right", fill="y")
tree.configure(yscrollcommand=scrollbar.set)

# Bind events
tree.bind('<<TreeviewSelect>>', on_tree_select)
combo_box.bind('<<ComboboxSelected>>', on_combobox_change)

# Fill table with initial data
fill_table(fetch_data())

# Elements for tab2 (About the Author)
label2 = tk.Label(tab2, text='Кличлієв Кирило Сердарович\nЧернігів, Україна', font=('Arial', 16, 'bold'))
label2.configure(anchor='center')
label2.pack()

def open_github():
    webbrowser.open("https://github.com/klychliiev")

def open_linkedin():
    webbrowser.open('https://www.linkedin.com/in/kyrylo-klychliiev/')

label3 = tk.Label(tab2, text='GitHub', fg='black', cursor='hand2', font=('Arial', 16, 'underline'))
label3.pack()
label3.bind('<Button-1>', lambda e: open_github())

label4 = tk.Label(tab2, text='LinkedIn', fg='black', cursor='hand2', font=('Arial', 16, 'underline'))
label4.pack()
label4.bind('<Button-1>', lambda e: open_linkedin())

label5 = tk.Label(tab2, text='kyrylo.klychliiev@gmail.com', font=('Arial', 16, 'underline'))
label5.pack()

# Start the application
root.mainloop()
