from flask import Flask, render_template, request, redirect, url_for, abort
import database as db
import hashlib
import sqlite3
import random


def lengthen_url(og_url, base_url):
    random_length = random.randint(5, 10)
    # Generate a hash of the original URL using SHA-256
    hashed_url = hashlib.sha256(og_url.encode()).hexdigest()
    # Return the full LongLongURL including the base URL
    lnglngurl_hashed = base_url + hashed_url[:random_length]
    print(lnglngurl_hashed)
    return lnglngurl_hashed


app = Flask(__name__)
db.create_db()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        og_url = request.form['og_url']
        base_url = request.host_url
        lnglng_url = lengthen_url(og_url, base_url)
        connection = sqlite3.connect('url_converter.db')
        c = connection.cursor()
        # Check if the original URL already exists in the database
        c.execute('''SELECT longlong_url FROM urls WHERE original_url=?''', (og_url,))
        result = c.fetchone()
        if result is not None:
            # If the original URL already exists, use the existing LongLongURL
            lnglng_url = result[0]
        else:
            # Otherwise, insert a new record with the original and LongLong URLs
            c.execute('''INSERT INTO urls (original_url, longlong_url) VALUES (?, ?)''', (og_url, lnglng_url))
            connection.commit()
        connection.close()
        print(f"OG_URL: {og_url}")
        print(f"LONGURL: {lnglng_url}")
        return render_template('ConvertedURL_Page.html', og_url=og_url, lnglng_url=lnglng_url)
    else:
        return render_template('index.html')


@app.route('/<path:longlong_url>')
def redirect_url(longlong_url):
    # Strip the base URL from the LongLongURL to get just the hash
    hash_value = longlong_url.replace(request.host_url, "")
    connection = sqlite3.connect('url_converter.db')
    c = connection.cursor()
    c.execute("SELECT * FROM urls WHERE longlong_url=?", (request.host_url + hash_value,))
    url = c.fetchone()
    connection.close()
    if url is not None:
        original_url = url[1]
        return redirect(original_url)
    else:
        return "URL not found", 404


if __name__ == '__main__':
  db.create_db()
  app.run(debug=True)
