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
import csv
import pandas as pd
import re
from isbnlib import desc, cover, isbn_from_words

from Book import Book
import random

from BookTournament import selector_screen

#instance variables
temp_book_list = []
final_book_list = []
__description = None
__cover_url = None
default_thumbnail_url = "https://publications.iarc.fr/uploads/media/default/0001/02/thumb_1291_default_publication.jpeg"

# Main screen
st.title("Welcome to Book Chooser")
st.write("To start, upload your Goodreads library below:")

uploaded_file = st.file_uploader("Upload your CSV", type="csv")

if uploaded_file is not None:
    try:
        print("File uploaded")
        if "uploaded_file" not in st.session_state:
            st.session_state.uploaded_file = uploaded_file
    except Exception as e:
        st.error(f"Error uploading file: {e}")

if "uploaded_file" not in st.session_state:
    st.write("")
else:
    if "temp_book_list" not in st.session_state:
        try:
            # Read the CSV file using the csv module
            uploaded_file.seek(0) # Reset file pointer to the beginning
            reader = csv.reader(st.session_state.uploaded_file.read().decode('utf-8').splitlines())
            st.session_state.temp_book_list = list(reader)
        except UnicodeDecodeError as e:
            st.error(f"Error decoding file: {e}")
        except csv.Error as e:
            st.error(f"Error reading CSV file: {e}")
        except Exception as e:
            st.error(f"Unexpected error: {e}")

    st.write(len(st.session_state.temp_book_list)) #TODO: delete (only for testing)
    st.write(st.session_state.temp_book_list)

    #temp_book_list = dataframe.astype(str).values.tolist()
    # print("booklist before formatting: ", temp_book_list)

    #[1:] skips the first line in the csv file
    for line in st.session_state.temp_book_list[1:]:
            #print("Processing line: ", line)
        try:
            # Access the needed values from the columns
            title: str = line[1]
            print(title)
            author: str = line[2]
            print(author)
            isbn10: str = re.sub(r'[="]', '', line[5]) #removes equals and quotes signs
            print(isbn10)
            isbn13: str = re.sub(r'[="]', '', line[6]) #removes equals and quotes signs
            print(isbn13)
            page_count_str: str = line[11]
            if page_count_str.isdigit():
                page_count: int = int(page_count_str)
            else:
                page_count = 0
            print(page_count)
            year: str = line[13]
            print(year)
            bookshelf: str = line[16]
            print(bookshelf)
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
                print(new_book)
                final_book_list.append(new_book)
                print("New book added: ", new_book.title, "\n")

        except IndexError as e:
            st.error(f"Error processing line: {line}. Index out of range: {e}")
        except Exception as e:
            st.error(f"Unexpected error processing line: {line}. Error: {e}")

    #cache the book list so it is remembered across all pages:
    #https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state
    if "final_book_list" not in st.session_state:
        st.session_state.final_book_list = final_book_list

    st.write("Length of final_book_list", len(final_book_list))
    for book in final_book_list:
        st.write(book.title)

    #Creates a number input widget that allows the user to select a number between 2 and
    #the length of final_book_list, with a default value of 2 and a step size of 1.
    #The selected value is stored in the number_book_comparisons variable.
    st.write("You have ", st.session_state.final_book_list.__len__(), " books on your to-read shelf, how many would you like to compare?")
    number_book_comparisons = st.number_input("Number of books to compare", min_value=0, max_value=st.session_state.final_book_list.__len__(), value=st.session_state.final_book_list.__len__(),
                                              step=1)
    st.write("You want to compare", number_book_comparisons, "books")

    #get max and min page count from final_book_list
    page_counts = [book.page_count for book in st.session_state.final_book_list]

    # Get the minimum and maximum page count
    min_page_count = min(page_counts)
    max_page_count = max(page_counts)

    #sets the values of the slides to min and max page count, and in brackets the default selected range
    values = st.slider("Page Count", min_page_count, max_page_count, (min_page_count, max_page_count))
    st.write("Values:", values)

    #assign the tuple from values to min_selected and max_selected:
    min_selected, max_selected = values

    filtered_books = [book for book in st.session_state.final_book_list if min_selected <= book.page_count <= max_selected]

    #check if the number of filtered books is smaller than the number of books we wanted to compare earlier
    filtered_books_length = len(filtered_books)
    if filtered_books_length < number_book_comparisons:
        st.write("The number of books matching your filter criteria is: ", filtered_books_length)
        number_book_comparisons = filtered_books_length

    #selects a specified number (number_book_comparisons) of unique elements from the filtered_books list
    book_comparisons = random.sample(filtered_books, number_book_comparisons)

    #caches the randomly selected books
    st.session_state.book_comparisons = book_comparisons

    if st.button("START"):
        st.switch_page(selector_screen)




# Possibly the three screens will need to be added in three separate files?
# See: https://www.youtube.com/watch?v=oqo8-1c4H-k&ab_channel=AndyMcDonald
#
#     Welcome screen: Add all code needed on the welcome screen
#         On uploading csv file, trigger BookController.store_lines and:
#         Look up the number of books on to-read shelf from BookController
#         Look up the min and max number of pages of books on to-read shelf from BookController
#
#     Tournament screen: Add all code needed for comparing the books
#         On displaying the view, randomly select two books from BookController.book_list to display
#         On selecting one of the books:
#             eliminate the other one from BookController.book_list
#             show two new books (or keep the "winner" and add one new book)
#
#     Winner screen: Add all code needed for displaying the winner
#         Triggered when only one book is left on BookController.book_list
#
# TODO:
# - display relative number of books on book_list
# - display relative min and max number of pages on book_list
# - random selection of 2 books from book_list and after first round, random selection of 1 new book, until only one book is left



