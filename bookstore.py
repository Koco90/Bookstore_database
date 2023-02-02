import os
import sqlite3

##########################################################################################################################
                                                    # DATABASE
##########################################################################################################################

# Had to include this to avoid the error: sqlite3.OperationalError: table books already exists
try:
    os.remove('bookstore') 
except OSError:      
	pass

db = sqlite3.connect('bookstore')
# Get a cursor object
c = db.cursor()  

# Create table
c.execute('''CREATE TABLE books 
    (id INTEGER PRIMARY KEY, 
    Title TEXT,
    Author TEXT,
    Qty INTEGER)
''')

db.commit()

c = db.cursor() 

# Inputting all data and saving it as one variable.

many_books = [
                (3001, 'A Tale of Two Cities', 'Charles Dickens', 30),
                (3002, 'Harry Potter and the Philosopher\'s Stone', 'J.K. Rowling', 40),
                (3003, 'The Lion, the Witch and the Wardrobe', 'C.S. Lewis', 25),
                (3004, 'The Lord of the Rings', 'J.R.R. Tolkien', 37),
                (3005, 'Alice in Wonderland', 'Lewis Carroll', 12),
                (3006, 'Northern Lights', 'Philip Pullman', 32),
                (3007, 'The Alchemist', 'Paulo Coelho', 18),
                (3008, 'Famous Five', 'Enid Blyton', 29),
                (3009, 'Eleven Minutes', 'Paulo Coelho', 11)

]

# Inserting the data into the db
c.executemany("INSERT INTO books VALUES (?,?,?,?)", many_books)
db.commit()


##########################################################################################################################
                                                # FUNCTIONS DEFINED
##########################################################################################################################

# Function to Enter book
def enter_book():
    print("\nYou wish to add a new book.\n")
    # Gather info from user
    title = input("What is the title of the book  ")
    # Make sure the user doesn't enter the same book twice by checking the title against the db
    c.execute('''SELECT * FROM books WHERE Title LIKE ?''', (f'%{title}%', ))
    exists = c.fetchall()
    while True: 
        if len(exists) != 0:
            print("This title may already exist, see below:")
            print(exists)
            print("\nDo you still wish to add this book?")
            yes_no = input("y for yes, n for no:  ")
            if yes_no == "y" or yes_no == "Y":
                break
            elif yes_no == "n" or yes_no == "N":
                exit()
            else :
                print("Please type y or n")
                continue
        else :
            break

    author = input("Who is the author of the book  ")
    try:
        qty = int(input("How many copies of the book are in store  "))
    except ValueError:
        print("Please enter an integer")

    c.execute(f'SELECT MAX(id) FROM books')
    id = c.fetchone()[0] + 1
    new_book = (id, title, author, qty)

    c.execute(f'INSERT INTO books VALUES(?, ?, ?, ?)', new_book)
    db.commit()

    return print(f"{title} has been added.\n")


# Function to Update book
def update_book():
    print("\nYou wish to update a book.\n")
    print("Please provide the required information to identify the book to update.")
    
    while True: 
        title_id = input("t for title or i for id: ")
        # ID given to make updates
        if title_id == 'i' or title_id == 'I' :
            id = int(input("What is the book's id: "))
            # Opportunity for user to confirm what they want to update
            c.execute("SELECT * FROM books WHERE id = ?", (id,))
            items = c.fetchall()
            # if id is incorrect
            if len(items) == 0 :
                print("The id does not exist. Try again.")
            # else if id is correct
            else :
                for i in items:
                    print(f"This is what you will be updating:\n{i}")
                print("What would you like to update")
                choice = input("t for title, a for author, q for quantity, x for cancel: ")
                while True:
                    # Given ID, change the Title 
                    if choice == 't' or choice == 'T':
                        new_title = input("What is the updated title: ")
                        c.execute(f"UPDATE books SET Title = ? WHERE id = ?", (new_title, id))
                        db.commit()
                        c.execute("SELECT * FROM books WHERE id = ?", (id,))
                        items = c.fetchall()
                        for i in items:
                            print(f"{i} has been updated.")
                        break
                    # Given ID, change the Author 
                    elif choice == 'a' or choice == 'A':
                        new_author = input("What is the updated author: ")
                        c.execute(f"UPDATE books SET Author = ? WHERE id = ?", (new_author, id))
                        db.commit()
                        c.execute("SELECT * FROM books WHERE id = ?", (id,))
                        items = c.fetchall()
                        for i in items:
                            print(f"{i} has been updated.")
                        break
                    # Given ID, change the quantity
                    elif choice == 'q' or choice == 'Q':
                        new_quant = int(input("What is the updated quantity: "))
                        c.execute(f"UPDATE books SET QTY = ? WHERE id = ?", (new_quant, id))
                        db.commit()
                        c.execute("SELECT * FROM books WHERE id = ?", (id,))
                        items = c.fetchall()
                        for i in items:
                            print(f"{i} has been updated.")
                        break
                    # Option if they decide to change their mind
                    elif choice == 'x' or choice == 'X':
                        break
                    # Way to deal with incorrect entries
                    else : 
                        print("Please type t, a, q or x")
                        continue
                break
        # Title given to make updates
        elif title_id == 't' or title_id == 'T' :
            title = input("What is the book's title: ")
            # Opportunity for user to confirm what they want to update
            c.execute("SELECT * FROM books WHERE Title = ?", (title,))
            items = c.fetchall()
            # if title is incorrect
            if len(items) == 0 :
                print("The title does not exist. Try again.")
            # else if title is correct
            else :
                for i in items:
                    print(f"This is what you will be updating:\n{i}")
                print("What would you like to update")
                # Will not give the choice to update id as it won't add anything useful
                choice = input("t for title, a for author, q for quantity, x for cancel: ")
                while True:
                    # Given Title, change the Title 
                    if choice == 't' or choice == 'T':
                        new_title = input("What is the updated title: ")
                        c.execute(f"UPDATE books SET Title = ? WHERE Title = ?", (new_title, title))
                        db.commit()
                        c.execute("SELECT * FROM books WHERE Title = ?", (new_title,))
                        items = c.fetchall()
                        for i in items:
                            print(f"{i} has been updated.")
                        break
                    # Given Title, change the Author 
                    elif choice == 'a' or choice == 'A':
                        new_author = input("What is the updated author: ")
                        c.execute(f"UPDATE books SET Author = ? WHERE Title = ?", (new_author, title))
                        db.commit()
                        c.execute("SELECT * FROM books WHERE Title = ?", (title,))
                        items = c.fetchall()
                        for i in items:
                            print(f"{i} has been updated.")
                        break
                    # Given Title, change the Quantity
                    elif choice == 'q' or choice == 'Q':
                        new_quant = int(input("What is the updated quantity: "))
                        c.execute(f"UPDATE books SET QTY = ? WHERE Title = ?", (new_quant, title))
                        db.commit()
                        c.execute("SELECT * FROM books WHERE Title = ?", (title,))
                        items = c.fetchall()
                        for i in items:
                            print(f"{i} has been updated.")
                        break
                    # Option if they decide to change their mind
                    elif choice == 'x' or choice == 'X':
                        break
                    # Way to deal with incorrect entries
                    else : 
                        print("Please type t, a, q or x")
                        continue
                break
        # Way to deal with incorrect entries
        else : 
            print("Please type t or i")
            continue


# Function to Delete book
def delete_book():
    print("\nYou wish to delete a book.\n")
    print("Please provide the required information to identify the book to delete.")
    
    while True: 
        title_id = input("t for title or i for id: ")
        # ID given to delete
        if title_id == 'i' or title_id == 'I' :
            id = int(input("What is the book's id: "))
            c.execute("SELECT * FROM books WHERE id = ?", (id,))
            items = c.fetchall()
            # if id is incorrect
            if len(items) == 0 :
                print("The id does not exist. Try again.")
            # else if id is correct
            else :
                for i in items:
                    print(f"This is what you will be deleting:\n{i}")
                print("Are you sure you want to delete?")
                choice = input("y for delete or n to cancel: ")
                while True:
                    # If they confirm they want to delete
                    if choice == 'y' or choice == 'Y':
                        c.execute("DELETE FROM books WHERE id = ?", (id,))
                        print("Deleted.")
                        break
                    elif choice == 'n' or choice == 'N':
                        break
                    else : 
                        print("Please type y or n")
                        continue
                break
        # Title given to delete
        elif title_id == 't' or title_id == 'T' :
            title = input("What is the book's title: ")
            c.execute("SELECT * FROM books WHERE Title = ?", (title,))
            items = c.fetchall()
            # if title is incorrect
            if len(items) == 0 :
                print("The title does not exist. Try again.")
            # else if title is correct
            else :
                for i in items:
                    print(f"This is what you will be deleting:\n{i}")
                print("Are you sure you want to delete?")
                choice = input("y for delete or n to cancel: ")
                while True:
                    # If they confirm they want to delete
                    if choice == 'y' or choice == 'Y':
                        c.execute("DELETE FROM books WHERE Title = ?", (title,))
                        print("Deleted.")
                        break
                    elif choice == 'n' or choice == 'N':
                        break
                # Way to deal with incorrect entries
                    else : 
                        print("Please type y or n")
                        continue
                break
        # Way to deal with incorrect entries
        else : 
            print("Please type t or i")
            continue


# Function to Search a book
def search_book():
    print("\nYou wish to search for a book.\n")
    print("Please provide the required information to identify the book you are looking for.")
    
    while True: 
        title_id = input("t for title, i for id or a for author: ")
        # ID given to search
        if title_id == 'i' or title_id == 'I' :
            id = int(input("What is the book's id: "))
            c.execute("SELECT * FROM books WHERE id = ?", (id,))
            items = c.fetchall()
            # if id is incorrect
            if len(items) == 0 :
                print("The id does not exist. Try again.")
            # else if id is correct
            else :
                print("Here are the book/s:\n")
                for i in items:
                    print(i)
                break
        # Title given to search
        elif title_id == 't' or title_id == 'T' :
            title = input("What is the book's title: ")
            c.execute('''SELECT * FROM books WHERE Title LIKE ?''', (f'%{title}%', ))
            items = c.fetchall()
            # if title is incorrect
            if len(items) == 0 :
                print("The title does not exist. Try again.")
            # else if title is correct
            else :
                print("Here are the book/s:\n")
                for i in items:
                    print(i)
                break
        # Author given to search
        elif title_id == 'a' or title_id == 'A' :
            author = input("Author's full name: ")
            # Use the like command to cover similar named items
            c.execute('''SELECT * FROM books WHERE Author LIKE ?''', (f'%{author}%', ))
            # c.execute("SELECT * FROM books WHERE Author = ?", (author,))
            items = c.fetchall()
            # if author is incorrect
            if len(items) == 0 :
                print("The author does not exist. Try again.")
            # else if title is correct
            else :
                print("Here are the book/s:\n")
                for i in items:
                    print(i)
                break
        # Way to deal with incorrect entries
        else : 
            print("Please type t or i or a")
            continue

# Function to View all the books in the db
def view_all() :
    print("\nYou wish to view all the books:\n")
    c.execute("SELECT * FROM books")
    items = c.fetchall()
    for i in items:
        print(i)



##########################################################################################################################
                                            # MAIN MENU AND OPTIONS
##########################################################################################################################

# While loop to keep the db avaiable for the clerk
while True:
# Introductory message
    print('''
Welcome to your book management service

Please select from the following options by inputting the corresponding number:
1. Enter a new book to the database
2. Update details of a book
3. Delete a book
4. Search a book
5. View all books
6. Exit
''')
    # try and except to deal with any incorrect entries.
    try:
        option = int(input("Option:"))
    except ValueError:
        print("Please enter an integer between 1 and 5")
        continue

    # Enter a new book to the database
    if option == 1 :
        enter_book()
    
    elif option == 2 :
        update_book()

    elif option == 3 :
        delete_book()

    elif option == 4 :
        search_book()

    elif option == 5 :
        view_all()

    elif option == 6 :
        exit()

    # Way to deal with incorrect entries
    else: 
        print("Please enter an integer between 1 and 5.")