# coding=utf-8
import shelve


def store_person(db):
    pid = raw_input('input persion id')
    person = {}
    person['name'] = raw_input('enter name')
    person['age'] = raw_input('enter age')
    person['phone'] = raw_input('enter phone')
    print(person)
    db[pid] = person
    print(db)


def lookup_person(db):
    pid = raw_input('id')
    field = raw_input('enter what you know(key = id name, age phone)')
    key = field.strip().lower()
    print field.capitalize() + ':', \
            db[pid][key]


def main():
    database = shelve.open('e:\\person_data.txt')
    try:
        # store_person(database)
        lookup_person(database)
    finally:
        database.close()

if __name__ == '__main__': main
