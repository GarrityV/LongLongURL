import sqlite3


def create_db():
    connection = sqlite3.connect('url_converter.db')
    c = connection.cursor()
    # Check if table exists
    c.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='urls' ''')
    if c.fetchone()[0]==1:
        print('Table exists')
    else:
        # Create table if it doesn't exist
        c.execute('''CREATE TABLE urls
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                     original_url TEXT NOT NULL, 
                     longlong_url TEXT NOT NULL UNIQUE)''')
        print('Table created')
    connection.commit()
    connection.close()


def insert_url(original_url, longlong_url):
    connection = sqlite3.connect('url_converter.db')
    c = connection.cursor()
    c.execute("INSERT INTO urls (original_url, longlong_url) VALUES (?, ?)", (original_url, longlong_url))
    connection.commit()
    connection.close()


def select_url_by_longlong_url(longlong_url):
    connection = sqlite3.connect('url_converter.db')
    c = connection.cursor()
    c.execute("SELECT * FROM urls WHERE longlong_url=?", (longlong_url,))
    url = c.fetchone()
    connection.close()
    return url


def select_url_by_id(id):
    connection = sqlite3.connect('url_converter.db')
    c = connection.cursor()
    c.execute("SELECT * FROM urls WHERE id=?", (id,))
    url = c.fetchone()
    connection.close()
    return url