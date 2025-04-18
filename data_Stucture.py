from tkinter import messagebox

class bookNode:
    def __init__(self, book_id, name, author, year):
        self.book_id = book_id
        self.name = name
        self.author = author
        self.year = year
        self.left = None
        self.right = None


class BookLibrary:
    def __init__(self):
        self.root = None
        self.filename = "library_data.txt"
        self.load_books_from_file()

    def _insert(self, node, book_id, name, author, year):
        if node is None:
            return bookNode(book_id, name, author, year)
        if book_id > node.book_id:
            node.right = self._insert(node.right, book_id, name, author, year)
        elif book_id < node.book_id:
            node.left = self._insert(node.left, book_id, name, author, year)
        return node

    def insert(self, book_id, name, author, year):
        if self.search(book_id):
            raise ValueError("A book with this ID already exists.")

        if self._check_duplicate_name_author(self.root, name, author):
            raise ValueError("A book with the same name and author already exists.")

        self.root = self._insert(self.root, book_id, name, author, year)
        self.save_books_to_file()

    def _check_duplicate_name_author(self, node, name, author):
        if node is None:
            return False
        if node.name.lower() == name.lower() and node.author.lower() == author.lower():
            return True
        return (self._check_duplicate_name_author(node.left, name, author) or
                self._check_duplicate_name_author(node.right, name, author))

    def _search(self, node, book_id):
        if node is None or node.book_id == book_id:
            return node
        if book_id > node.book_id:
            return self._search(node.right, book_id)
        else:
            return self._search(node.left, book_id)

    def search(self, book_id):
        return self._search(self.root, book_id)

    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def _delete(self, node, book_id):
        if node is None:
            return node
        if book_id > node.book_id:
            node.right = self._delete(node.right, book_id)
        elif book_id < node.book_id:
            node.left = self._delete(node.left, book_id)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            temp = self._min_value_node(node.right)
            node.book_id = temp.book_id
            node.name = temp.name
            node.author = temp.author
            node.year = temp.year
            node.right = self._delete(node.right, temp.book_id)
        return node

    def delete(self, book_id):
        if not self.search(book_id):
            raise ValueError("Book ID not found.")
        self.root = self._delete(self.root, book_id)
        self.save_books_to_file()

    def _inorder(self, node, books):
        if node:
            self._inorder(node.left, books)
            books.append(node)
            self._inorder(node.right, books)

    def display_books(self, sort_by="id"):
        books = []
        self._inorder(self.root, books)
        if sort_by == "name":
            books.sort(key=lambda x: x.name.lower())
            header = "Sorted by: Book Name\n\n"
        else:
            books.sort(key=lambda x: x.book_id)
            header = "Sorted by: Book ID\n\n"
        return header + "".join(
            f"ID: {b.book_id}, Book: {b.name}, Author: {b.author}, Year: {b.year}\n"
            for b in books
        )

    def save_books_to_file(self):
        books = []
        self._inorder(self.root, books)
        with open(self.filename, "w") as f:
            for b in books:
                f.write(f"{b.book_id},{b.name},{b.author},{b.year}\n")

    def load_books_from_file(self):
        try:
            with open(self.filename, "r") as f:
                for line in f:
                    parts = line.strip().split(",")
                    if len(parts) == 4:
                        book_id, name, author, year = parts
                        self.root = self._insert(self.root, int(book_id), name, author, int(year))
        except FileNotFoundError:
            messagebox.showerror("File Not Found", "The books.txt file was not found.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
