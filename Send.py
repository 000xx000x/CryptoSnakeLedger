import base64
import hashlib
from cryptography.fernet import Fernet

def get_account_data(block_number, key):
    # Create a Fernet object with the provided key
    cipher_suite = Fernet(key.encode())

    # Read the encrypted account data
    with open(f'crypt{block_number}', 'rb') as f:
        cipher_text = f.read()

    # Decrypt the account data
    account_data = cipher_suite.decrypt(cipher_text).decode()

    return account_data

def update_account_data(block_number, key, new_data):
    # Create a Fernet object with the provided key
    cipher_suite = Fernet(key.encode())

    # Encrypt the new account data
    cipher_text = cipher_suite.encrypt(new_data.encode())

    # Write the encrypted new account data
    with open(f'crypt{block_number}', 'wb') as f:
        f.write(cipher_text)

def record_transaction(sender_block, receiver_block, amount, sender_key):
    # Prepare the transaction data
    transaction_data = f'SENDER: {sender_block}\nRECEIVER: {receiver_block}\nAMOUNT: {amount}\n'

    # Generate a unique hash for this transaction
    transaction_hash = hashlib.sha256(transaction_data.encode()).hexdigest()
    
    # Include the hash of the previous transactions (if any)
    try:
        with open('Transaction', 'rb') as f:
            previous_transactions = f.read().decode()
            previous_hash = hashlib.sha256(previous_transactions.encode()).hexdigest()
            transaction_data += f'PREVIOUS HASH: {previous_hash}\n'
    except FileNotFoundError:
        pass

    # Add the current transaction's hash
    transaction_data += f'HASH: {transaction_hash}\n'

    # Encrypt the transaction data using the sender's Fernet key
    cipher_suite = Fernet(sender_key.encode())
    cipher_text = cipher_suite.encrypt(transaction_data.encode())

    # Append the encrypted transaction data to the file
    with open('Transaction', 'ab') as f:
        f.write(cipher_text + b'\n')

def login():
    key = input("Enter your Fernet key: ")
    block_number = input("Enter your block number: ")

    account_data = get_account_data(block_number, key)

    # Extract the balance from the account data
    balance_line = [line for line in account_data.split('\n') if line.startswith('AMOUNT')][0]
    
    try:
        balance = int(balance_line.split(': ')[1])
    except IndexError:
        balance = 0

    print(f'Your account balance is: {balance}')

    return block_number, key, balance

# Login as sender
sender_block, sender_key, sender_balance = login()

# Ask for the receiver's block number and base64 encoded address
receiver_block = input("Enter receiver's block number: ")
encoded_receiver_address = input("Enter receiver's base64 encoded address: ")

# Base64 decode the receiver's address 10 times to get the Fernet key
receiver_key = encoded_receiver_address
for _ in range(10):
    receiver_key = base64.b64decode(receiver_key).decode()

# Ask for the amount to send
amount_to_send = int(input("Enter amount to send: "))

# Deduct the amount from sender's balance and add it to receiver's balance
sender_data = get_account_data(sender_block, sender_key)
receiver_data = get_account_data(receiver_block, receiver_key)

sender_balance_line = [line for line in sender_data.split('\n') if line.startswith('AMOUNT')][0]
sender_balance = int(sender_balance_line.split(': ')[1])
receiver_balance_line = [line for line in receiver_data.split('\n') if line.startswith('AMOUNT')][0]

try:
    receiver_balance = int(receiver_balance_line.split(': ')[1])
except IndexError:
    receiver_balance = 0

if amount_to_send > sender_balance:
    print("Insufficient balance.")
else:
    sender_balance -= amount_to_send
    receiver_balance += amount_to_send

    sender_data = sender_data.replace(sender_balance_line, f'AMOUNT: {sender_balance}')
    receiver_data = receiver_data.replace(receiver_balance_line, f'AMOUNT: {receiver_balance}')

    update_account_data(sender_block, sender_key, sender_data)
    update_account_data(receiver_block, receiver_key, receiver_data)

# Record this transaction in an encrypted form in a file called "Transaction"
record_transaction(sender_block, receiver_block, amount_to_send, sender_key)
