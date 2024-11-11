import re
from isbnlib import desc, cover, isbn_from_words
from isbnlib.registry import bibformatters
from Book import Book
import UserInterface
from UserInterface import BookView

SERVICE = "openl"
bibtex = bibformatters["bibtex"]

class BookController:

    def __init__(self):
        self.view = BookView()
        self.book_list = []
        # initialize instance variables that are needed across several methods
        self.__description = None
        self.__cover_url = None

    def display_books(self):
        books = self.model.get_books()
        self.view.display_books(books)

    def store_lines(self):
        # Open the file.
        # gets uploaded file from view, encoding allows to use it on a file downloaded from goodreads:
        with open(UserInterface.uploaded_file, 'r', encoding='latin-1') as file:
        # gets file from resources folder, encoding allows to use it on a file downloaded from goodreads:
        #with open('resources/booklist.csv', 'r', encoding='latin-1') as file:
            # Read the file's lines into a list.
            lines = file.readlines()

        # Process the lines.
        for line in lines[1:]:
            # Get the book as tokens.
            modified_line = re.sub(r',(?=\S)', '|', line)
            # Split the line into columns.
            book_line = modified_line.split('|')
            print("print the book_line before checking shelf: ", book_line)

            # Access the needed values from the .csv columns.
            title = book_line[1]
            author = book_line[2]
            isbn10 = re.sub(r'[\"=]', '', book_line[5])
            isbn13 = re.sub(r'[\"=]', '', book_line[6])
            page_count = book_line[11]
            year = book_line[13]
            bookshelf = book_line[16]
            if bookshelf == "to-read":
                # Look up description and cover_url using isbn. If isbn is not available, using book title
                if len(isbn10) and len(isbn13) != 0:
                    self.isbn_check(isbn10, isbn13)
                else:
                    self.title_check(title)
                if len(self.__description) == 0:
                    self.__description = "No description available"
                if len(self.__cover_url) == 0:
                    self.__cover_url == "Display default cover_url"
                # Create a new Book object and add it to book_list
                new_book = Book(title, author, isbn10, isbn13, year, page_count, self.__description, self.__cover_url)
                self.book_list.append(new_book)
                print("new book added: ", new_book.title)


    def isbn_check (self, isbn10, isbn13):
        # Retrieve metadata using ISBN-10 or ISBN-13.
        if isbn13:
            try:
                #print("BibTeX:", bibtex(meta(isbn13, SERVICE)))
                print("Description:", desc(isbn13))
                print("Cover:", cover(isbn13), "\n")
                self.__description = desc(isbn13)
                self.__cover_url = cover(isbn13)
            except Exception as e:
                print(f"Error retrieving data for ISBN-13 {isbn13}: {e}\n")
        elif isbn10:
            try:
                #print("BibTeX:", bibtex(meta(isbn13, SERVICE)))
                print("Description:", desc(isbn10))
                print("Cover:", cover(isbn10), "\n")
                self.__description = desc(isbn10)
                self.__cover_url = cover(isbn10)
            except Exception as e:
                print(f"Error retrieving data for ISBN-10 {isbn10}: {e}\n")

    def title_check(self, title):
            try:
                # Fallback to title if both ISBN and ISBN-13 are missing.
                isbn13 = isbn_from_words(title)
                #print(bibtex(meta(isbn13, SERVICE)))
                print("description: ", desc(isbn13))
                print("cover: ", cover(isbn13))
                self.__description = desc(isbn13)
                self.__cover_url = cover(isbn13)
            except Exception as e:
                print(f"Error retrieving data for Title {title}: {e}\n")





"""
DONE:
- read in .csv file line by line & clean up all unnecessary characters: 
- check if category is "to-read": 
- if yes, check where isbn is available and look it up where necessary
- look up missing metadata
- create book object
- add book object to list
"""

"""
not sure if needed:
    def add_book(self):
        title, author, isbn10, isbn13, year, page_count, description, cover_url = self.view.get_book_details()
        book = Book(self, title, author, isbn10, isbn13, year, page_count, description, cover_url)
        self.model.add_book(book)
        print("Book added successfully.")
"""

