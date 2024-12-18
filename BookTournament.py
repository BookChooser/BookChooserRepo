"""
update 11 Nov 24: currently this class is most recent together with Book.py and pages in "pages" folder.
Run by typing "streamlit run BookTournament.py" in terminal

class getting some metadata, a description and cover incl thumbnail from OpenLibrary.org api
(also possible to get from Google Books or Wikipedia apis)
Important: input ISBN13 (not ISBN10)

Steps needed for it to work:
1. add a local virtual environment for the project
2. install pip: right-click project, open in Terminal. In terminal type:  py -m ensurepip --upgrade
3. install isbnlib: in terminal type: pip install isbntools
4. upgrade setuptools: in terminal type: pip install --upgrade setuptools
"""
import streamlit as st
import pandas as pd
import re
from isbnlib import meta, desc, cover, isbn_from_words
from isbnlib.registry import bibformatters
from Book import Book
import random
import csv
from io import StringIO

#instance variables
temp_book_list = []
final_book_list = []
__description = None
__cover_url = None
default_thumbnail_url = "http://google.com" #TODO: change to actual default thumbnail

st.title("Welcome to Book Chooser")
st.write("To start, upload your Goodreads library below:")

uploaded_file = st.file_uploader("Upload your CSV", type="csv")

if uploaded_file is not None:
    print("File uploaded")
    # Can be used wherever a "file-like" object is accepted:
    dataframe = pd.read_csv(uploaded_file)
    st.write(dataframe)

    temp_book_list = dataframe.astype(str).values.tolist()
    # print("booklist before formatting: ", temp_book_list)

    for line in temp_book_list:
        #print("Processing line: ", line)

        # Access the needed values from the columns
        title: str = line[1]
        author: str = line[2]
        isbn10: str = re.sub(r'[="]', '', line[5]) #removes equals and quotes signs
        isbn13: str = re.sub(r'[="]', '', line[6]) #removes equals and quotes signs
        page_count: str = line[11]
        year: str = line[13]
        bookshelf: str = line[16]
        #print(bookshelf)
        if bookshelf == "to-read":
            # Look up missing metadata using isbn and if not available, book title
            if len(isbn10) and len(isbn13) > 4:
                print(title, ": look up metadata with isbn10 and 13")
                # Retrieve metadata using ISBN-10 or ISBN-13.
                if isbn13:
                    try:
                        # print("BibTeX:", bibtex(meta(isbn13, SERVICE)))
                        isbn13 = str(int(float(isbn13)))
                        print("ISBN-13 of: ", title, " = ", isbn13)
                        print("description:", desc(isbn13))
                        print("cover_url:", cover(isbn13), "\n")
                        __description = desc(isbn13)
                        __cover_url = cover(isbn13)
                    except Exception as e:
                        print(f"Error retrieving data for ISBN-13 {isbn13}: {e}\n")
                elif isbn10:
                    try:
                        # print("BibTeX:", bibtex(meta(isbn10, SERVICE)))
                        print("Description:", desc(isbn10))
                        print("Cover:", cover(isbn10), "\n")
                        __description = desc(isbn10)
                        __cover_url = cover(isbn10)
                    except Exception as e:
                        print(f"Error retrieving data for ISBN-10 {isbn10}: {e}\n")
            else:
                print(title, ": look up metadata with title")
                try:
                    # Fallback to title if both ISBN and ISBN-13 are missing.
                    isbn13 = isbn_from_words(title)
                    # print(bibtex(meta(isbn13, SERVICE)))
                    print("description: ", desc(isbn13))
                    print("cover: ", cover(isbn13))
                    __description = desc(isbn13)
                    __cover_url = cover(isbn13)
                except Exception as e:
                    print(f"Error retrieving data for Title {title}: {e}\n")
            #if year is empty, add default year
            if len(year) == 0:
                year = "Year published unavailable"
            #if description is empty, add default text
            if len(__description) == 0:
                __description = "Description unavailable"
            # if cover_url is empty, add default thumbnail
            if not __cover_url.get("thumbnail"):
                __cover_url["thumbnail"] = default_thumbnail_url
            # Create a new Book object and add it to book_list
            new_book = Book(title, author, isbn10, isbn13, year, page_count, __description,
                            __cover_url)
            final_book_list.append(new_book)
            print("New book added: ", new_book.title, "\n")

#display the to-read list incl the looked up metadata
#for development only. TODO: delete before submission to Rainer
st.write("To-Read list:")
dataframe_to_read = pd.DataFrame(final_book_list)
st.write(dataframe_to_read)

#cache the book list so it is remembered across all pages:
#https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state
if "final_book_list" not in st.session_state:
    st.session_state.final_book_list = final_book_list

if "temp_book_list" not in st.session_state:
    st.session_state.temp_book_list = temp_book_list

#Creates a number input widget that allows the user to select a number between 2 and
#the length of final_book_list, with a default value of 2 and a step size of 1.
#The selected value is stored in the number_book_comparisons variable.
st.write("You have ", final_book_list.__len__(), " books on your to-read shelf, how many would you like to compare?")
number_book_comparisons = st.number_input("Number of books to compare", min_value=2, max_value=final_book_list.__len__(), value=2,
                                          step=1)

st.write("You want to compare", number_book_comparisons, "books")
values = st.slider("Page Count", 0, 1000, (0, 1000))
st.write("Values:", values)
st.button("START")

book_comparisons = random.sample(final_book_list, number_book_comparisons)
if "book_comparisons" not in st.session_state:
    st.session_state.book_comparisons = book_comparisons

"""
Possibly the three screens will need to be added in three separate files?
See: https://www.youtube.com/watch?v=oqo8-1c4H-k&ab_channel=AndyMcDonald

    Welcome screen: Add all code needed on the welcome screen
        On uploading csv file, trigger BookController.store_lines and: 
        Look up the number of books on to-read shelf from BookController
        Look up the min and max number of pages of books on to-read shelf from BookController
        
    Tournament screen: Add all code needed for comparing the books
        On displaying the view, randomly select two books from BookController.book_list to display
        On selecting one of the books:
            eliminate the other one from BookController.book_list
            show two new books (or keep the "winner" and add one new book)
            
    Winner screen: Add all code needed for displaying the winner 
        Triggered when only one book is left on BookController.book_list
        
TODO: 
- display relative number of books on book_list
- display relative min and max number of pages on book_list
- random selection of 2 books from book_list and after first round, random selection of 1 new book, until only one book is left    
"""


