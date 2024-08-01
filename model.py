from classes import *
from data_worker import save_data, load_data

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return "Expect one argument"
        except ValueError:
            return "Expect two or more arguments"
        except KeyError:
            return "No such name in contacts"
    return inner

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, contacts: AddressBook):
    name, phone, *_ = args
    record = contacts.find(name)
    try: 
        if record == None:
            new_record = Record(name)
            new_record.add_phone(phone)
            contacts.add_record(new_record)
        else:
            record.add_phone(phone)
        return "Contact added"
    except Exception as e:
        return e

@input_error
def change_contact(args, contacts: AddressBook):
    name, old_phone, new_phone, *_ = args
    record = contacts.find(name)
    if record == None:
        return "Contact not exist, add it"
    try:
        result = record.edit_phone(old_phone, new_phone)
    except Exception as e:
        return e
    output = "Contact changed" if result else "Not found number to change"
    return output

@input_error
def single_phone(args, contacts: AddressBook):
    name = args[0]
    record = contacts.find(name)
    if record == None:
        return "No such contact"
    return str(record)

def all_phones(contacts: AddressBook):
    if not contacts.data:
        return ["Contacts is empty"]
    result = []
    for record in contacts.data.values():
        result.append(str(record))
    return result

@input_error
def add_birthday(args, contacts: AddressBook):
    name, date, *_ = args
    record = contacts.find(name)
    if record == None:
        return "No such contact"
    if record.birthday != None:
        return "Birthday already added"
    try:
        record.add_birthday(date)
        return "Bidthday date added"
    except ValueError as e:
        return e
    
@input_error
def show_birthday(args, contacts: AddressBook):
    name = args[0]
    record = contacts.find(name)
    if record == None:
        return "No such contact"
    if record.birthday == None:
        return "No birthday info about contact"
    return "Birthday for " + record.name.value + " at: " + record.birthday.value.strftime("%d %B")

def birthdays(contacts: AddressBook):
    data = contacts.get_upcoming_birthdays()
    if not data:
        return "No one have birthdays this week"
    output = "You need to congratulate: "
    for index, row in enumerate(data):
        output += row['name'] + " on " + row["congratulation_date"]
        if index < len(data) - 1:
            output += ", "
    return output

def main():
    contacts = load_data()
    commands = [
        "close", 
        "exit", 
        "hello", 
        "add [username] [phone]", 
        "change [username] [old_phone] [new_phone]", 
        "phone [username]", 
        "all",
        "add-birthday [ім'я] [дата народження]",
        "show-birthday [ім'я]",
        "birthdays"
    ]
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        try: 
            command, *args = parse_input(user_input)
        except ValueError:
            command = ''

        if command in ["close", "exit"]:
            save_data(contacts)
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(single_phone(args, contacts))
        elif command == "all":
            print("\n".join(all_phones(contacts)))
        elif command == "add-birthday":
            print(add_birthday(args, contacts))
        elif command == "show-birthday":
            print(show_birthday(args, contacts))
        elif command == "birthdays":
            print(birthdays(contacts))
        else:
            print("Invalid command. Available commands:\n   ", "\n    ".join(commands))
