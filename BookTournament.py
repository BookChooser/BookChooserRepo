"""
class getting some metadata, a description and cover incl thumbnail from OpenLibrary.org api
(also possible to get from Google Books or Wikipedia apis)
Important: input ISBN13 (not ISBN10)

Steps needed for it to work:
1. add a local virtual environment for the project
2. install pip: right-click project, open in Terminal. In terminal type:  py -m ensurepip --upgrade
3. install isbnlib: in terminal type: pip install isbntools
4. upgrade setuptools: in terminal type: pip install --upgrade setuptools
"""
from isbnlib import meta, desc, cover, isbn_from_words
from isbnlib.registry import bibformatters

SERVICE = "openl"

# now you can use the service
isbn1 = "9780553572988"
bibtex = bibformatters["bibtex"]
print(bibtex(meta(isbn1, SERVICE)))
print("description: ", desc(isbn1))
print("cover: ", cover(isbn1),"\n")

isbn2 = isbn_from_words("Working for Bigfoot")
print(bibtex(meta(isbn2, SERVICE)))
print("description: ", desc(isbn2))
print("cover: ", cover(isbn2))
