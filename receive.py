import base64
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

# Login as receiver
receiver_block, receiver_key, receiver_balance = login()

# Base64 encode the Fernet key 10 times
encoded_key = receiver_key
for _ in range(10):
    encoded_key = base64.b64encode(encoded_key.encode()).decode()
print(f'Your encoded receive address: {encoded_key}')
print(f'Your block number: {receiver_block}')
