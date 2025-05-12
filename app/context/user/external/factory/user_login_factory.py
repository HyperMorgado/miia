

from fastapi import Request, Response
from app.context.user.controller.user_login_controller import UserLoginController
from app.context.user.external.repository.user_repository import UserRepository
from app.context.user.usecase.login_user_usecase import LoginUserUseCase
from app.main.adapter.logger_adapter import Logger
from app.main.config.database.db import AsyncSessionLocal, SessionLocal
from app.shared.jwt.jwt_util import SECRET_KEY
from app.shared.protocol.controller import AbstractController
from app.shared.provider.jwt_provider.jwt_provider import JwtProvider
from app.shared.provider.password_provider.bcrypter_adapter import BcryptAdapter
from app.shared.provider.password_provider.password_provider import PasswordProvider


async def makeUserLoginFactory(
    request: Request,
    response: Response,
) -> AbstractController:
    """
    Factory function to create an instance of dependences.
    """

    # Instantiate the logger
    logger = Logger()
    userRepository = UserRepository(
        db=AsyncSessionLocal(),
    )
    jwtProvider = JwtProvider(
        SECRET_KEY
    )
    
    passwordProvider = PasswordProvider(
        logger=logger,
        bcrypt_adapter=BcryptAdapter(),
    )

    # Instantiate the register user use case
    loginUserUseCase = LoginUserUseCase(
        userRepository,
        logger,
        passwordProvider,
        jwtProvider,
    )

    # Create and return the controller instance
    controller = UserLoginController(
        logger=logger,
        loginUserUsecase=loginUserUseCase
        # user_factory=user_factory,
        # register_user_usecase=register_user_usecase,
    )

    return controller