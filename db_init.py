import sqlite3


def create_schema():
    conn = sqlite3.connect('library.db', isolation_level=None)
    cursor = conn.cursor()

    try:
        # enable foreign key support
        cursor.execute("PRAGMA foreign_keys = ON;")

        # cursor.execute("""
        #     CREATE TABLE IF NOT EXISTS genres (
        #         id INTEGER PRIMARY KEY,
        #         name TEXT NOT NULL
        #     );
        # """)
        #
        # cursor.execute("""
        #     CREATE TABLE IF NOT EXISTS countries (
        #         id INTEGER PRIMARY KEY,
        #         name TEXT NOT NULL,
        #         isocode TEXT NOT NULL UNIQUE
        #     );
        # """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                rating INTEGER,
                customers_rated INTEGER,
                prize TEXT 
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS authors (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS book_authors (
                id INTEGER PRIMARY KEY,
                book_id INTEGER REFERENCES books(id),
                author_id INTEGER REFERENCES authors(id)
            );
        """)
    finally:
        cursor.close()
        conn.close()


def create_schema_with_script():
    conn = sqlite3.connect('library.db', isolation_level=None)

    try:
        with open('schema.sql', 'r') as fd:
            conn.executescript(fd.read())
    finally:
        conn.close()


if __name__ == '__main__':
    create_schema()
    # create_schema_with_script()
