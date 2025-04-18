from tkinter import *
from tkinter import messagebox, simpledialog
from data_Structure import BookLibrary

def display_book(sort_by="id"):
    msg = library.display_books(sort_by)
    book_list.config(state=NORMAL)
    book_list.delete("1.0", END)
    book_list.insert(END, msg)
    book_list.config(state=DISABLED)

def insert_Func(book_id, name, author, year):
    try:
        library.insert(int(book_id), name, author, int(year))
        # Clear input fields
        for entry in [id_input, name_input, author_input, year_input]:
            entry.delete(0, END)
        display_book() # Update the display after insertion
        messageBox("Success", "Book inserted successfully.")
    except ValueError as ve:
        messageBox("Insert Error", str(ve))
    except Exception as e:
        messageBox("Error", "Invalid input. Please check your entries.")

def search_book(book_id):
    try:
        book = library.search(int(book_id))
        if book:
            messageBox("Library", f"Found: {book.name} by {book.author} ({book.year})")
        else:
            messageBox("Library", "No book found")
    except ValueError:
        messageBox("Search Error", "Invalid Book ID. Please enter a number.")

def delete_window():
    delete_id = simpledialog.askinteger("Delete Book", "Enter Book ID to delete:")
    if delete_id is not None:
        try:
            if library.search(delete_id):
                library.delete(delete_id)
                display_book() # Update the display after deletion
                messageBox("Library", f"Book with ID {delete_id} deleted.")
            else:
                messageBox("Library", "Book ID not found!")
        except ValueError as ve:
            messageBox("Delete Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during deletion: {e}")

def messageBox(title, text):
    messagebox.showinfo(title, text)

window = Tk()
window.geometry("400x600")
window.title("Book Library")
library = BookLibrary()

# --- Input Frame ---
input_frame = LabelFrame(window, text="Add New Book", padx=10, pady=10)
input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

Label(input_frame, text="Book ID:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
id_input = Entry(input_frame)
id_input.grid(row=0, column=1, sticky="ew", padx=5, pady=2)

Label(input_frame, text="Book Name:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
name_input = Entry(input_frame)
name_input.grid(row=1, column=1, sticky="ew", padx=5, pady=2)

Label(input_frame, text="Author:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
author_input = Entry(input_frame)
author_input.grid(row=2, column=1, sticky="ew", padx=5, pady=2)

Label(input_frame, text="Year:").grid(row=3, column=0, sticky="w", padx=5, pady=2)
year_input = Entry(input_frame)
year_input.grid(row=3, column=1, sticky="ew", padx=5, pady=2)

insert_btn = Button(input_frame, text="Insert Book", command=lambda: insert_Func(id_input.get(), name_input.get(), author_input.get(), year_input.get()))
insert_btn.grid(row=4, column=0, columnspan=2, pady=5, sticky="ew")

# --- Action Buttons Frame ---
action_frame = LabelFrame(window, text="Actions", padx=10, pady=10)
action_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

search_btn = Button(action_frame, text="Search by ID", command=lambda: search_book(id_input.get()))
search_btn.grid(row=0, column=0, pady=2, sticky="ew")

delete_btn = Button(action_frame, text="Delete by ID", command=delete_window)
delete_btn.grid(row=1, column=0, pady=2, sticky="ew")

display_id_btn = Button(action_frame, text="Display (Sort by ID)", command=lambda: display_book("id"))
display_id_btn.grid(row=2, column=0, pady=2, sticky="ew")

display_name_btn = Button(action_frame, text="Display (Sort by Name)", command=lambda: display_book("name"))
display_name_btn.grid(row=3, column=0, pady=2, sticky="ew")

# --- Display Area ---
display_frame = LabelFrame(window, text="Book List", padx=10, pady=10)
display_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
window.grid_rowconfigure(2, weight=1)
window.grid_columnconfigure(0, weight=1)

book_list = Text(display_frame, wrap=WORD, state=DISABLED)
book_list.pack(fill="both", expand=True)

scrollbar = Scrollbar(display_frame, command=book_list.yview)
scrollbar.pack(side=RIGHT, fill="y")
book_list.config(yscrollcommand=scrollbar.set)


exit_btn = Button(window, text="Exit", command=window.destroy)
exit_btn.grid(row=3, column=0, pady=10, sticky="ew")

display_book() # Initial display of books
window.mainloop()