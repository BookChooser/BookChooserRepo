import random
import streamlit as st
from st_clickable_images import clickable_images

from BookTournament import winner_screen

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
    if st.button(book1.title):
        st.session_state.book_comparisons.remove(book2)
        st.write("Removed book: ", book2.title)
    # button_on_image(book1, "button1")
    st.write("")
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
    if st.button(book2.title):
        st.session_state.book_comparisons.remove(book1)
        st.write("Removed book: ", book1.title)
    # button_on_image(book2, "button2")
    st.write("")
    st.write(f"**Author:** {book2.author}")
    st.write(f"**ISBN-10:** {book2.isbn10}")
    st.write(f"**ISBN-13:** {book2.isbn13}")
    st.write(f"**Year:** {book2.year}")
    st.write(f"**Page Count:** {book2.page_count}")
    st.write(f"**Description:** {book2.description}")


if len(st.session_state.book_comparisons) < 2:
    st.switch_page(winner_screen)
else:
    # TODO: delete for loop once no longer needed
    for book in st.session_state.book_comparisons:
        st.write(book.title)

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
