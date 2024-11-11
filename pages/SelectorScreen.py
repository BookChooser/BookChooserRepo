import random
import streamlit as st

st.title("All Books in Book List")
for book in st.session_state.book_list:
    st.write(book.__str__())

# Randomly select two books
#selected_books = random.sample(st.session_state.book_list, 2)

#st.title("2 Books from Book List")
#for book in selected_books:
    #st.write(book.__str__())



# Display the titles using Streamlit
#st.title("Randomly Selected Books")
#for book in selected_books:
    #st.write(f"Title: {book.title}")