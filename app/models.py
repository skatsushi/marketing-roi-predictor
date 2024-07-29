from flask_login import UserMixin
from typing import Dict

class User(UserMixin):
    USERS = {
        'admin': {'password': 'secret'}
    }

    def __init__(self, username: str):
        self.username = username

    def get_id(self) -> str:
        return self.username

    @staticmethod
    def get(username: str):
        if username in User.USERS:
            return User(username)
        return None

    def check_password(self, password: str) -> bool:
        return User.USERS.get(self.username).get('password') == password




