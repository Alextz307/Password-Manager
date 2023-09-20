from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
           'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
           'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
NUMBERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
SYMBOLS = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


def generate_password():
    req_letters = random.randint(8, 10)
    req_symbols = random.randint(2, 4)
    req_numbers = random.randint(2, 4)

    password_list = []

    for data, req in [(LETTERS, req_letters), (SYMBOLS, req_symbols), (NUMBERS, req_numbers)]:
        password_list.extend([random.choice(data) for _ in range(req)])

    random.shuffle(password_list)

    password = ''.join(password_list)

    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def write_data(data):
    with open('data.json', 'w') as data_file:
        json.dump(data, data_file, indent=4)


def save_data():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title='Something went wrong', message='Please make sure that you fill in all the fields!')
    else:
        is_ok = messagebox.askokcancel(title=website, message=f'These are the details entered:\nEmail: {email}\n'
                                                              f'Password: {password}\nIs it ok to save?')

        if is_ok:
            new_data = {
                website: {
                    'email': email,
                    'password': password
                }
            }

            try:
                with open('data.json', 'r') as data_file:
                    data = json.load(data_file)
                    data.update(new_data)
            except FileNotFoundError:
                write_data(new_data)
            else:
                write_data(data)
            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)


# --------------------------- SEARCH DATA ------------------------------ #
def find_data():
    website = website_entry.get()

    if len(website) == 0:
        messagebox.showinfo(title='Something went wrong', message='Please make sure that you fill in the field!')
    else:
        try:
            with open('data.json', 'r') as data_file:
                data = json.load(data_file)
                email = data[website]['email']
                password = data[website]['password']
        except FileNotFoundError:
            messagebox.showerror(title='Something went wrong', message='No data file found!')
        except KeyError:
            messagebox.showerror(title='Something went wrong', message='No details exist for this website!')
        else:
            messagebox.showinfo(title=website, message=f'Email: {email}\nPassword: {password}')


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title('Password Manager')
window.config(bg='white', padx=50, pady=50)

# Image
canvas = Canvas(height=200, width=200, bg='white', highlightthickness=0)
logo_image = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=logo_image)
canvas.grid(row=0, column=1)


# Labels
def create_label(new_text, new_row):
    new_label = Label(text=new_text, bg='white', fg='black')
    new_label.grid(row=new_row, column=0)
    return new_label


website_label = create_label(new_text='Website:', new_row=1)
email_label = create_label(new_text='Email/Username:', new_row=2)
password_label = create_label(new_text='Password:', new_row=3)


# Entries
def create_entry(new_width, new_row, new_column_span):
    new_entry = Entry(width=new_width, bg='white', fg='black', insertbackground='black', highlightthickness=0)
    new_entry.grid(row=new_row, column=1, columnspan=new_column_span)
    return new_entry


website_entry = create_entry(new_width=23, new_row=1, new_column_span=1)
website_entry.focus()

email_entry = create_entry(new_width=39, new_row=2, new_column_span=2)
email_entry.insert(0, 'alexofficialadress7@gmail.com')

password_entry = create_entry(new_width=23, new_row=3, new_column_span=1)


# Buttons
def create_button(new_text, new_width, new_row, new_column, new_column_span):
    new_button = Button(text=new_text, width=new_width, bg='white', fg='black', highlightthickness=0,
                        padx=0, pady=0, borderwidth=0, highlightbackground='white')
    new_button.grid(row=new_row, column=new_column, columnspan=new_column_span)
    return new_button


search_button = create_button(new_text='Search', new_width=12, new_row=1, new_column=2, new_column_span=1)
search_button.config(command=find_data)

password_button = create_button(new_text='Generate Password', new_width=12, new_row=3, new_column=2, new_column_span=1)
password_button.config(command=generate_password)

add_button = create_button(new_text='Add', new_width=36, new_row=4, new_column=1, new_column_span=2)
add_button.config(command=save_data)

window.mainloop()
