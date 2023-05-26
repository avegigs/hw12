from collections import UserDict
from datetime import datetime
import re
from pathlib import Path
import pickle


class AddressBook:
    def __init__(self, filename='book.bin'):
        self.records = {}
        self.last_record_id = 0
        self.file = Path(filename)
        self.deserialize()

    def add_record(self, record):
        key = record.name.value
        self.records[key] = record
        # self.records[self.last_record_id] = record
        record.id = self.last_record_id
        self.last_record_id += 1

    def search(self, search_str):
        result = []
        for name, record in self.records.items():
            if (search_str in str(name)) or (search_str in str(record)):
                result.append(f'Found. {record}')
        return result

    def serialize(self):
        with open(self.file, "wb") as file:
            pickle.dump((self.last_record_id, self.records), file)

    def deserialize(self):
        if not self.file.exists():
            return None
        with open(self.file, "rb") as file:
            self.last_record_id, self.records = pickle.load(file)

    # def show_record(self, rec_id):
    #     return f'{self.records[rec_id]}\n'

    def show_records(self, size: int):
        counter = 0
        result = ""
        for record in self.records.values():
            result += f'{str(record)} \n'
            counter += 1
            if counter == size:
                yield result
                counter = 0
                result = ""

        yield result

    def __str__(self) -> str:
        return str(self.records)

    # def search(self, search_string):
    #     search_result = []
    #     for record in self.data.values():
    #         if search_string in record.name.value:
    #             search_result.append(record)
    #         else:
    #             for phone in record.phones:
    #                 if search_string in phone.value:
    #                     search_result.append(record)
    #                     break
    #     return search_result


class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return self.value


class Name(Field):

    def __init__(self, value):
        self.value = value
    # def __init__(self, name):
    #     self.value = name
    #     self.name = name

    # def __str__(self) -> str:
    #     return self.name

    # def __repr__(self) -> str:
    #     return self.name


class Phone(Field):

    def __init__(self, value):
        self.value = value

    @Field.value.setter
    def value(self, value):
        if not re.match(r'^\+38\d{10}$', value):
            raise ValueError(
                "Phone number should be in the format +380XXXXXXXXX")
        Field.value.fset(self, value)

    def __str__(self) -> str:
        return self.__value

    def __repr__(self) -> str:
        return self.value

        # @Private.value.setter
    # def value(self, value):
    #     if not isinstance(value, int):
    #         raise Exception(f"'{value}' is not a valid")
    #     Private.value.fset(self, value)


class Birthday(Field):

    @Field.value.setter
    def value(self, value):
        self.__value = datetime.strptime(value, '%d.%m.%Y').date()
        Field.value.fset(self, value)

    def __str__(self) -> str:
        return datetime.strftime(self.__value, '%d.%m.%Y')

    def __repr__(self) -> str:
        return datetime.strftime(self.__value, '%d.%m.%Y')


class Record:
    def __init__(self, name: Name, birthday: Birthday = None):
        self.birthday = birthday
        self.name = name

        self.phones = []

    def __str__(self) -> str:
        return f'User {self.name} have phone nymbers: {self.phones}'

    def __repr__(self) -> str:
        return f'{self.phones}'

    def add_phone(self, phone: Phone):
        self.phones.append(phone.value)

    def remove_phone(self, phone):
        self.phones.remove(phone)

    def edit_phone(self, old_phone, new_phone):
        index = self.phones.index(old_phone)
        self.phones[index] = new_phone

    # def get_name(self):
    #     return self.name.value

    def get_phone(self, old_phone):
        for phone in self.phones:
            if phone == old_phone:
                return phone
            else:
                return None

    def days_to_birthday(self):
        if not self.birthday:
            return None
        now = datetime.now().date()
        birth = datetime.strptime(str(self.birthday), '%d.%m.%Y').date()
        if (birth.replace(year=now.year) - now).days > 0:
            return (birth.replace(year=now.year) - now).days
        return (birth.replace(year=now.year + 1) - now).days


# phone1 = Phone('+380681537636')
# birthday1 = Birthday('27.05.1988')
# phone3 = Phone('+380681535555')
# phone4 = Phone('+380678889966')

# name1 = Name('Angle')
# name2 = Name('Lol')
# record1 = Record(name1, birthday1)
# record1.add_phone(phone1)
# record1.add_phone(phone4)
# record2 = Record(name2)
# record2.add_phone(phone3)


# address = AddressBook()
# address.add_record(record1)
# address.add_record(record2)
# address.serialize()

# print(record1.days_to_birthday())
# print(address.search('Angle'))
# print('-' * 15)
# for res in address.show_records(1):
#     print(res)
# print('-' * 15)
# print(address.records)

# print(phone1.value)
# print(record1)
# print(address)
