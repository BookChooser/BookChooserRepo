import streamlit as st
import pandas as pd
from io import StringIO

st.title("Welcome to Book Chooser")
st.write("To start, upload your Goodreads library below:")
uploaded_file = st.file_uploader("Upload your CSV", type = "csv" )
if uploaded_file is not None:

    # Can be used wherever a "file-like" object is accepted:
    dataframe = pd.read_csv(uploaded_file)
    st.write(dataframe)

st.write("You have ", 200," books on your to-read shelf, how many would you like to compare?")
number_book_comparisons = st.number_input("Number of books to compare", min_value=2, max_value=None,value=2, step=1)
st.write("You want to compare", number_book_comparisons, "books")
values = st.slider("Page Count", 0, 1000, (0,1000))
st.write("Values:", values)
st.button("START")

class BookView:
    @staticmethod
    def display_books(books):
        print("\nBook List:")
        for book in books:
            print(f"Title: {book.title}, Author: {book.author}, ISBN: {book.isbn}")


class display_books:
    pass

class display_welcome_screen:
    pass

class display_winner_screen:
    pass
