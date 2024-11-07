
class Book:
    def __init__(self, title, author, isbn10, isbn13, year, page_count, description, cover_url):
        self.title = title
        self.author = author
        self.isbn10 = isbn10
        self.isbn13 = isbn13
        self.year = year
        self.page_count = page_count
        self.description = description
        self.cover_url = cover_url


    def __str__(self):
        return f"{self.title}, {self.author}, {self.isbn10}, {self.isbn13}, {self.year}, {self.page_count}, {self.description}, {self.cover_url}"
"""
TODO: 
getters, setters for all attributes  
"""
