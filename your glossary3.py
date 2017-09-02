from tkinter import *
import sqlite3
from tkinter.messagebox import askyesno
import os
from tkinter import messagebox

##################################################################################
root = Tk()
root.title("Your Glossary")
root.configure(bg="#BA68C8")
scrollbar_ver = Scrollbar(root, orient="vertical")
scrollbar_hor = Scrollbar(root)
Label(root, text="Words", bg="#BA68C8", font="Times 18 bold").grid(pady=10, row=0, column=1)

# dictonary
words = {}

word_box = Listbox(root, width=50, height=18)

# Functions

# def highlight_searched(*args):
#   search = search_var.get()
#   for i,item in enumerate(word_box):
#     if search.lower() in item.lower():
#         word_box.selection_set(i)
#     else:
#         word_box.selection_clear(i)
#   if search == '':
#       word_box.selection_clear(0, END)

#===========================================DATABASE===============================================#
db_conn = sqlite3.connect('words.db')
print("Database Created")

# treverse the db
theCursor = db_conn.cursor()

if os.path.isfile(r"C:\Users\Bablu\Desktop\New folder\database\words.db"):
    words = theCursor.execute("SELECT * FROM Words").fetchall()
    for word, meaning in sorted(words):
        print(word, meaning)
        word_box.insert("end", word)

else:
    try:
        BASE_DIR = os.path.dirname(os.path.abspath(r'C:\Users\Bablu\Desktop\New folder\database'))
        db_path = os.path.join(BASE_DIR, "words.db")
        with sqlite3.connect(db_path) as db_conn:
            db_conn.execute("CREATE TABLE Words(word TEXT NOT NULL, meaning TEXT NOT NULL)")
            db_conn.commit()
    except sqlite3.OperationalError:
        print("Table couldn't be created.")



#===========================================DATABASE===============================================#

def retriveData(theCursor):
    try:
        words = theCursor.execute("SELECT * FROM Words").fetchall()
        db_conn.commit()
        print(words)
        for word, meaning in sorted(words):
            print("Here", word)
            word_box.insert("end", word)
    except sqlite3.OperationalError:
        print("Not found")

    except:
        print("Couldn't Retrieve data")


def saveData(word, meaning):
    db_conn.execute("INSERT INTO Words(word, meaning) VALUES(?,?)", (word, meaning))
    db_conn.commit()
    print("Tabel Created")
    # print info to the console
    retriveData(theCursor)

def show_all():
    # clear the listbox
    word_box.delete(0, "end")
    # iterate through the keys and add to the listbox
    try:
        words = theCursor.execute("SELECT * FROM Words").fetchall()
        db_conn.commit()
        for word, meaning in sorted(words):
            word_box.insert("end", word)

    except sqlite3.OperationalError:
        print("Not found")

    except:
        print("Couldn't Retrieve data")



def show_one():
    meaning_box.insert("end", "-------Meaning------- ")
    meaning_box.delete(1, "end")
    word = word_box.get("active")
    words = theCursor.execute("SELECT * FROM Words")

    # tuple to dictionary
    words_dict = dict((w,m) for w,m in words)
    print(dict((w,m) for w,m in words))
    print(words_dict[word])
    meaning = words_dict[word]
    #meaning_box.insert("end", word + "\n")
    meaning_box.insert("end", meaning[0:25] + "\n")
    meaning_box.insert("end", meaning[25:50] + "\n")
    meaning_box.insert("end", meaning[50:100] + "\n")
    meaning_box.insert("end", meaning[100:125] + "\n")
    meaning_box.insert("end", meaning[125:150] + "\n")
    meaning_box.insert("end", meaning[150:175] + "\n")
    meaning_box.insert("end", meaning[175:200] + "\n")
    meaning_box.insert("end", meaning[225:250] + "\n")
    meaning_box.insert("end", meaning[250:275] + "\n")
    meaning_box.insert("end", meaning[275:300] + "\n")
    meaning_box.insert("end", meaning[300:375] + "\n")

    print(meaning)

def save_word(*args):
    word = enter_word.get()
    meaning = enter_meaning.get()
    if word and meaning != "":
        saveData(word, meaning)
        words[word] = meaning
    show_all()
    enter_word.delete(0, "end")
    enter_meaning.delete(0, "end")

def del_item():
    if(askyesno("", "Do you want to delete this word?")):
        # Get the text of the currently selected item
        word = word_box.get("active")
        print(word)
        db_conn.execute("DELETE FROM Words WHERE word=(?)", (word,))
        db_conn.commit()
        # Confirm if it is in the list
        # if word in words:
        #     del words[word]
        #Update the listbox
        show_all()


def del_all():
    if(askyesno("", "Do you want to remove all words?")):
        global words
        db_conn.execute("DELETE FROM Words")
        db_conn.commit()
        word_box.delete(0, "end")
        meaning_box.delete(0, "end")


def on_entry_click(event):
    """function that gets called whenever entry is clicked"""
    if enter_word.get() == 'Enter word':
        enter_word.delete(0, "end") # delete all the text in the entry
        enter_word.insert(0, '') #Insert blank for user input
        enter_word.config(fg = 'black')

def on_focusout(event):
    if enter_word.get() == '':
        enter_word.insert(0, 'Enter word')
        enter_word.config(fg = 'grey')


def on_entry_clickWord(event):
    """function that gets called whenever entry is clicked"""
    if enter_meaning.get() == 'Enter meaning':
        enter_meaning.delete(0, "end") # delete all the text in the entry
        enter_meaning.insert(0, '') #Insert blank for user input
        enter_meaning.config(fg = 'black')


def on_focusoutWord(event):
    if enter_meaning.get() == '':
        enter_meaning.insert(0, 'Enter meaning')
        enter_meaning.config(fg = 'grey')

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        db_conn.close()
        print("Database Closed")
        root.destroy()



#word_box = Listbox(root, width=50, height=18, yscrollcommand=scrollbar_ver.set)
scrollbar_hor.config(command=word_box.yview)
word_box.grid(padx=20, pady=10, row=1, column=1)
word_box.configure(font="Times 15")

Label(root, text="Meaning", bg="#BA68C8", font="Times 18 bold").grid(pady=10, row=0, column=2)

meaning_box = Listbox(root, width=50, height=18, yscrollcommand=scrollbar_ver.set, xscrollcommand=scrollbar_hor.set)
scrollbar_ver.config(command=meaning_box.xview)
meaning_box.grid(padx=20, pady=10, row=1, column=2)
meaning_box.configure(font="Times 15")



# Add entry box to add words
enter_word = Entry(root, font="Times 15", fg="gray")
enter_word.insert(0, 'Enter word')
enter_word.bind('<FocusIn>', on_entry_click)
enter_word.bind('<FocusOut>', on_focusout)
enter_word.grid()
enter_word.place(x=20, y=500, width=170)

enter_meaning = Entry(root, font="Times 15", fg="gray")
enter_meaning.insert(0, 'Enter meaning')
enter_meaning.bind('<FocusIn>', on_entry_clickWord)
enter_meaning.bind('<FocusOut>', on_focusoutWord)
enter_meaning.grid()
enter_meaning.place(x=225, y=500, width=170)

add_button = Button(root, text="Add to your list", font="Times 10 bold", command=save_word)
add_button.grid(padx=20, pady=10, row=3, column=1, sticky=E)

show_one = Button(root, text="Show Meaning", font="Times 10 bold", command=show_one)
show_one.grid()
show_one.place(relx=0.5, rely=0.5, anchor=CENTER)

load_data = Button(root, text="Load All Words", font="Times 10 bold", fg="red", command=show_all)
load_data.grid(padx=30, pady=10, row=3, column=2, sticky=W)


del_button = Button(root, text="Delete item", font="Times 10 bold", fg="red", command=del_item)
del_button.grid(padx=230, pady=10, row=3, column=2, sticky=W)

del_all_button = Button(root, text="Delete All", font="Times 10 bold", fg="red", command=del_all)

del_all_button.grid(padx=20, pady=10, row=3, column=2, sticky=E)

myName = Label(root, text="Developed by: Bablu Kumar")
myName.grid(row=4, column=2, sticky=E)

# Label(root, text="Search:", bg="#BA68C8", font="Times 18 bold").grid( pady=10, row=0, column=1, sticky=E)
# search_var = StringVar()
# search_var.trace('w', highlight_searched)
# search_bar = Entry(root, textvariable=search_var) #this should search through the strings listed under listbox_2 configs
# search_bar.grid(pady=10, padx=10, row=0, column=2, sticky=W)


root.protocol("WM_DELETE_WINDOW", on_closing)

root.bind('<Return>', save_word)
root.resizable(False, False)
root.mainloop()
###########################################################################
