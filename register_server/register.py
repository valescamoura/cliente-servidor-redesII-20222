from typing import Dict, Union
from core.user import User

class Register:
    def __init__(self) -> Dict[str, User]:
        self.table = {}

    def add_user(self, user: User) -> Union[Dict[str, User], str]:
        if user.name in self.table:
            return 'Usuário já registrado'

        self.table[user.name] = user
        return self.table

    def remove_user(self, user: User) -> Union[Dict[str, User], str]:
        if not user.name in self.table:
            return 'Usuário não cadastrado'

        del self.table[user.name]
        return self.table
