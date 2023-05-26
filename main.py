from my_cls import AddressBook, Field, Name, Phone, Record


def error_handler(func):
    def inner(*args):
        try:
            result = func(*args)
            return result
        except KeyError:
            return "No user"
        except ValueError:
            return 'Give me name and phone please'
        except IndexError:
            return 'Enter user name'
        # except Exception:
        #     return 'Other ERROR'
    return inner


def hello_user():
    return "How can I help you?"


def unknown_command():
    return "unknown_command"


@error_handler
def add_user(name, phone):
    record = Record(Name(name))
    record.add_phone(Phone(phone))
    users.add_record(record)
    return f'User {name} added!'


@error_handler
def change_phone(name, old_phone, new_phone):
    record = users.get(name)
    old_phone = Phone(old_phone)
    new_phone = Phone(new_phone)
    tel = record.get_phone(old_phone.value)
    if tel:
        record.edit_phone(tel, new_phone)
    else:
        return f'Phone not found'
    return f'Done!'


@error_handler
def show_all():
    return users


@error_handler
def show_phone(name):
    record = users.get(name)
    return record


HANDLERS = {
    'hello': hello_user,
    'add': add_user,
    'change': change_phone,
    'show': show_all,
    'phone': show_phone,
}


def main():

    while True:
        command, *data = input('Please enter command: ').strip().split(' ', 1)

        if command in ["goodbye", "close", "exit"]:
            print("Good bye!")
            break

        if HANDLERS.get(command):
            handler = HANDLERS.get(command)
            if data:
                data = data[0].strip().split(' ')

            result = handler(*data)
        else:
            result = unknown_command()

        print(result)


if __name__ == "__main__":
    users = AddressBook()
    main()
