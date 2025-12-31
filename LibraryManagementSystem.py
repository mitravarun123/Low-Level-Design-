# Design and implement a Library Management system that caters to its registered members by cataloging and housing books that can be borrowed.
#
# Core Requirements:
# The system must provide the following functionalities:
#
# Add books to the catalog: Every book will be added by name and author and the program must generate a unique id for it by joining the first three letters of the author’s last name to a number to create a unique key. For example, a book by Rowling would have ROW1234 as a unique Id. Also, note that the library can have more than one copy for a book.
# Register and unregister users in the Library
# Reservation Management system: A user should be able to make a request to borrow a book from the library.
# Users can borrow books by the book id (eg - ROW1234). For the scope of problems, let's assume users are aware of book id’s.
# If the book is available and not borrowed by anyone, it should be reserved to the member’s name.
# If the book is already borrowed by another user, the reservation system must add the requesting member to a FIFO waitlist of reservations. When the book is returned to the library, it will not be marked as available and will be available only to the first user under the FIFO queue
# If the user is the first user of the FIFO waitlist, the book can be reserved under the user’s name
# Fine calculation system: A user is allowed to borrow a book only for 14 days. If this time limit is exceeded at the time of return, the system should calculate a fine of 20 rupees per day for the number of days delay.
# Good To Have (Bonus):
# One user should only be allowed to reserve one copy of the book
# Auditing: Design should cater to following use cases:
# Given a bookId, give a list of users having that book
# Given a userId, list of books issued to him
import random

class IdGenerator:
    def __init__(self,title):
        self.title = title
        self.randint = random.randint(1,10000)

    def generate_id(self,title):
        return self.title[:2]+str(self.randint)

class Book:
    def __int__(self,title,author,users,istaken,id):
        self.id = IdGenerator.generate_id(title)
        self.title = title
        self.author = author
        self.users = []
        self.istaken = False



class User:
    def __init__(self,name,id,book_list):
        self.name = name
        self.id = id
        self.book_list = book_list


class Catalog:
    def __init__(self):
        self.books = []

    def add_book(self,book:Book):
        self.books.append(Book)

    def search_book(self,title):
        for book in self.books:
            if book.title==title:
                return book
        raise ValueError("There is no such book")

    def list_books(self):
        for book in self.books:
            print(f"{book.title} {book.author}")
            print("----------------------------")




class Library:
    def __init__(self):
        self.users = []

    def add_user(self,user:User):
        self.users.append(user)

    def remove_user(self,user_name):
        for user in self.users:
            if user.name == user_name:
                self.users.remove(user)
        print("There is no such user")

