from flask import Flask, render_template, request, redirect
from flask_wtf.csrf import CSRFProtect
from utils import generate_random_code
import uvicorn
from datetime import datetime, timedelta
import secrets
import sqlite3
import os

app = Flask(__name__)
csrf = CSRFProtect(app)

if app.debug:
    base_url = "http://localhost:8080/"
else:
    base_url = os.environ.get("BASEURL", "http://localhost:8080/") 

def get_db_connection():
    if not os.path.exists('data'):
        os.makedirs('data')
    conn = sqlite3.connect('data/database.db')
    conn.row_factory = sqlite3.Row
    return conn

app.config['SECRET_KEY'] = secrets.token_hex(16)


@app.route("/", methods=['GET'])
def index():
    """
    Page d'accueil
    """
    return render_template('index.html')

@app.route("/<short_url>", methods=['GET']) # type: ignore
def redirect_to_url(short_url):
    """
    Rediriger vers l'URL originale
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Récupérer l'URL originale
    cursor.execute('SELECT original_url FROM urls WHERE short_url = ?', (short_url,))
    original_url = cursor.fetchone()

    if not original_url:
        conn.close()
        return render_template('invalid.html'), 404

    

    if original_url:
        # Supprimer l'entrée si elle est à usage unique ou expirée
        cursor.execute('DELETE FROM urls WHERE short_url = ? AND (expiration IS NOT NULL AND expiration <= ?)', (short_url, datetime.now()))
        conn.commit()

        conn.close()
        return redirect(original_url[0])


@app.route("/shorten/", methods=['POST'])
def shorten_url():
    """
    Créer une URL courte
    """
    short_url = generate_random_code(6)
    expiration = int(request.form.get('expiration', 0))

    if expiration:
        if expiration == -1:
            expiration = 1  # Usage unique
        else:
            expiration = datetime.now() + timedelta(seconds=expiration)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO urls (short_url, original_url, expiration) VALUES (?, ?, ?)',
                   (short_url, request.form['url'], expiration))
    conn.commit()
    conn.close()

    return render_template(
        'results.html',
        short_url=short_url,
        base_url=base_url,
    )



if __name__ == "__main__":
    # Initialiser la base de données
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS urls (short_url TEXT PRIMARY KEY, original_url VARCHAR(1024), expiration INTEGER, creation_date DATETIME DEFAULT CURRENT_TIMESTAMP)')
    conn.commit()
    conn.close()

    app.run(host='0.0.0.0', debug=False, port=8080)