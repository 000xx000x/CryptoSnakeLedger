import random
import curses
from cryptography.fernet import Fernet

MAX_COINS = 97000000
coins_left = MAX_COINS

def get_account_data(block_number, fernet_key):
    cipher_suite = Fernet(fernet_key)
    with open(f'crypt{block_number}', 'rb') as f:
        cipher_text = f.read()
    account_data = cipher_suite.decrypt(cipher_text).decode()
    return account_data

def update_account_data(block_number, fernet_key, new_data):
    cipher_suite = Fernet(fernet_key)
    cipher_text = cipher_suite.encrypt(new_data.encode())
    with open(f'crypt{block_number}', 'wb') as f:
        f.write(cipher_text)

def login():
    fernet_key = input("Enter your Fernet key: ")
    block_number = input("Enter your block number: ")
    account_data = get_account_data(block_number, fernet_key)
    balance_line = [line for line in account_data.split('\n') if line.startswith('AMOUNT')]
    try:
        balance = int(balance_line[0].split(': ')[1])
    except IndexError:
        balance = 0
    print(f'Your account balance is: {balance}')
    return block_number, fernet_key, balance

def main():
    global coins_left
    block_number, fernet_key, balance = login()
    s = curses.initscr()
    curses.curs_set(0)
    sh, sw = s.getmaxyx()
    w = curses.newwin(sh, sw, 0, 0)
    w.keypad(1)
    w.timeout(100)
    snk_x = sw//4
    snk_y = sh//2
    snake = [
        [snk_y, snk_x],
        [snk_y, snk_x-1],
        [snk_y, snk_x-2]
    ]
    food = [sh//2, sw//2]
    w.addch(int(food[0]), int(food[1]), curses.ACS_PI)
    direction_key = curses.KEY_RIGHT  # Use a different variable name for the direction key
    while True:
        next_key = w.getch()
        direction_key = direction_key if next_key == -1 else next_key
        if snake[0][0] in [0, sh] or snake[0][1]  in [0, sw] or snake[0] in snake[1:]:
            curses.endwin()
            quit()
        new_head = [snake[0][0], snake[0][1]]
        if direction_key == curses.KEY_DOWN:
            new_head[0] += 1
        if direction_key == curses.KEY_UP:
            new_head[0] -= 1
        if direction_key == curses.KEY_LEFT:
            new_head[1] -= 1
        if direction_key == curses.KEY_RIGHT:
            new_head[1] += 1
        snake.insert(0, new_head)
        if snake[0] == food:
            food = None
            while food is None:
                nf = [
                    random.randint(1, sh-1),
                    random.randint(1, sw-1)
                ]
                food = nf if nf not in snake else None
            w.addch(food[0], food[1], curses.ACS_PI)
            reward = min(coins_left, len(snake))
            coins_left -= reward
            balance += reward
            print(f"You won {reward} coin(s)! Your new balance is {balance}.")
            account_data = get_account_data(block_number, fernet_key)
            balance_line = [line for line in account_data.split('\n') if line.startswith('AMOUNT')]
            new_account_data = account_data.replace(balance_line[0], f'AMOUNT: {balance}')
            update_account_data(block_number, fernet_key, new_account_data)
        else:
            tail = snake.pop()
            w.addch(int(tail[0]), int(tail[1]), ' ')
        w.addch(int(snake[0][0]), int(snake[0][1]), curses.ACS_CKBOARD)

if __name__ == "__main__":
    main()
