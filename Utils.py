# import string  # TICKET 1
import requests
import hashlib
import time
import os
import re


########################################################################################
# Utils
########################################################################################


class ServiceUtils:
    # Variables
    PATH = '~/Desktop/SongsDatabase/'

    # Methods

    # TODO 1: Make more checks for the user data

    def clear(self, delay):
        time.sleep(delay)
        os.system("clear" if os.name == "posix" else "cls")

    def validate_username(self, username: str) -> bool:
        if len(username) < 3:
            return False
        if len(username) > 16:
            return False
        return True

    def validate_password(self, password: str) -> bool:

        if len(password) < 8:
            return False

        if not any(char.isdigit() for char in password):
            return False

        if not any(char.isalpha() for char in password):
            return False

        '''
               if password in common_passwords:
                   return False
               #TODO: substitute with breach 
        '''
        return True

    # def validate_choice() -> None:

    def create_user_directory(self, username: str) -> None:
        parent_directory = os.path.expanduser(ServiceUtils.PATH)
        directory = os.path.join(parent_directory, username)
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"Directory {directory} created")
        except OSError:
            print(f'Unable to create directory {directory}')

    def get_video_title(self, title: str) -> str:
        return re.sub(r'[\\/*?:"<>|]', "", title)
