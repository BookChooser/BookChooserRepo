import streamlit as st
from BookTournament import upload_screen
from Style import load_css

load_css()
st.markdown("<h1 style='text-align: center;', class='title'>The winner is:</h1>", unsafe_allow_html=True)

col1, col2 = st.columns(2, vertical_alignment="top")

for book in st.session_state.book_comparisons:

    with col1:
        st.write("")
        st.image(book.cover_url['thumbnail'], width=200)
    with col2:
        st.header(book.title, anchor=False)
        st.write(f"**Author:** {book.author}")
        st.write(f"**Series:** {book.series}")
        st.write(f"**ISBN-10:** {book.isbn10}")
        st.write(f"**ISBN-13:** {book.isbn13}")
        st.write(f"**Year:** {book.year}")
        st.write(f"**Page Count:** {book.page_count}")
        st.write(f"**Description:** {book.description}")

    st.balloons()

col3, col4, col5 = st.columns(3)

with col4:
    if st.button('Again?', type="primary", icon=":material/repeat:"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.switch_page(upload_screen)