# This program reads test scores from a CSV file
# and calculates each student's test average.
from matplotlib import lines
import re
from isbnlib import meta, desc, cover, isbn_from_words
from isbnlib.registry import bibformatters

SERVICE = "openl"


def main():
    # Open the file.
    csv_file = open('booklist.csv', 'r')

    # Read the file's lines into a list.
    lines = csv_file.readlines()

    # Close the file.
    csv_file.close()

    bibtex = bibformatters["bibtex"]

    # Process the lines.
    for line in lines[1:]:
        # Get the book as tokens.
        modified_line = re.sub(r',(?=\S)', '|', line)

        book = modified_line.split('|')

        #choose isbn and replace " and =
        isbn = book[5]
        isbn13 = book[6]
        author = book[2]

        isbn = re.sub(r'[\"=]', '', isbn)
        isbn13 = re.sub(r'[\"=]', '', isbn13)

        # Retrieve metadata using ISBN, ISBN-13, or fallback to author.
        if isbn:
            try:
                print("BibTeX:", bibtex(meta(isbn, SERVICE)))
                print("Description:", desc(isbn))
                print("Cover:", cover(isbn), "\n")
            except Exception as e:
                print(f"Error retrieving data for ISBN {isbn}: {e}\n")

        elif isbn13:
            try:
                print("BibTeX:", bibtex(meta(isbn13, SERVICE)))
                print("Description:", desc(isbn13))
                print("Cover:", cover(isbn13), "\n")
            except Exception as e:
                print(f"Error retrieving data for ISBN-13 {isbn13}: {e}\n")

        else:
            # Fallback to author if both ISBN and ISBN-13 are missing.
            print(f"Author: {author}\n")













# Execute the main function.
if __name__ == '__main__':
    main()
