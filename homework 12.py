import pickle
from collections import UserDict
from datetime import datetime, timedelta

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        super().__init__(value.strip())

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must contain exactly 10 digits")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            parsed_date = datetime.strptime(value, "%d.%m.%Y")
            super().__init__(parsed_date)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        try:
            new_phone = Phone(phone)
            self.phones.append(new_phone)
        except ValueError as e:
            print(f"Failed to add phone number: '{phone}'. {e}")

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                try:
                    phone.value = Phone(new_phone).value
                    print(f"Phone '{old_phone}' was changed to '{new_phone}'")
                    return
                except ValueError as e:
                    print(f"Phone change error: {e}")
                    return
        print(f"Phone '{old_phone}' not found in contact {self.name.value}")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def delete_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                print(f"Phone '{phone}' deleted")
                return
        print(f"Phone '{phone}' not found")

    def add_birthday(self, birthday_str):
        try:
            self.birthday = Birthday(birthday_str)
        except ValueError as e:
            raise ValueError(f"Invalid birthday format: {e}")

    def show_birthday(self):
        if self.birthday:
            return str(self.birthday)
        return "No birthday set"

    def __str__(self):
        phones_str = "; ".join(str(p) for p in self.phones) if self.phones else "No phones"
        return f"Contact name: {self.name.value}, phones: {phones_str}"

class AddressBook(UserDict):
    def __init__(self):
        super().__init__()

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            print(f"Contact '{name}' deleted")
        else:
            print(f"Contact '{name}' not found")

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Please provide name and phone number."
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Please enter a name."
    return inner

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone = args
    record = book.find(name)
    if not record:
        raise KeyError
    record.edit_phone(old_phone, new_phone)
    return "Phone number changed."

@input_error
def phone_username(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if not record:
        raise KeyError
    phones = ", ".join(p.value for p in record.phones)
    return f"{name}'s phone numbers: {phones}"

@input_error
def add_birthday(args, book: AddressBook):
    name, birthday_str, *_ = args
    record = book.find(name)
    if not record:
        return f"Contact '{name}' not found."
    record.add_birthday(birthday_str)
    return f"Birthday added for '{name}'."

@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if not record:
        return f"Contact '{name}' not found."
    return f"{name}'s birthday is: {record.show_birthday()}"

@input_error
def birthdays(args, book: AddressBook):
    today = datetime.today()
    next_week = today + timedelta(days=7)
    upcoming = []

    for record in book.data.values():
        if record.birthday:
            bday = record.birthday.value.replace(year=today.year)
            if today <= bday <= next_week:
                upcoming.append(f"{record.name.value}: {record.birthday}")

    if upcoming:
        return "Birthdays in the upcoming week:\n" + "\n".join(upcoming)
    return "No birthdays this week."

def main():
    book = load_data()  # Завантаження з файлу при запуску
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book) 
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(phone_username(args, book))
        elif command == "all":
            print(book if book.data else "The contact list is empty.")
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
