import sqlite3
import pytest


@pytest.fixture()
def table():
    connection = sqlite3.connect('library.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        year INTEGER NOT NULL
    )
    ''')
    connection.commit()
    yield connection
    cursor.execute("DELETE FROM books")
    connection.commit()
    connection.close()
