import os
import hashlib
import random
from cryptography.fernet import Fernet

def create_account(previous_hash=''):
    password = input("Enter your password: ")
    encrypted_password = hashlib.sha256(password.encode()).hexdigest()
    block_number = random.randint(100, 999)

    # Prepare the account data
    account_data = f'BLOCKS: {block_number}\nHASH: {encrypted_password}\nAMOUNT:\n'

    # Add the hash of the previous account
    if previous_hash:
        account_data += f'PREVIOUS HASH: {previous_hash}\n'

    # Generate a unique hash for this account
    account_hash = hashlib.sha256(account_data.encode()).hexdigest()
    account_data += f'HASH: {account_hash}\n'

    # Generate a Fernet key and create a Fernet object
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)

    # Encrypt the account data
    cipher_text = cipher_suite.encrypt(account_data.encode())

    with open(f'crypt{block_number}', 'wb') as f:
        f.write(cipher_text)

    print(f'Your account has been created with block number {block_number}.')
    print(f'Your Fernet key is: {key.decode()}')
    print('Please save this key and do not share it with anyone.')

    return account_hash

# Create the first account
previous_hash = create_account()

# Create more accounts, each one linked to the previous one
for _ in range(10):
    previous_hash = create_account(previous_hash)
