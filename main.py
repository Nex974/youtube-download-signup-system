import os.path

from Utils import ServiceUtils
from pytube import YouTube
import sqlite3
import random
import time

utils = ServiceUtils()


########################################################################################
# Database setup
########################################################################################

def db_setup() -> sqlite3.Cursor:
    conn = sqlite3.connect('users.db')

    cur = conn.cursor()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS users(name TEXT, password TEXT)"
    )

    conn.commit()

    return cur


########################################################################################
# Credentials management
########################################################################################

def get_creds() -> dict:
    username = input(
        "Please enter your username: "
    )
    password = input(
        "Please enter your password: "
    )

    if not utils.validate_username(username):
        print('Must provide a valid username (valid username is between 3 and 16 characters and is not taken)')
        get_creds()

    if not utils.validate_password(password):
        print(
            'Must provide a valid password (valid password is one that has characters and digits and is over 8 characters')
        get_creds()

    creds = {
        "username": username,
        "password": password
    }

    return creds


def register(cur: sqlite3.Cursor, username: str, password: str):
    password = (password,)
    username = (username,)

    username_query = cur.execute(f'SELECT name FROM users WHERE name = ?', username).fetchone()

    if username_query is not None:
        print(f'Username {username[0]} is already taken, maybe try with {username[0] + str(random.randint(1, 1000))}')

    else:
        cur.execute("INSERT INTO users VALUES (?, ?)", (username[0], password[0]))
        cur.connection.commit()
        print(f'Successfully created your account {username[0]} -- {time.asctime()}')
        utils.create_user_directory(username[0])


def login(cur: sqlite3.Cursor, username: str, password: str):
    password = (password,)  
    username = (username,)

    user_query = cur.execute(f'SELECT name FROM users WHERE name=?', username).fetchone()

    if user_query is None:
        print('User does not exist!')
        utils.clear(3)
        menu()
    # TODO 2: Either save hash of the password or save something "obfuscated" (not really) like rot13 or your
    # custom variation
    password_query = cur.execute('SELECT password FROM users WHERE name=?', username).fetchone()

    if password == password_query:
        print(f'Successfully logged {username[0]}, Welcome! -- {time.asctime()}')
        after_log_in(username[0])

    else:
        print(f'Wrong password for {username[0]}, this will be reported -- {time.asctime()}')
        # report_logging_error(username[])


def after_log_in(username):
    print(f'If you want to exit, type exit.')
    while True:
        url = input('Enter YouTube video URL: ')
        if url.lower() == 'exit':
            print(f'Exited successfully.')
            break
        yt = YouTube(url)
        title = f'{utils.get_video_title(yt.title)}.mp4'
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        path = os.path.expanduser(utils.PATH+username)
        try:
            stream.download(output_path=path, filename=title)
            print(f'Downloaded {title} successfully.')
        except Exception as e:
            print(f'Failed download, error = {e}')


def menu():
    choice = int(
        input(
            '''
        Please select an option
        1 -- Login
        2 -- Register
        '''
        )
    )

    if choice != 1 and choice != 2 and choice != 3:
        print("Select a valid option please!")
        utils.clear(3)
        menu()

    creds = get_creds()
    cursor = db_setup()

    if choice == 2:
        register(
            cursor,
            creds['username'],
            creds['password']
        )

    elif choice == 1:
        login(
            cursor,
            creds['username'],
            creds['password']
        )


def main() -> None:
    menu()


if __name__ == "__main__":
    main()
