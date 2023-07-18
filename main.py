import sqlite3
from getpass import getpass
import requests

# Connecting to or creating SQLite database
conn = sqlite3.connect('users_db.sqlite')
cursor = conn.cursor()

# Creating users table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL);
''')
conn.commit()

def register():
    while True:
        username = input("Enter a username: ")
        cursor.execute('SELECT * FROM users WHERE username=?', (username,))
        if cursor.fetchone() is not None:
            print("Username already taken. Try a different username.")
        else:
            password = getpass("Enter a password: ")
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            print("Registration successful!")
            break

def login():
    username = input("Enter your username: ")
    password = getpass("Enter your password: ")
    cursor.execute('SELECT password FROM users WHERE username=?', (username,))
    db_password = cursor.fetchone()
    if db_password is None:
        print("Username not found. Please try again.")
    else:
        if password == db_password[0]:
            print("Login successful!")
        else:
            print("Incorrect password. Please try again.")

def view_prices():
    response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd")
    prices = response.json()
    print(f"Bitcoin Price: ${prices['bitcoin']['usd']}")
    print(f"Ethereum Price: ${prices['ethereum']['usd']}")

def main_menu():
    while True:
        print("1. Register\n2. Login\n3. View Market Prices\n4. Quit")
        choice = input("Choose an option: ")
        if choice == "1":
            register()
        elif choice == "2":
            login()
        elif choice == "3":
            view_prices()
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()

# Closing connection to database
conn.close()
