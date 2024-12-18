import random
import streamlit as st
from st_clickable_images import clickable_images


st.title("2 Books from Book List")

# implement logic to remove 1 book from book_comparisons before uncommenting this line
# while len(st.session_state.book_comparisons) > 1:

# Randomly select two books
book1, book2 = random.sample(st.session_state.book_comparisons, 2)

# Create two columns to display the books side by side
col1, col2 = st.columns(2)


#clickable_images(paths,titles=[], div_style={}, img_style={}, key=None)

with col1:
    st.header(book1.title)
    clicked1 = clickable_images(
        [book1.cover_url['thumbnail']],
        titles=[book1.title],
        div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
        img_style={"margin": "5px", "height": "200px"} )
    st.write(f"**Author:** {book1.author}")
    st.write(f"**ISBN-10:** {book1.isbn10}")
    st.write(f"**ISBN-13:** {book1.isbn13}")
    st.write(f"**Year:** {book1.year}")
    st.write(f"**Page Count:** {book1.page_count}")
    st.write(f"**Description:** {book1.description}")

with col2:
    st.header(book2.title)
    clicked2 = clickable_images(
        [book2.cover_url['thumbnail']],
        titles=[book2.title],
        div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
        img_style={"margin": "5px", "height": "200px"})
    st.write(f"**Author:** {book2.author}")
    st.write(f"**ISBN-10:** {book2.isbn10}")
    st.write(f"**ISBN-13:** {book2.isbn13}")
    st.write(f"**Year:** {book2.year}")
    st.write(f"**Page Count:** {book2.page_count}")
    st.write(f"**Description:** {book2.description}")

st.markdown(f"Image #{clicked1} clicked in column 1" if clicked1 > -1 else "No image clicked in column 1")
st.markdown(f"Image #{clicked2} clicked in column 2" if clicked2 > -1 else "No image clicked in column 2")
