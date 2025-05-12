from typing import Any, Optional, Literal, Callable
from pydantic import BaseModel
from starlette.datastructures import UploadFile
# from src.context.user.domain.model.user import IUser  # your domain user class

FileType = Literal["pdf", "doc", "docx", "xlsx"]

class FileResponse():
    fileType: FileType

class HttpResponse():
    statusCode: int
    body: Any

class HttpRequest():
    def __init__(
        self,
        params: Optional[Any] = None,
        query: Optional[Any] = None,
        body: Optional[Any] = None,
        headers: Optional[Any] = None,
        socket: Optional[Any] = None,
        token: Optional[str] = None,
        file: Optional[UploadFile] = None,
    ) :
        self.params = params
        self.query = query
        self.body = body
        self.headers = headers
        self.socket = socket
        self.token = token
        self.file = file

# Next-function type alias
HttpNextFunction = Callable[[Optional[Exception]], None]