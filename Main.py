from controller import BookController

def main():
    controller = BookController()

    while True:
        print("\n1. Add Book\n2. Display Books\n3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            controller.add_book()
        elif choice == "2":
            controller.display_books()
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()