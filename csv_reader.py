# This program reads test scores from a CSV file
# and calculates each student's test average.
from matplotlib import lines
import re

def main():
    # Open the file.
    csv_file = open('booklist.csv', 'r')

    # Read the file's lines into a list.
    lines = csv_file.readlines()

    # Close the file.
    csv_file.close()

    # Process the lines.
    #for line in lines[1:]:
    for line in lines:
        # Get the book as tokens.
        modified_line = re.sub(r',(?=\S)', '|', line)

        book= modified_line.split('|')

        isbn = book[6]
        print(isbn)


        # get the isbn
        #for attributes in book:
        #    print(attributes)






# Execute the main function.
if __name__ == '__main__':
    main()
