# Online Transaction Security Enhancement Using Cryptographic Techniques

The Online Transaction Security Enhancement Using Cryptographic Techniques is a secure approach to handle online transactions by leveraging modern cryptographic methods, including RSA encryption and OTP-based multi-factor authentication. Designed with Python Flask as the backend and SQLite for storage, the application offers a clear, practical example of how cryptography can be integrated into user registration, login, and transaction workflows.

---

## About the Project

In today's digital world, the security of online transactions is paramount. This application showcases how sensitive user data can be encrypted and protected using public-key cryptography (RSA), with an added layer of security through one-time passwords (OTP). The project is suitable as a learning resource, a proof-of-concept, or as a foundational block for production-ready secured web applications.

---

## Key Highlights

- **Robust User Security:** Each registered user is assigned an individual RSA key pair. Passwords are encrypted with the user's public key and stored in the database, ensuring that raw credentials are never exposed.
- **Multi-Factor Authentication:** After successful login, users are prompted to enter a one-time password (OTP), which strengthens protection against unauthorized access.
- **Secure Session Management:** User sessions are handled securely within Flask, and sensitive operations require authentication and OTP verification.
- **Transparent Data Handling:** All cryptographic operations (key generation, password encryption/decryption) are performed using Python's trusted `cryptography` library.
- **Simple and Portable Storage:** User details and encrypted private keys are stored in a local SQLite database, making it easy to deploy or migrate.

---

## Getting Started

### Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/lekhanakommareddy/crypto-pjt.git
   cd crypto-pjt
   ```

2. **(Optional but recommended) Create a Python virtual environment:**
   ```bash
   python -m venv venv
   # Activate it:
   # On Windows:
   venv\Scripts\activate
   # On Linux/macOS:
   source venv/bin/activate
   ```

3. **Install the necessary dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the Flask server:**
   ```bash
   cd api
   python app.py
   ```
   The application will be available at [http://127.0.0.1:5000](http://127.0.0.1:5000).

---

## How It Works

- **Registration:** New users sign up with a username and password. The backend generates a unique RSA key pair for the user, encrypts the password with the public key, and stores everything securely.
- **Login:** When a user logs in, the application decrypts the stored password using the user's private key and verifies credentials.
- **OTP Verification:** After password verification, a random OTP is generated and must be entered by the user to complete the login process.
- **User Dashboard:** Only after successful OTP entry does the user gain access to protected resources.
- **Database Viewing:** Use the included script (`show_database.py`) to inspect user records and their encrypted data for administrative or educational purposes.

---

## Security Considerations

- **No Plaintext Storage:** Passwords and private keys are always stored in encrypted form.
- **Key Isolation:** Each user operates with their own key pair, reducing the risk of widespread compromise.
- **Session Protection:** Sessions are securely managed to prevent unauthorized access or session hijacking.
- **Extensible Design:** The system is architected to add further cryptographic methods or integrate with other authentication providers as needed.

---

## Contributing

Contributions are encouraged! If you'd like to suggest improvements, fix bugs, or add features:

1. Fork this repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes with clear messages.
4. Push to your fork and open a pull request.



