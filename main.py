from collections import UserDict
from datetime import datetime, timedelta
import pickle
import sys

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook() 
    
# --- CORE CLI HANDLERS AND DECORATOR ---

def input_error(func):
    """Decorator to handle common input errors (ValueError, IndexError, KeyError)."""
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            # Catches incorrect number of arguments
            return "Please enter name and phone or date please."
        except IndexError:
            # Catches access to a non-existent argument
            return "Please enter user name or required argument."
        except KeyError:
            # Catches attempt to access a non-existent contact
            return "Contact not found."
    return inner

def parse_input(user_input):
    """Parses user input into command and arguments."""
    parts = user_input.split()
    if not parts:
        return "", []
    cmd = parts[0].strip().lower()
    args = parts[1:]
    return cmd, args

# --- HANDLER FUNCTIONS ---

@input_error
def add_contact(args, book):
    """Adds a new contact record or a new phone number to an existing record."""
    name, phone, *_ = args
    
    try:
        # Try to find existing record
        record = book.find(name)
        record.add_phone(phone)
        return "Contact updated (phone added)."
    except KeyError:
        # If not found, create a new record
        record = Record(name)
        book.add_record(record)
        record.add_phone(phone)
        return "Contact added."

@input_error
def change_contact(args, book):
    """Changes an existing phone number for a contact."""
    name, old_phone, new_phone, *_ = args
    
    record = book.find(name)
    # edit_phone handles ValueError if phone numbers are invalid
    record.edit_phone(old_phone, new_phone)
    return "Contact updated (phone changed)."

@input_error
def show_phone(args, book):
    """Shows all phone numbers for a specific contact"""
    name = args[0]
    record = book.find(name)
    # Returns Record.__str__ output
    return str(record) 

def show_all(book):
    """Shows all saved contacts in the address book."""
    records = [str(record) for record in book.data.values()]
    if not records:
        return "No contacts saved."
    return '\n'.join(records)

@input_error
def add_birthday(args, book):
    """Adds a birthday date to an existing contact."""
    name, birthday = args
    record = book.find(name)
    # add_birthday handles ValueError if date format is invalid
    record.add_birthday(birthday)
    return "Birthday added."

@input_error
def show_birthday(args, book):
    """Shows the birthday date for a specific contact."""
    name = args[0]
    record = book.find(name)
    if record.birthday is None:
        return f"Birthday information is not available for {record.name.value}."
    else:
        # Use strftime to format the date object
        return f"{record.name.value}'s birthday: {record.birthday.value.strftime('%d.%m.%Y')}"
    
@input_error
def birthdays(args, book):
    """Returns a list of contacts with upcoming birthdays in the next week."""
    upcoming_birthdays = book.get_upcoming_birthdays()
    if not upcoming_birthdays:
        return "No birthdays upcoming next week."
    output_lines = ["Upcoming birthdays:"]
    for item in upcoming_birthdays:
        output_lines.append(f"{item['name']}: {item['congratulation_date']}")
    return "\n".join(output_lines)


# ---------------------------------------
# CORE LOGIC: CLASSES
# ---------------------------------------

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass
           
class Phone(Field):
    def __init__(self, value):
        if len(value) != 10 or not value.isdigit():
            raise ValueError("Phone number must be exactly 10 digits.")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            date = datetime.strptime(value, "%d.%m.%Y").date()
            super().__init__(date)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone_number):
         phone = Phone(phone_number)
         self.phones.append(phone)
    
    def remove_phone(self, phone_number):
        for p in self.phones[:]:
            if p.value == phone_number:
                self.phones.remove(p)
                return "Phone removed successfully."
        raise ValueError(f"Phone number '{phone_number}' not found in contact.")
    
    def find_phone(self, phone_number):
        for p in self.phones[:]:
            if p.value == phone_number:
                return p
        raise ValueError(f"Phone number '{phone_number}' not found in contact.")
    
    def edit_phone(self, old_number, new_number):
        found_phone_object = self.find_phone(old_number)
        Phone(new_number) 
        found_phone_object.value = new_number
        return "Phone updated successfully."
    
    def add_birthday(self, date_str):
        birthday = Birthday(date_str)
        self.birthday = birthday
    
    def __str__(self):
        # Displays name and all phones, checking if birthday is set
        birthday_info = f", birthday: {self.birthday.value.strftime('%d.%m.%Y')}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}{birthday_info}"


class AddressBook(UserDict):
    def add_record(self, record):
        user_name = record.name.value
        self.data[user_name] = record

    def find(self, name):
        return self.data[name]
    
    def delete(self, name):
        del self.data[name]

    def get_upcoming_birthdays(self):
        upcoming_birthdays = [] 
        today = datetime.today().date()
        for record in self.data.values():
            if record.birthday is None:
                continue
            user_birthday = record.birthday.value
            birthday_this_year = user_birthday.replace(year=today.year) 
            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)
            days_difference = (birthday_this_year - today).days
            if 0 <= days_difference <= 6:
                congrat_date = birthday_this_year
                if congrat_date.weekday() == 5: 
                    congrat_date = congrat_date + timedelta(days=2)
                elif congrat_date.weekday() == 6: 
                    congrat_date = congrat_date + timedelta(days=1)
                congrat_date_str = congrat_date.strftime("%d.%m.%Y")
                upcoming_birthdays.append({"name": record.name.value, "congratulation_date": congrat_date_str })      
        return upcoming_birthdays

# -------------------------------------------------------------
# MAIN CLI LOOP
# -------------------------------------------------------------

def main():
    # Initialize the AddressBook object
    book = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        try:
            command, *args = parse_input(user_input)
        except ValueError:
            command = "" 
        if not command:
            continue

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            # Using show_all function to display all contacts
            print(show_all(book)) 
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))
        else:
            print("Invalid command.")
        save_data(book)

if __name__ == "__main__":
    main()