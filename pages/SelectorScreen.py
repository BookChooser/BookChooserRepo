import random
import streamlit as st
from st_clickable_images import clickable_images
from streamlit import rerun

from BookTournament import winner_screen
from Style import load_css


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

load_css()
st.markdown("<h1 style='text-align: center;', class='title'>Time to make a decision!</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;', class='subheading1'>Which book would you like to read more?</h3>", unsafe_allow_html=True)

# Create two columns to display the books side by side
col1, col2 = st.columns(2)

# Randomly select two books
book1, book2 = random.sample(st.session_state.book_comparisons, 2)


with col1:
    # get the full title of the book and store it in a string variable
    book1_title = book1.title

    # Check if the title contains brackets and extract the substring
    # e.g. "Flames of Chaos (Legacy of the Nine Realms, #1)"
    # if '(' in book1_title and ')' in book1_title:
    #     book1_title_only = book1_title.split('(')[0].strip()
    #     series1 = book1_title.split('(')[1].split(')')[0].strip()
    # else:
    #     book1_title_only = book1_title
    #     series1 = "Not Applicable"

    #display the book title and cover
    st.header(book1.title, anchor=False)
    st.image(book1.cover_url['thumbnail'], width=200)

    # if this button is pressed, remove the other displayed book
    st.button(book1.title, args=[book2], on_click=book_clicked, type="primary")

    #display additional book information
    st.write("")
    st.write(f"**Author:** {book1.author}")
    st.write(f"**Series:** {book1.series}")
    st.write(f"**Year Published:** {book1.year}")
    st.write(f"**Page Count:** {book1.page_count}")
    st.write(f"**Description:** {book1.description}")

with col2:
    # get the full title of the book and store it in a string variable
    book2_title = book2.title

    # Check if the title contains brackets and extract the substring
    # e.g. "Flames of Chaos (Legacy of the Nine Realms, #1)"
    # if '(' in book2_title and ')' in book2_title:
    #     book2_title_only = book2_title.split('(')[0].strip()
    #     series2 = book2_title.split('(')[1].split(')')[0].strip()
    # else:
    #     book2_title_only = book2_title
    #     series2 = "Not Applicable"

    # display the book title and cover
    st.header(book2.title, anchor=False)
    st.image(book2.cover_url['thumbnail'], width=200)

    #if this button is pressed, remove the other displayed book
    st.button(book2.title, args=[book1], on_click=book_clicked, type="primary")

    #display additional book information
    st.write("")
    st.write(f"**Author:** {book2.author}")
    st.write(f"**Series:** {book2.series}")
    st.write(f"**Year Published:** {book2.year}")
    st.write(f"**Page Count:** {book2.page_count}")
    st.write(f"**Description:** {book2.description}")

# Handle the clicked book
if "clicked_book" in st.session_state:
    if st.session_state.clicked_book == book1:
        book_clicked(book2)
    elif st.session_state.clicked_book == book2:
        book_clicked(book1)