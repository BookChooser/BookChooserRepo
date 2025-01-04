import streamlit as st

#Define screens and navigation menu
upload_screen = st.Page("screens/UploadScreen.py", title="Book Tournament Upload Screen")
selector_screen = st.Page("screens/SelectorScreen.py", title="Book Tournament Selector Screen")
winner_screen = st.Page("screens/WinnerScreen.py", title="Book Tournament Winner Screen")

pg = st.navigation([upload_screen, selector_screen, winner_screen], position="hidden")
pg.run()


