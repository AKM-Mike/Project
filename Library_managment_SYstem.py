from tkinter import *
from tkinter import messagebox, simpledialog
from data_Stucture import BookLibrary

window = Tk()
window.geometry("300x500")
library = BookLibrary()


def insert_Func(book_id, name, author, year):
    try:
        library.insert(int(book_id), name, author, int(year))
        id_input.delete(0, END)
        name_input.delete(0, END)
        author_input.delete(0, END)
        year_input.delete(0, END)
        messageBox("Success", "Book inserted successfully.")
    except ValueError as ve:
        messageBox("Insert Error", str(ve))
    except Exception as e:
        messageBox("Error", "Invalid input. Please check your entries.")


def search_book(book_id):
    book = library.search(int(book_id))
    if book:
        messageBox("Library", f"Found: {book.name} by {book.author} ({book.year})")
    else:
        messageBox("Library", "No book found")


def delete_window():
    delete_id = simpledialog.askinteger("Delete Book", "Enter Book ID to delete:")
    if delete_id is not None:
        if library.search(delete_id):
            library.delete(delete_id)
            messageBox("Library", f"Book with ID {delete_id} deleted.")
        else:
            messageBox("Library", "Book ID not found!")


def display_book(sort_by="id"):
    msg = library.display_books(sort_by)
    messageBox("Library Books", msg if msg else "No books in library.")


def messageBox(title, text):
    messagebox.showinfo(title, text)


# Input Fields
Label(text="Book ID").pack()
id_input = Entry()
id_input.pack()

Label(text="Book Name").pack()
name_input = Entry()
name_input.pack()

Label(text="Author").pack()
author_input = Entry()
author_input.pack()

Label(text="Year").pack()
year_input = Entry()
year_input.pack()

btn_config = {"width": 25, "height": 2, "font": ("Arial", 10), "padx": 3, "pady": 3}

# Buttons
Button(text="Insert",command=lambda: insert_Func(id_input.get(), name_input.get(), author_input.get(), year_input.get()), **btn_config).pack()

Button(
    text="Search by ID", command=lambda: search_book(id_input.get()), **btn_config
).pack()

Button(
    text="Delete by ID", command=delete_window, **btn_config
).pack()

Button(
    text="Display (Sort by ID)", command=lambda: display_book("id"), **btn_config
).pack()

Button(
    text="Display (Sort by Name)", command=lambda: display_book("name"), **btn_config
).pack()

window.mainloop()
