from flask import Flask, render_template, request, redirect, abort
from flask_wtf.csrf import CSRFProtect
from utils import generate_random_code, get_db_connection, is_valid_url
from datetime import datetime, timedelta
import secrets
import sqlite3
import os


app = Flask(__name__)
csrf = CSRFProtect(app)

if app.debug:
    base_url = "http://localhost:5000/"
else:
    base_url = os.environ.get("BASEURL", "http://localhost:8080/") 


app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(16))


@app.route("/", methods=['GET'])
def index():
    """
    Page d'accueil
    """
    return render_template('index.html')

@app.route("/<short_url>", methods=['GET'])
def redirect_to_url(short_url):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT original_url, expiration FROM urls WHERE short_url = ?', (short_url,))
    row = cursor.fetchone()

    if row:
        original_url = row['original_url']
        expiration = row['expiration']
        
        if expiration:
            # Cas usage unique (stocké comme entier 1)
            if expiration == 1:
                cursor.execute('DELETE FROM urls WHERE short_url = ?', (short_url,))
                conn.commit()
            # Cas expiration temporelle
            else:
                try:
                    exp_date = datetime.fromisoformat(str(expiration))
                    if datetime.now() > exp_date:
                        cursor.execute('DELETE FROM urls WHERE short_url = ?', (short_url,))
                        conn.commit()
                        conn.close()
                        return "Lien expiré", 404
                except ValueError:
                    pass 

        conn.close()
        return redirect(original_url)
    else:
        conn.close()
        return "URL non trouvée", 404


@app.route("/shorten/", methods=['POST'])
def shorten_url():
    original_url = request.form['url']
    
    if not is_valid_url(original_url):
        return abort(400, description="URL invalide.")

    expiration = int(request.form.get('expiration', 0))

    if expiration:
        if expiration == -1:
            expiration = 1
        else:
            expiration = datetime.now() + timedelta(seconds=expiration)
    else:
        expiration = None

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Gestion des collisions
    short_url = None
    for _ in range(5):
        try:
            short_url = generate_random_code(6)
            cursor.execute('INSERT INTO urls (short_url, original_url, expiration) VALUES (?, ?, ?)',
                        (short_url, original_url, expiration))
            conn.commit()
            break
        except sqlite3.IntegrityError:
            continue
            
    conn.close()

    if not short_url:
        return render_template('index.html', error="Erreur lors de la génération. Veuillez réessayer.")

    return render_template(
        'results.html',
        short_url=short_url,
        base_url=base_url
    )



if __name__ == "__main__":
    # Initialiser la base de données
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS urls (short_url TEXT PRIMARY KEY, original_url VARCHAR(1024), expiration INTEGER, creation_date DATETIME DEFAULT CURRENT_TIMESTAMP)')
    conn.commit()
    conn.close()