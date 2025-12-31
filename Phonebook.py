
class Contact:
    def __init__(self,name,number):
        self.name =name
        self.number = number



class TrieNode:
    def __init__(self):
        self.children ={}
        self.isEnd = False
        self.contacts = set()

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert_contact(self,contact:Contact):
        node = self.root
        for char in contact.name:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            node.contacts.add(contact)
        node.isEnd = True


    def contact_suggestions(self,prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return "No contacts found"
            node = node.children[char]
        contacts = node.contacts
        return list(contacts)

class PhoneBook:

    def __init__(self,user):
        self.user =user
        self.trie = Trie()

    def get_user(self):
        return self.user

    def add_contact(self,contact:Contact):
        self.trie.insert_contact(contact)
        self.trie.insert_contact(contact)

    def get_suggestions(self,prefix):
        contacts = self.trie.contact_suggestions(prefix)
        if not contacts:
            print("No contacts")
        for contact in contacts:

            print(f"Name:{contact.name}\n"
                  f"Number:{contact.number}")
            print("------------------------")


phone_book = PhoneBook("Mitra varun")
print(f"Welcome to {phone_book.get_user()} PhoneBook")
phone_book.add_contact(Contact("Prabhas",9978345731))
phone_book.add_contact(Contact("Pratapsingh",9912395085))
phone_book.add_contact(Contact("Alexander",3423543523))
phone_book.add_contact(Contact("Alexhales",34234534))
phone_book.add_contact((Contact("Alexpual",32423423523456)))

phone_book.get_suggestions("Pra")