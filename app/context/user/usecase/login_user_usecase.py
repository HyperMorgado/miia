

import json
from app.context.user.external.model.user_model import UserModel
from app.context.user.external.repository.user_repository import UserRepository
from app.shared.protocol.result import Result
from app.shared.provider.jwt_provider.jwt_provider import JwtProvider
from app.shared.provider.password_provider.password_provider import PasswordProvider


class LoginUserUseCase:
    """
    Use case for logging in a user.
    """

    def __init__(self, user_repository: UserRepository, logger, password_provider: PasswordProvider, jwtProvider: JwtProvider ):
        self.user_repository = user_repository
        self.logger = logger
        self.password_provider = password_provider
        self.jwtProvider = jwtProvider

    async def execute(self, document: str, password: str) -> Result[UserModel]:
        """
        Execute the use case to log in a user.
        """
        # Log the start of the login process
        self.logger.info(f"Starting login process for document: {document}")

        # Fetch the user from the repository
        user = await self.user_repository.by_document(document)

        # Check if the user exists
        if not user:
            self.logger.warning(f"User not found for document: {document}")
            return Result.fail("User not found")

        # Verify the password
        
        compareResult = await self.password_provider.compare(password, user.salt, user.password)
        
        if not compareResult.get_value():
            self.logger.warning(f"Invalid password for document: {document}")
            return Result.fail("Invalid password")

        # Log successful login
        self.logger.info(f"User logged in successfully for document: {document}")
        
        token_payload = {
            "id": user.id,
            "type": "TOKEN",
        }
        refresh_payload = {
            "id": user.id,
            "type": "REFRESH",
        }
        
        token = await self.jwtProvider.encrypt(json.dumps(token_payload), "30d")
        refresh = await self.jwtProvider.encrypt(json.dumps(refresh_payload), "30d")

        return Result.ok({
            "token": token,
            "refresh": refresh
        })
       
       
       
       