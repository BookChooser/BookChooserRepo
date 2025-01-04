# BookTournament Project

An app that helps the user choose their next book from an exported Goodreads list. 

Run by typing "streamlit run BookTournament.py" in terminal
class getting some metadata, a description and cover incl thumbnail from isbnlib
Important: input ISBN13 (not ISBN10)

Steps needed for it to work:
1. add a local virtual environment for the project
2. install pip: right-click project, open in Terminal. In terminal type:  py -m ensurepip --upgrade
3. install isbnlib: in terminal type: pip install isbntools
4. upgrade setuptools: in terminal type: pip install --upgrade setuptools