import streamlit as st
import threading
import csv
import re
import random
from Style import load_css
from isbnlib import desc, cover, isbn_from_words
from Book import Book
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
    if st.session_state.currentThread == threading.current_thread().ident:
        quit()

# Main screen
load_css()
st.markdown("<h1 style='text-align: center;', class='title'>Welcome to the Book Tournament!</h1>", unsafe_allow_html=True)

# File uploader for Goodreads csv
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

        # Read in the csv file line by line
        # [1:] skips the first line
        for line in temp_book_list[1:]:
            try:
                # Access the needed values from the columns
                title: str = line[1]
                # Split title into title and series
                if '(' in title and ')' in title:
                    series = title.split('(')[1].split(')')[0].strip()
                    title = title.split('(')[0].strip()
                else:
                    series = "Not Applicable"
                author: str = line[2]
                isbn10: str = re.sub(r'[="]', '', line[5])  # removes equals and quotes signs
                isbn13: str = re.sub(r'[="]', '', line[6])  # removes equals and quotes signs
                page_count_str: str = line[11]
                if page_count_str.isdigit():
                    page_count: int = int(page_count_str)
                else:
                    page_count = 0
                year: str = line[13]
                bookshelf: str = line[16]
                # Add "to-read" books to final_book_list
                if bookshelf == "to-read":
                    new_book = Book(title, series, author, isbn10, isbn13, year, page_count, '', '')
                    final_book_list.append(new_book)
                    print(new_book) #TODO: remove

            except IndexError as e:
                st.error(f"Error processing line: {line}. Index out of range: {e}")
            except Exception as e:
                st.error(f"Unexpected error processing line: {line}. Error: {e}")

            st.session_state.final_book_list = final_book_list


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

    # Number input Widget to set the number of books to compare
    # Allows the user to select a number between 2 and the length of final_book_list
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


        if st.button("START",type="primary"):
            # caches the randomly selected books
            st.session_state.book_comparisons = book_comparisons
            #initialize progress bar with message to user
            progress_text = "Looking up metadata and preparing the tournament for you"
            progress_bar = st.progress(0, text=progress_text)
            processed_books = 0
            for book in st.session_state.book_comparisons:
                # Look up missing metadata using isbn and if not available, book title
                if len(book.isbn10) and len(book.isbn13) > 4:
                    # Retrieve metadata using ISBN-10 or ISBN-13.
                    if book.isbn13:
                        try:
                            isbn13 = str(int(float(book.isbn13)))
                            __description = desc(book.isbn13)
                            __cover_url = cover(book.isbn13)

                        except Exception as e:
                            print(f"Error retrieving data for ISBN-13 {book.isbn13}: {e}\n")
                    elif book.isbn10:
                        try:
                            __description = desc(book.isbn10)
                            __cover_url = cover(book.isbn10)
                        except Exception as e:
                            print(f"Error retrieving data for ISBN-10 {book.isbn10}: {e}\n")
                else:
                    try:
                        # Fallback to title if both ISBN and ISBN-13 are missing.
                        isbn13 = isbn_from_words(book.title)
                        __description = desc(book.isbn13)
                        __cover_url = cover(book.isbn13)

                    except Exception as e:
                        print(f"Error retrieving data for Title {book.title}: {e}\n")
                # if year is empty, add default year
                if len(book.year) == 0:
                    year = "Unavailable"
                # if description is empty, add default text
                if __description is None:
                    __description = "Unavailable"
                # if cover_url is empty, add default thumbnail
                if __cover_url is None:
                    __cover_url = {}
                if not __cover_url.get("thumbnail"):
                    __cover_url["thumbnail"] = default_thumbnail_url

                # Create a new Book object and add it to book_list
                book.description = __description
                book.cover_url = __cover_url

                #update the progress bar
                processed_books += 1
                progress = processed_books / number_book_comparisons
                progress_bar.progress(progress, text=progress_text)

            # Switch to the next page
            st.switch_page(selector_screen)