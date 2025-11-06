# GoIT Python Core - Home Work 08: Data Persistence and Final Integration

## Project Overview

This repository implements the final version of the **Console Assistant Bot**, merging the full **Object-Oriented Programming (OOP)** model with **data persistence** to ensure contact data is saved and restored across application sessions.

---

## Repository Structure and Functionality (Solutions)

| Class / Function | Purpose | Key Functionality |
| :--- | :--- | :--- |
| **Classes** | `Field`, `Phone`, `Record`, `AddressBook` | Core OOP structure with **data validation** and **inheritance**. |
| **`save_data()`** | Data Persistence | Uses **`pickle.dump`** to serialize the entire `AddressBook` object to a file (`addressbook.pkl`). |
| **`load_data()`** | Data Restoration | Uses **`pickle.load`** to deserialize and restore the `AddressBook` from the file on startup. |
| **`get_upcoming_birthdays()`** | Date Logic | Calculates birthdays in the next 7 days, including automatic **weekend shift** (Saturday/Sunday → Monday). |
| **Handlers** | `@input_error` | **Universal Decorator:** Protects all commands against `ValueError`, `KeyError`, and `IndexError`. |

---

## Execution Instructions and Commands

| Command | Usage Example | Functionality |
| :--- | :--- | :--- |
| **Start/Restore** | Launch the script | Bot automatically restores data from the persistence file. |
| **`add [Name] [Phone]`** | `add John 1234567890` | Adds a new contact or phone number. |
| **`add-birthday [Name] [Date]`** | `add-birthday John 25.12.1990` | Adds the contact's date of birth (validated). |
| **`birthdays`** | `birthdays` | Displays all contacts to be congratulated in the next week, adjusted for weekends. |
| **`close` / `exit`** | `exit` | **Saves data** using `pickle` and terminates the application. |