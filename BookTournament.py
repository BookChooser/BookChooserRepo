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
from isbnlib import meta, desc, cover
from isbnlib.registry import bibformatters

SERVICE = "openl"

# now you can use the service
isbn = "9780553572988"
bibtex = bibformatters["bibtex"]
print(bibtex(meta(isbn, SERVICE)))
print("description: ", desc(isbn))
print("cover: ", cover(isbn))