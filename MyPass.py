from tkinter import *
from tkinter import messagebox
import pyperclip
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
import string
import random

letters = string.ascii_lowercase + string.ascii_uppercase
symbols = string.punctuation[2:4]
numbers = string.digits

def passgen(n_letters=6,n_symbols=1,n_numbers=3):

    password = []
    for char in range(n_letters):
        password.append(random.choice(letters))

    for char in range(n_symbols):
        password.append(random.choice(symbols))

    for char in range(n_numbers):
        password.append(random.choice(numbers))

    random.shuffle(password)

    pass_word = ''.join(password)
    if password_entry.get() == '':
        password_entry.insert(0, pass_word)
        generate_btn.config(text='Copy!')
    elif password_entry.get() != '':
        pyperclip.copy(password_entry.get())
        generate_btn.config(text='Generate')
        password_entry.delete(0, 'end')

# ---------------------------- CONNECT DATABASE PASSWORDS ------------------------------- #

# install pymongo ~ pip install pymongo 
# Impor ting pymongo so you can work with mongodb in python
import pymongo 
# Connection with mongodb
db = pymongo.MongoClient("mongodb://localhost:27017/")
# Creating the Database "passwords"
# MongoDB will create the database if it does not exist.
pwDB = db["passwords"]

# ---------------------------- SAVE PASSWORD ------------------------------- #
def savepass():
    password = password_entry.get()
    email = email_entry.get()
    website = website_entry.get().capitalize()
    if password == '' or email == '' or website == '':
        messagebox.showwarning(message="Please make sure to fill all the fields", title="MyPass")
    else:
        # Mongodb Document 
        new_data = {
            "website": website,
            "email" : email,
            "password" : password,
        }
        if pwDB["passwords_col"].find_one({"website": website}) == None:
            pwDB["passwords_col"].insert_one(new_data)
        else:
            pwDB["passwords_col"].update_one({"website": website}, {"$set" : new_data})

        messagebox.showinfo(message="Saved Successfully!", title="MyPass")

        password_entry.delete(0, 'end')
        website_entry.delete(0, 'end')
        generate_btn.config(text='Generate')
# ---------------------------- SEARCH PASSWORD ------------------------------- #
def searchpass():
    website = website_entry.get().capitalize()
    try:
        account = pwDB["passwords_col"].find_one({"website" : website})

        if account != None:
            email = account["email"]
            password = account["password"]
            pyperclip.copy(password)
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}\n\nPassword copied!")
            
        else:
            messagebox.showwarning(message="No details found", title="MyPass")

    except:
        messagebox.showerror(message="No data file found", title="MyPass")


# ---------------------------- UI SETUP ------------------------------- #
from window import Window
win = Window(title="Password Manager", width=600, height=420)
win.config(padx=60, pady=60)
win.maxsize(width=600, height=420)

# logo
logo = Canvas(width=200, height=200, highlightthickness=0)
logo_image = PhotoImage(file="/Users/yusufisawi/Documents/Self/Python/pythonAdvanced/password-manager/logo.png")
logo.create_image(101, 101 , image=logo_image)
logo.grid(column=1, row=0)
# logo------
FONT = "Ariel"
# labels
website_label = Label(text="Website", font=(FONT, 15),)
website_label.grid(column=0, row=1,)

email_label = Label(text="Email/Username", font=(FONT, 15),)
email_label.grid(column=0, row=2,)

password_label = Label(text="Password", font=(FONT, 15),)
password_label.grid(column=0, row=3,)
# entries
website_entry = Entry(border=0,width=21, highlightthickness=1, highlightcolor="red", cursor="text")
website_entry.grid(column=1, row=1, ipady=2, pady=2)
website_entry.focus()
# ----
email_entry = Entry(border=0,width=39, highlightthickness=1, highlightcolor="red", cursor="text")
email_entry.grid(column=1, row=2, columnspan=2, ipady=2, pady=2)
email_entry.insert(0, "yusufisawi@gmail.com")
# ----
password_entry = Entry(border=0,width=21, highlightthickness=1, highlightcolor="red", cursor="text")
password_entry.grid(column=1, row=3 ,ipady=2, pady=2)

# buttons
generate_btn = Button(text="Generate", highlightthickness=0, border=0, width=14, command=passgen)
generate_btn.grid(column=2, row=3 , pady=2)

add_button = Button(text="Add", width=36, highlightthickness=0, border=0, command=savepass).grid(row=4, column=1, columnspan=2,pady=2)

search_btn = Button(text="Search", highlightthickness=0, border=0, width=14, command=searchpass)
search_btn.grid(column=2, row=1 , pady=2)

win.mainloop()




