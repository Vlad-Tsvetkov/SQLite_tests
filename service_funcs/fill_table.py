import sqlite3

from faker import Faker

fake = Faker()


def fill_table(num: int):
    req = 'INSERT INTO books (title, author, year) VALUES (?, ?, ?)'
    with sqlite3.connect('library.db') as connection:
        cursor = connection.cursor()
        added_rows = []
        for _ in range(num):
            row = (fake.company(), fake.name(), int(fake.year()))
            added_rows.append(row)
            cursor.execute(req, row)
    return added_rows
