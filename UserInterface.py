import streamlit as st

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
