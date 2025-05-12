
class UserLoginDTO:
    """
    Data Transfer Object for user login.
    """

    def __init__(self, document: str, password: str):
        self.document = document
        self.password = password

    def __repr__(self):
        return f"UserLoginDTO(email={self.document}, password=****)"