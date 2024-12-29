"""
update 11 Nov 24: currently this class is most recent together with Book.py and pages in "pages" folder.
Run by typing "streamlit run BookTournament.py" in terminal

class getting some metadata, a description and cover incl thumbnail from OpenLibrary.org api
(also possible to get from Google Books or Wikipedia apis)
Important: input ISBN13 (not ISBN10)

Steps needed for it to work:
1. add a local virtual environment for the project
2. install pip: right-click project, open in Terminal. In terminal type:  py -m ensurepip --upgrade
3. install isbnlib: in terminal type: pip install isbntools
4. upgrade setuptools: in terminal type: pip install --upgrade setuptools
"""
import streamlit as st
import pandas as pd
import re
from isbnlib import desc, cover, isbn_from_words

from Book import Book
import random

#Define pages and navigation menu
upload_screen = st.Page("pages/UploadScreen.py", title="Book Tournament Upload Screen")
selector_screen = st.Page("pages/SelectorScreen.py", title="Book Tournament Selector Screen")
winner_screen = st.Page("pages/WinnerScreen.py", title="Book Tournament Winner Screen")

#TODO: add ", position="hidden"" between ] and ) to hide the navigation:
pg = st.navigation([upload_screen, selector_screen, winner_screen], position="hidden")
pg.run()


