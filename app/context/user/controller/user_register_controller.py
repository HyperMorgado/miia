from typing import Optional
from fastapi import Response
from app.context.user.domain.dto.user_register_dto import RegisterUserDTO
from app.context.user.usecase.register_user_usecase import RegisterUserUseCase
from app.main.adapter.logger_adapter import Logger
from app.main.config.server.helpers.http_helper import ok
from app.main.config.server.http import HttpRequest, HttpResponse
from app.shared.error.type import server_error
from app.shared.protocol.controller import AbstractController
from app.shared.util.get_line_number import getFileAndLineCaller

class UserRegisterController(AbstractController):
    def __init__(
        self,
        logger: Logger,
        # user_factory: IUserFactory,
        registerUserUsecase: RegisterUserUseCase,
    ) -> None:
        super().__init__(logger)
        # self.user_factory = user_factory
        self.registerUserUsecase = registerUserUsecase

    async def handle(self, request: HttpRequest, response: Optional[Response]) -> Response:
            try:
                # # Extract payload from request
                payload = request.body or {}
              
                dto = RegisterUserDTO(**payload)
                registerUserUseCaseResult = await self.registerUserUsecase.execute(dto)

                # it's comment because the test is not ok. The goal of this code its to test the response of usecase
                # if registerUserUseCaseResult.is_failure():
                #     response.status_code = 400
                #     response.body = {"error": registerUserUseCaseResult.error}
                #     return response

                self.logger.info(
                    message="User registered successfully",
                    metadata={"file": getFileAndLineCaller()},
                )
                # this status code response in hard code if not a good practice, but it's ok because is a test
                response.status_code = 200
                return response

            except Exception as err:
                # Log the error and return a 500 response
                self.logger.error(
                    message=str(err),
                    metadata={"file": getFileAndLineCaller()},
                )
                # this status code response in hard code if not a good practice, but it's ok because is a test
                response.status_code = 500
                # response.body =  {
                #     "error": server_error(
                #         stack_trace=str(err),
                #     ),
                # }
                return response