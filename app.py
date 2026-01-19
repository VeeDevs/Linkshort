from flask import Flask, request, redirect, render_template, url_for, flash
import sqlite3
import string
import random
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Database setup
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            long_url TEXT NOT NULL,
            short_code TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def insert_url_mapping(long_url, short_code):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO urls (long_url, short_code) VALUES (?, ?)', (long_url, short_code))
    conn.commit()
    conn.close()

def get_long_url(short_code):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT long_url FROM urls WHERE short_code = ?', (short_code,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def generate_short_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        long_url = request.form['long_url']
        short_code = generate_short_code()
        insert_url_mapping(long_url, short_code)
        flash(f"Shortened URL: {request.url_root}{short_code}", "success")
        return redirect(url_for('index'))
    return render_template('index.html')

@app.route('/<short_code>')
def redirect_to_long_url(short_code):
    long_url = get_long_url(short_code)
    if long_url:
        return redirect(long_url)
    else:
        return "URL not found", 404

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
