class AbstractControllerIncorrectImplementation(Exception):
    """
    Raised when a subclass of AbstractController fails to override the handle() method properly.
    """
    def __init__(self):
        super().__init__("AbstractController incorrect implementation in handle function")