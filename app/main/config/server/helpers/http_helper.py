import os
from typing import Any, Dict, Optional

from app.main.adapter.logger_adapter import Logger              # our Python port of your Winston adapter
from app.main.config.server.http import HttpResponse
from app.shared.util.get_line_number import getFileAndLineCaller  # see below for a quick impl
from app.shared.error.type.server_error import ServerError
from app.shared.error.type.unauthorized_error import UnauthorizedError
from app.shared.error.type.too_many_requests_error import TooManyRequestsError

NODE_ENV = os.getenv("NODE_ENV", "development")


def bad_request(error: Exception) -> Dict[str, Any]:
    Logger().info(
        message=f"[HTTP:400 BadRequest]: {error}",
        metadata={"file": getFileAndLineCaller()},
    )
    return {"error_code": 400, "error": error}


def forbidden(error: Exception) -> Dict[str, Any]:
    Logger().info(
        message=f"[HTTP:403 Forbidden]: {error}",
        metadata={"file": getFileAndLineCaller()},
    )
    return {"error_code": 403, "error": error}


def unauthorized(error: Optional[Exception] = None) -> Dict[str, Any]:
    msg = error.message if error and hasattr(error, "message") else "[HTTP:401 Unauthorized]"
    Logger().info(
        message=msg,
        metadata={"file": getFileAndLineCaller()},
    )
    return {
        "error_code": 401,
        "error": error or UnauthorizedError(),
    }


def too_many_requests() -> Dict[str, Any]:
    Logger().info(
        message="[HTTP:429 TooManyRequests]",
        metadata={"file": getFileAndLineCaller()},
    )
    return {
        "error_code": 429,
        "error": TooManyRequestsError(),
    }


def server_error(error: Exception) -> Dict[str, Any]:
    Logger().error(
        message="[HTTP:500 ServerError]",
        metadata={"file": getFileAndLineCaller()},
    )

    if NODE_ENV == "development":
        print("\n\n⚠️ ⚠️", error, getattr(error, "__traceback__", ""))

    return {
        "error_code": 500,
        "error": ServerError(str(error)),
    }


def ok(data: Any, file: Optional[Dict[str, Any]] = None) -> HttpResponse:
    resp = data
    if file is not None:
        resp["file"] = file
    return HttpResponse(resp)


def no_content() -> Dict[str, Any]:
    return