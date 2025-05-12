

from fastapi import Request, Response
from app.context.user.controller.user_register_controller import UserRegisterController
from app.context.user.external.repository.user_repository import UserRepository
from app.context.user.usecase.register_user_usecase import RegisterUserUseCase
from app.main.adapter.logger_adapter import Logger
from app.main.config.database.db import SessionLocal
from app.shared.protocol.controller import AbstractController
from app.shared.provider.password_provider.bcrypter_adapter import BcryptAdapter
from app.shared.provider.password_provider.password_provider import PasswordProvider


async def makeUserRegisterFactory(
       request: Request, 
       response: Response
    ) -> AbstractController:
    """
    Factory function to create an instance of dependences.
    """

    # Instantiate the logger
    logger = Logger()
    userRepository = UserRepository(
        db=SessionLocal(),
    )
    passwordProvider = PasswordProvider(
        logger=logger,
        bcrypt_adapter=BcryptAdapter(),
    )

    # Instantiate the register user use case
    registerUserUseCase = RegisterUserUseCase(
        userRepository,
        logger,
        passwordProvider=passwordProvider,
    )

    # Create and return the controller instance
    controller = UserRegisterController(
        logger=logger,
        registerUserUsecase=registerUserUseCase,
        # user_factory=user_factory,
        # register_user_usecase=register_user_usecase,
    )
    
    return controller