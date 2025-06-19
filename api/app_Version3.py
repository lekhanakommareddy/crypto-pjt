import os
import sqlite3
from flask import Flask, g, render_template, request, redirect, session
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
import secrets

app = Flask(__name__, static_url_path='/static')
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

DATABASE = 'users.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    return db, cursor

def close_db(e=None):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.teardown_appcontext
def teardown_db(e=None):
    close_db()

def init_db():
    with app.app_context():
        db, cursor = get_db()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password BLOB,
                private_key BLOB
            )
        ''')
        db.commit()

def generate_rsa_keypair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

def encrypt_data(data, public_key):
    encrypted_data = public_key.encrypt(
        data.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_data

def decrypt_data(encrypted_data, private_key):
    decrypted_data = private_key.decrypt(
        encrypted_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted_data.decode()

def generate_otp():
    return str(secrets.randbelow(1000000)).zfill(6)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db, cursor = get_db()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        if cursor.fetchone():
            print("Username already exists.", flush=True)
            return "Username already exists. Please choose another one."

        private_key, public_key = generate_rsa_keypair()
        encrypted_password = encrypt_data(password, public_key)

        cursor.execute('''
            INSERT INTO users (username, password, private_key) VALUES (?, ?, ?)
        ''', (username, encrypted_password, private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )))
        db.commit()

        print(f"User {username} registered.", flush=True)
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print("Login POST received", flush=True)  # Debug print

        username = request.form['username']
        password = request.form['password']

        db, cursor = get_db()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        print(f"User found: {user is not None}", flush=True)  # Debug print

        if not user:
            print("Username not found.", flush=True)  # Debug print
            return "Username not found. Please register."

        try:
            private_key = serialization.load_pem_private_key(user[3], password=None, backend=default_backend())
            decrypted_password = decrypt_data(user[2], private_key)
            print(f"Password match: {password == decrypted_password}", flush=True)  # Debug print
        except Exception as e:
            print(f"Private key or decryption error: {e}", flush=True)
            return "Error reading your credentials. Please register again."

        if password == decrypted_password:
            generated_otp = generate_otp()
            print(f"Generated OTP for {username}: {generated_otp}", flush=True)  # OTP printed here
            session['generated_otp'] = generated_otp
            return render_template('otp_verification.html', username=username)
        else:
            print("Incorrect password.", flush=True)  # Debug print
            return "Incorrect username or password. Please try again."
    return render_template('login.html')

@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    if request.method == 'POST':
        username = request.form['username']
        otp_value = request.form['otp']
        generated_otp = session.get('generated_otp')
        print(f"Verifying OTP: entered={otp_value}, session={generated_otp}", flush=True)
        if not generated_otp:
            print("OTP session expired.", flush=True)
            return "OTP session expired. Please try again."
        if otp_value == generated_otp:
            session.pop('generated_otp')
            session['username'] = username
            print("OTP verified successfully.", flush=True)
            return redirect('/dashboard')
        else:
            print("Incorrect OTP entered.", flush=True)
            return "Incorrect OTP. Please try again."

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)