from typing import Dict, Union
from core.user import User

class Register:
    def __init__(self) -> Dict[str, User]:
        self.table: Dict[str, User] = {}

    def add_user(self, user: User) -> Union[Dict[str, User], str]:
        if user['name'] in self.table:
            return 'Usuário já registrado'

        self.table[user['name']] = user
        return 'Usuário registrado com sucesso!'

    def remove_user(self, user_name: str) -> Union[Dict[str, User], str]:
        if not user_name in self.table:
            return 'Usuário não cadastrado'

        del self.table[user_name]
        return 'Usuário removido com sucesso!'

    def get_user(self, user_name: str) -> Union[str, User]:
        if user_name in self.table:
            return self.table[user_name]
        else:
            return 'Usuário não registrado'
