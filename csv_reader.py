# This program reads test scores from a CSV file
# and calculates each student's test average.
from matplotlib import lines


def main():
    # Open the file.
    csv_file = open('booklist.csv', 'r')

    # Read the file's lines into a list.
    lines = csv_file.readlines()

    # Close the file.
    csv_file.close()

    # Process the lines.
    for line in lines:
        # Get the test scores as tokens.
        tokens = line.split(',')
        print(tokens)






# Execute the main function.
if __name__ == '__main__':
    main()
