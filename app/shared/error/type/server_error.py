from typing import Optional

class ServerError(Exception):
    """
    Represents a generic 500 Internal Server Error.
    
    Attributes:
        stack: Optional string containing a custom stack trace or error details.
    """
    def __init__(self, stack: Optional[str] = None):
        # Set the exception message
        super().__init__("Internal server error")
        # Mirror the TypeScript .stack property if provided
        self.stack = stack