import streamlit as st

st.write("The winner is:")

for book in st.session_state.book_comparisons:
    st.write(book.title)
