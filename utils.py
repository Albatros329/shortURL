import random
import os
import sqlite3
from urllib.parse import urlparse

random_characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

def generate_random_code(length):
    return ''.join(random.choice(random_characters) for _ in range(length))

def get_db_connection():
    if not os.path.exists('data'):
        os.makedirs('data')
    conn = sqlite3.connect('data/database.db')
    conn.row_factory = sqlite3.Row
    return conn

def is_valid_url(url):
    try:
        parsed = urlparse(url)
        return all([parsed.scheme, parsed.netloc]) and parsed.scheme in ['http', 'https']
    except:
        return False
    
def initialize_database():
    # Initialiser la base de données
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS urls (short_url TEXT PRIMARY KEY, original_url VARCHAR(1024), expiration INTEGER, creation_date DATETIME DEFAULT CURRENT_TIMESTAMP)')
    conn.commit()
    conn.close()