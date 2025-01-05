# BookTournament

An app that helps the user choose their next book from their exported Goodreads library, 
by allowing the user to compare two books with each other and selecting the preferred one 
until only one book is left and the winner is found. 
The app displays metadata from the Goodreads Library and from isbnlib to support the user's decision.

## Download Goodreads Library
1. Go to https://www.goodreads.com/review/import and log in
4. Select 'Export Library', and click the download link once available
5. Run the BookTournament app and upload the exported library

## Steps needed to run the app locally
1. Install pip: py -m ensurepip --upgrade
2. Install isbnlib: pip install isbntools
3. Upgrade setuptools: pip install --upgrade setuptools
4. Install streamlit: pip install streamlit 
5. Type "streamlit run BookTournament.py" in terminal

## Run deployed app
https://huggingface.co/spaces/Alex-02/book-tournament

