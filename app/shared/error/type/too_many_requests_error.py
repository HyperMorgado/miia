class TooManyRequestsError(Exception):
    def __init__(self):
        super().__init__("Too many requests error")