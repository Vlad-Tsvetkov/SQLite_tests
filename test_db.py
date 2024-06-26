from faker import Faker
from service_funcs.fill_table import fill_table
from random import randint

fake = Faker()


def test_add_book(table):
    cursor = table.cursor()
    insert_req = 'INSERT INTO books (title, author, year) VALUES (?, ?, ?)'
    check_req = 'SELECT * FROM books where title = ? and author = ? and year = ?'
    row = (fake.company(), fake.name(), int(fake.year()))
    cursor.execute(insert_req, row)
    table.commit()

    cursor.execute(check_req, (row[0], row[1], row[2]))
    res = cursor.fetchone()[1:]
    assert row == res


def test_get_all_books(table):
    added_rows = fill_table(5)
    req = 'SELECT * FROM books'
    cursor = table.cursor()
    cursor.execute(req)
    table.commit()
    res = list(map(lambda x: x[1:], cursor.fetchall()))
    assert res == added_rows


def test_get_info_by_id(table):
    rows_num = 5
    added_rows = fill_table(rows_num)
    id = randint(1, rows_num)
    req = 'SELECT title, author, year FROM books WHERE id = ?'
    cursor = table.cursor()
    cursor.execute(req, (id,))
    table.commit()
    row = cursor.fetchone()
    assert row == added_rows[id - 1]


def test_update_info_by_id(table):
    rows_num = 5
    fill_table(rows_num)
    id = randint(1, rows_num)
    new_data = (fake.company(), fake.name(), int(fake.year()), id)
    update_req = 'UPDATE books SET title = ?, author = ?, year = ? WHERE id = ?'
    check_req = 'SELECT title, author, year, id FROM books WHERE id = ?'

    cursor = table.cursor()
    cursor.execute(update_req, new_data)
    table.commit()

    cursor.execute(check_req, (id,))
    table.commit()
    res = cursor.fetchone()
    assert res == new_data


def test_delete_info_by_id(table):
    rows_num = 5
    fill_table(rows_num)
    id = randint(1, rows_num)
    delete_req = 'DELETE FROM books WHERE id = ?'
    check_req = 'SELECT * FROM books WHERE id = ?'

    cursor = table.cursor()
    cursor.execute(delete_req, (id,))
    table.commit()

    cursor.execute(check_req, (id,))
    table.commit()
    res = cursor.fetchone()
    assert res is None


def test_get_nonexisting_book(table):
    rows_num = 1
    fill_table(rows_num)
    id = 5
    check_req = 'SELECT * FROM books WHERE id = ?'
    cursor = table.cursor()
    cursor.execute(check_req, (id,))
    table.commit()
    res = cursor.fetchone()
    assert res is None
