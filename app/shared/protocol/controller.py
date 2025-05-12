# controller.py

import abc
from typing import Optional, Awaitable

from fastapi import Request, Response

from app.main.config.server.http import HttpRequest, HttpResponse  # your TypedDict or Pydantic types
from app.main.adapter.logger_adapter import Logger     
from app.shared.error.type.server_error import ServerError
from app.shared.util.get_line_number import getFileAndLineCaller# your Logger port


class IController(abc.ABC):
    """
    Defines the Controller contract:
      - optional logger injected
      - handle(): async method taking request/response, returning HttpResponse
    """
    def __init__(self, logger: Optional[Logger] = None) -> None:
        self.logger = logger

    @abc.abstractmethod
    async def handle(
        self,
        request: Optional[HttpRequest] = None,
        response: Optional[Response] = None
    ) -> Response:
        ...

class AbstractController(IController):
    """
    Provides a default `execute()` wrapper that calls `handle()` and
    catches/logs any unhandled exceptions.
    """

    async def execute(
        self,
        request: Request = None,
        response: Optional[Response] = None
    ) -> HttpResponse:
        try:
            # Convert FastAPI request to your HttpRequest type
                # Extract JSON from incoming FastAPI Request or custom HttpRequest
            if hasattr(request, "json"):
                payload = await request.json()
            else:
                payload = request.body or {}
                # Validate and parse into DTO
                
                # You can now use dto.name, dto.email, etc. in your use case
            http_request = HttpRequest(
                params=request.query_params,
                query=request.query_params,
                body= payload if request.method != "GET" else None,
                headers=request.headers,
                socket=None,
                token=None,
                file=None,
            )
            return await self.handle(http_request, response)
        except Exception as err:
            # Log the error
            if self.logger:
                self.logger.critical(
                    message=str(err),
                    metadata=getFileAndLineCaller(),
                )
            # Return a generic server error response, or re-raise
            return ServerError(err)