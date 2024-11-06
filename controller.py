import re



def store_lines():
    # Open the file.
    csv_file = open('booklist.csv', 'r')

    # Read the file's lines into a list.
    lines = csv_file.readlines()

    # Close the file.
    csv_file.close()



    # Process the lines.
    for line in lines[1:]:
        # Get the book as tokens.
        modified_line = re.sub(r',(?=\S)', '|', line)

        book = modified_line.split('|')
        print(book)
