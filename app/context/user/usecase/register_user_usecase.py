
from app.context.user.domain.dto.user_register_dto import RegisterUserDTO
from app.context.user.external.model.user_model import UserModel
from app.context.user.external.repository.user_repository import AbstractUserRepository
from app.main.adapter.logger_adapter import Logger
from app.shared.protocol.result import Result
from app.shared.provider.password_provider.password_provider import PasswordProvider


class RegisterUserUseCase:
    def __init__(
        self, 
        userRepository: AbstractUserRepository, 
        logger: Logger, 
        passwordProvider: PasswordProvider):
        self.userRepository = userRepository
        self.logger = logger
        self.passwordProvider = passwordProvider

    async def execute(self, user: RegisterUserDTO) -> Result[any]:
        
        try:
            passwordResult = await self.passwordProvider.hash(user.password)
            
            if passwordResult.error:
                raise ValueError("Error hashing password")
            
            hashed_password = passwordResult.get_value().get("hash")
            salt = passwordResult.get_value().get("salt")

            
            # Register the user
            user_model = UserModel(
                name=user.name,
                email=user.email,
                password=hashed_password,
                salt=salt,
                document=user.document,
            )
            await self.userRepository.registerUser(user_model)
            return Result.ok()
        except Exception as e:
            self.logger.error(f"Error during user registration: {str(e)}")
            
            return Result.fail(f"Error during user registration: {str(e)}")
        

    def validate_user_data(self, user_data):
        # Implement validation logic here
        return True