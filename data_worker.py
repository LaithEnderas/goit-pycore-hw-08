import pickle
from classes import AddressBook

ADDRESS_BOOK_FILE = "addressbook.pkl"

def save_data(book, filename=ADDRESS_BOOK_FILE):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename=ADDRESS_BOOK_FILE):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()
