import random
import streamlit as st

st.title("2 Books from Book List")

#while len(st.session_state.book_list) > 1:
# Randomly select two books
selected_books = random.sample(st.session_state.book_list, 2)
for book in selected_books:
    st.write(book.title)
    st.write(book.author)
    st.write(book.isbn10)
    st.write(book.isbn13)
    st.write(book.year)
    st.write(book.page_count)
    st.write(book.description)
    st.write(book.cover_url)

# Display the titles using Streamlit
#st.title("Randomly Selected Books")
#for book in selected_books:
    #st.write(f"Title: {book.title}")