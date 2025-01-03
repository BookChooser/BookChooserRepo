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
import threading

import streamlit as st
import csv
import pandas as pd
import re
from isbnlib import desc, cover, meta, isbn_from_words

from Book import Book
import random

from BookTournament import selector_screen

# instance variables
final_book_list = []
__description = None
__cover_url = None
default_thumbnail_url = "https://publications.iarc.fr/uploads/media/default/0001/02/thumb_1291_default_publication.jpeg"

# Ensure the components are only rendered once
if "currentThread" not in st.session_state:
    st.session_state.currentThread = threading.current_thread().ident
else:
    #print("Session Thread value:" + str(st.session_state.currentThread) + " Current Thread value" + str(threading.current_thread().ident))
    if st.session_state.currentThread == threading.current_thread().ident:
        #print("Quiting!")
        quit()


# Main screen
st.title("Welcome to Book Chooser")

st.session_state.uploaded_file = st.file_uploader("To start, upload your Goodreads library here:", type="csv")

if st.session_state.uploaded_file is not None:
    if "final_book_list" not in st.session_state:
        try:
            # Read the CSV file using the csv module
            st.session_state.uploaded_file.seek(0)  # Reset file pointer to the beginning
            reader = csv.reader(st.session_state.uploaded_file.read().decode('utf-8').splitlines())
            temp_book_list = list(reader)
        except UnicodeDecodeError as e:
            st.error(f"Error decoding file: {e}")
        except csv.Error as e:
            st.error(f"Error reading CSV file: {e}")
        except Exception as e:
            st.error(f"Unexpected error: {e}")

        # [1:] skips the first line in the csv file
        for line in temp_book_list[1:]:
            # print("Processing line: ", line)
            try:
                # Access the needed values from the columns
                title: str = line[1]
                if '(' in title and ')' in title:
                    series = title.split('(')[1].split(')')[0].strip()
                    title = title.split('(')[0].strip()
                else:
                    series = "Not Applicable"
                print(title)
                print(series)
                author: str = line[2]
                print(author)
                isbn10: str = re.sub(r'[="]', '', line[5])  # removes equals and quotes signs
                print(isbn10)
                isbn13: str = re.sub(r'[="]', '', line[6])  # removes equals and quotes signs
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
                if bookshelf == "to-read":
                    new_book = Book(title, series, author, isbn10, isbn13, year, page_count, '', '')
                    print(new_book)
                    final_book_list.append(new_book)
                    print("New book added: ", new_book.title, "\n")

            except IndexError as e:
                st.error(f"Error processing line: {line}. Index out of range: {e}")
            except Exception as e:
                st.error(f"Unexpected error processing line: {line}. Error: {e}")

            st.session_state.final_book_list = final_book_list

    # Creates a number input widget that allows the user to select a number between 2 and
    # the length of final_book_list, with a default value of 2 and a step size of 1.
    # The selected value is stored in the number_book_comparisons variable.
    st.write("You have ", st.session_state.final_book_list.__len__(),
             " books on your to-read shelf!")

    # get max and min page count from final_book_list
    page_counts = [book.page_count for book in st.session_state.final_book_list]

    # Get the minimum and maximum page count
    min_page_count = min(page_counts)
    max_page_count = max(page_counts)

    # Widget to select page_count range. Sets the values of the slides to min and max page count, and in brackets the default selected range
    values = st.slider("Set the minimum and maximum page count:", min_page_count, max_page_count, (min_page_count, max_page_count))
    st.write("Note that page count can be 0 if Goodreads does not have the information")

    # assign the tuple from values to min_selected and max_selected:
    min_selected, max_selected = values

    # check which books match the selected page_count
    max_no_books = [book for book in st.session_state.final_book_list if min_selected <= book.page_count <= max_selected]

    # widget to set the number of books to compare
    number_book_comparisons = st.number_input("Set the number of books you wish to compare:", min_value=0,
                                              max_value=len(max_no_books),
                                              value=len(max_no_books),
                                              step=1)
    st.write("You want to compare", number_book_comparisons, "books")

    if number_book_comparisons < 2:
        st.write("You need to compare at least two books")
    else:
        filtered_books = [book for book in st.session_state.final_book_list if
                          min_selected <= book.page_count <= max_selected]

        # check if the number of filtered books is smaller than the number of books we wanted to compare earlier
        filtered_books_length = len(filtered_books)
        if filtered_books_length < number_book_comparisons:
            st.write("The number of books matching your filter criteria is: ", filtered_books_length)
            number_book_comparisons = filtered_books_length

        # selects a specified number (number_book_comparisons) of unique elements from the filtered_books list
        book_comparisons = random.sample(filtered_books, number_book_comparisons)


        if st.button("START"):
            # caches the randomly selected books
            st.session_state.book_comparisons = book_comparisons
            progress_text = "Looking up metadata and preparing the tournament for you"
            progress_bar = st.progress(0, text=progress_text)
            processed_books = 0
            for book in st.session_state.book_comparisons:
                # Look up missing metadata using isbn and if not available, book title
                if len(book.isbn10) and len(book.isbn13) > 4:
                    print(book.title, ": look up metadata with isbn10 and 13")
                    # Retrieve metadata using ISBN-10 or ISBN-13.
                    if book.isbn13:
                        try:
                            # print("BibTeX:", bibtex(meta(isbn13, SERVICE)))
                            isbn13 = str(int(float(book.isbn13)))
                            print("ISBN-13 of: ", book.title, " = ", book.isbn13)
                            print("description:", desc(book.isbn13))
                            print("cover_url:", cover(book.isbn13), "\n")
                            __description = desc(book.isbn13)
                            __cover_url = cover(book.isbn13)

                        except Exception as e:
                            print(f"Error retrieving data for ISBN-13 {book.isbn13}: {e}\n")
                    elif book.isbn10:
                        try:
                            # print("BibTeX:", bibtex(meta(isbn10, SERVICE)))
                            print("Description:", desc(book.isbn10))
                            print("Cover:", cover(book.isbn10), "\n")
                            __description = desc(book.isbn10)
                            __cover_url = cover(book.isbn10)
                        except Exception as e:
                            print(f"Error retrieving data for ISBN-10 {book.isbn10}: {e}\n")
                else:
                    print(book.title, ": look up metadata with title")
                    try:
                        # Fallback to title if both ISBN and ISBN-13 are missing.
                        isbn13 = isbn_from_words(book.title)
                        # print(bibtex(meta(isbn13, SERVICE)))
                        print("description: ", desc(book.isbn13))
                        print("cover: ", cover(book.isbn13))
                        __description = desc(book.isbn13)
                        __cover_url = cover(book.isbn13)

                    except Exception as e:
                        print(f"Error retrieving data for Title {book.title}: {e}\n")
                # if year is empty, add default year
                if len(book.year) == 0:
                    year = "Unavailable"
                # if description is empty, add default text
                if len(__description) == 0:
                    __description = "Unavailable"
                # if cover_url is empty, add default thumbnail
                if not __cover_url.get("thumbnail"):
                    __cover_url["thumbnail"] = default_thumbnail_url
                # Create a new Book object and add it to book_list
                book.description = __description
                book.cover_url = __cover_url
                processed_books += 1
                progress = processed_books / number_book_comparisons
                progress_bar.progress(progress, text=progress_text)
            st.switch_page(selector_screen)