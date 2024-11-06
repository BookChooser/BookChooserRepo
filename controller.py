import re

from matplotlib import lines

from Book import Book
from UserInterface import BookView

class BookController:
    def __init__(self):
        self.model = Book()
        self.view = BookView()

    def add_book(self):
        title, author, isbn10, isbn13, year, page_count, description, cover_url = self.view.get_book_details()
        book = Book(self, title, author, isbn10, isbn13, year, page_count, description, cover_url)
        self.model.add_book(book)
        print("Book added successfully.")

    def display_books(self):
        books = self.model.get_books()
        self.view.display_books(books)

    def store_lines(self):
        # Open the file.
        csv_file = open('booklist.csv', 'r')

        # Read the file's lines into a list.
        lines = csv_file.readlines()

        # Close the file.
        csv_file.close()

        # Process the lines.
        for line in lines[1:]:
            # Get the book as tokens.
            modified_line = re.sub(r',(?=\S)', '|', line)

            book = modified_line.split('|')
            print(book)

"""
- read in .csv file line by line & clean up all unnecessary characters
- check if category is "to-read"
- if yes, check where isbn is available and look it up where necessary
- look up missing metadata
- create book object
- add book object to list
"""



