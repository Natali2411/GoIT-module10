from __future__ import annotations

import re
from collections import UserDict
from re import Match
from typing import Tuple, Any


class RecordAlreadyExistsException(Exception):
    """
    Custom exception class for catching exceptions in case of the try to add a record
    that already exists in the AddressBook.
    """
    pass


class Field:
    """
    Base class that describes the logic for all types of fields.
    """
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """
    This class is a derived class from Field and needed for storing name of the client.
    """
    def __init__(self, client_name: str):
        super().__init__(value=client_name)


class Phone(Field):
    """
    This class is a derived class from Field and needed for storing phone of the client.
    """
    def __init__(self, phone: str):
        match: Match[bytes] | None = re.search('\d+', phone)
        numbers = match.group() if match else ""
        phone_number_len: int = len(phone)
        if phone_number_len != 10 or len(numbers) != phone_number_len:
            raise ValueError(f"Phone number must have only digits with length "
                             f"10, but number: '{phone}' was given with the "
                             f"length {phone_number_len}")
        super().__init__(value=phone)


class Record:
    """
    This class describes the logic of storing data about the client and all his/her
    phones.
    """
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    def get_phone_by_number(self, phone_num: str) -> Tuple[Any, int] | Tuple[None, None]:
        """
        Method iterates through the list of phone objects and returns the object that
        has 'phone_num' as a phone value.
        :param phone_num: Phone number string.
        :return: Phone object and it's index in the list.
        """
        for idx, phone in enumerate(self.phones):
            if phone.value == phone_num:
                return phone, idx
        return None, None

    def add_phone(self, phone_num: str) -> None:
        """
        Method adds Phone instances into the list of phones for a particular client.
        :param phone_num: Phone number as a string.
        :return: None.
        """
        self.phones.append(Phone(phone=phone_num))

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        """
        Method founds the phone number in a list of other client's numbers and edits
        it if the number was found.
        :param old_phone: The phone that must be changed.
        :param new_phone: The new phone number.
        :return: None.
        """
        found_phone, idx = self.get_phone_by_number(phone_num=old_phone)
        if found_phone:
            self.phones[idx].value = new_phone
        else:
            raise ValueError(
                f"Phone with the number '{old_phone}' was not found for the "
                f"user '{self.name.value}'")

    def remove_phone(self, phone_num: str) -> None:
        """
        Method that removes phone number from the list of client's numbers.
        :param phone_num: Phone number that should be removed.
        :return: None.
        """
        _, idx = self.get_phone_by_number(phone_num=phone_num)
        self.phones.pop(idx)

    def find_phone(self, phone_num: str) -> Phone:
        """
        Method that searches for a phone number and returns a Phone object if the
        number was found.
        :param phone_num: Phone number that should be found.
        :return: The Phone object of found phone number or None.
        """
        found_phone, _ = self.get_phone_by_number(phone_num=phone_num)
        return found_phone


class AddressBook(UserDict):
    """
    Class that describes the logic of saving client's records in the address book and
    making manipulations with the records.
    """

    def add_record(self, record: Record) -> None:
        """
        Method adds Record objects into the address book using client name as a key
        and the object as a value.
        :param record: Record instance that has an information about client name and
        her/his phone numbers.
        """
        if record.name.value not in self.data:
            self.data[record.name.value] = record
        else:
            raise RecordAlreadyExistsException(f"Record with the name '"
                                               f"{record.name.value}' already exists "
                                               f"in the address book dictionary")

    def find(self, name: str) -> Record:
        """
        Method finds records from the address book by client's name.
        :param name: The name of a client.
        :return: Record from the address book for specific client.
        """
        return self.data.get(name)

    def delete(self, name: str) -> None:
        """
        Method deletes the record from the address book for the specific client by
        his/her name.
        :param name: Client's name.
        :return: None.
        """
        if self.data.get(name):
            self.data.pop(name)


if __name__ == "__main__":
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    book.delete("Jane")
