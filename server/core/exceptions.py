class UserAlreadyExistsError(Exception):
    def __init__(self, message:list[str]):
        self.message = message

class DatabaseError(Exception):
    pass