from cryptography.fernet import Fernet

def login():
    key = input("Enter your Fernet key: ")
    block_number = input("Enter your block number: ")

    # Create a Fernet object with the provided key
    cipher_suite = Fernet(key.encode())

    # Read the encrypted account data
    with open(f'crypt{block_number}', 'rb') as f:
        cipher_text = f.read()

    # Decrypt the account data
    account_data = cipher_suite.decrypt(cipher_text).decode()

    # Extract the balance from the account data
    balance_line = [line for line in account_data.split('\n') if line.startswith('AMOUNT')][0]
    
    try:
        balance = balance_line.split(': ')[1]
    except IndexError:
        balance = ''

    # If balance is blank, display it as 0
    if not balance:
        balance = '0'

    print(f'Your account balance is: {balance}')

login()
