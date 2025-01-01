import random
import streamlit as st
from st_clickable_images import clickable_images
from streamlit import rerun

from BookTournament import winner_screen

# callback for buttons
def book_clicked(book_to_remove):
    st.session_state.book_remove = book_to_remove
    print("Book to remove: " + book_to_remove.title)

# remove book from list if set in session_state
if "book_remove" in st.session_state:
    st.session_state.book_comparisons.remove(st.session_state.book_remove)

# stop if only one book is left and go to winner screen
if len(st.session_state.book_comparisons) < 2:
    st.switch_page(winner_screen)

st.title("2 Books from Book List:")
st.write("Welcome to the Selector Screen!")
st.write("Which book would you like to read?")

# Create two columns to display the books side by side
col1, col2 = st.columns(2)

# Randomly select two books
book1, book2 = random.sample(st.session_state.book_comparisons, 2)

with col1:
    st.header(book1.title)
    st.image(book1.cover_url['thumbnail'])
    #if this button is pressed, remove the other displayed book
    st.button(book1.title, args=[book2], on_click=book_clicked)

    st.write(f"**Author:** {book1.author}")
    st.write(f"**ISBN-10:** {book1.isbn10}")
    st.write(f"**ISBN-13:** {book1.isbn13}")
    st.write(f"**Year:** {book1.year}")
    st.write(f"**Page Count:** {book1.page_count}")
    st.write(f"**Description:** {book1.description}")

with col2:
    st.header(book2.title)
    st.image(book2.cover_url['thumbnail'])
    #if this button is pressed, remove the other displayed book
    st.button(book2.title, args=[book1], on_click=book_clicked)

    st.write("")
    st.write(f"**Author:** {book2.author}")
    st.write(f"**ISBN-10:** {book2.isbn10}")
    st.write(f"**ISBN-13:** {book2.isbn13}")
    st.write(f"**Year:** {book2.year}")
    st.write(f"**Page Count:** {book2.page_count}")
    st.write(f"**Description:** {book2.description}")




# implement logic to remove 1 book from book_comparisons before uncommenting this line
# while len(st.session_state.book_comparisons) > 1:

# def button_on_image(book, key):
#     st.markdown(
#         f"""
#         <div style="position: relative; display: inline-block; text-align: center;">
#             <img src="{book.cover_url['thumbnail']}" alt="{book.title}" style="width: 180px; height: auto;">
#             <button style="position: absolute; top: 0%; left: 0%; width: 100%; height: 100%;
#                  background: green; border: none; cursor: pointer;"
#                  onclick=st.session_state.{key}>
#             </button>
#         </div>
#         """,
#         unsafe_allow_html=True
#     )
#     st.session_state.clicked = book
