from typing import Optional
from fastapi import Response
from app.context.user.domain.dto.user_login_dto import UserLoginDTO
from app.context.user.external.model.user_model import UserModel
from app.context.user.usecase.login_user_usecase import LoginUserUseCase
from app.main.config.server.http import HttpRequest
from app.shared.protocol.controller import AbstractController
from app.shared.protocol.result import Result


class UserLoginController(AbstractController):
    """
    Controller for user login.
    """

    def __init__(self, logger, loginUserUsecase: LoginUserUseCase):
        self.logger = logger
        self.loginUserUsecase = loginUserUsecase

    async def handle(self, request: HttpRequest, response: Optional[Response]) -> Response:
        """
        Handle the user login request.
        """
        # Extract the user data from the request
        userLoginDto: UserLoginDTO = UserLoginDTO(**request.body)

        # Call the use case to login the user
        result: Result[UserModel] = await self.loginUserUsecase.execute(userLoginDto.document, userLoginDto.password)

        self.logger.info(f"Login attempt for user: {userLoginDto.document}, result: {result}")

        # Return the result as a JSON response
        response.body = result.get_value()
        # response.status_code = 200 if result.is_success() else 401
        
        if result.get_value() is None:
            response.body = {"error": result.error}
            response.status_code = 401
            return Result.fail()
        else:
            return result.get_value()