import uuid
from typing import Dict

from app.main.adapter.logger_adapter import Logger
from app.shared.protocol.result import Result
from app.shared.provider.password_provider.bcrypter_adapter import BcryptAdapter


class PasswordProvider:
    """
    Implements IPasswordProvider:
      - hash(value) -> Result[{'hash': str, 'salt': str}]
      - compare(value, salt, hash) -> Result[bool]

    Dependencies:
      - Logger: for optional logging
      - BcryptAdapter: async bcrypt wrapper returning Result
    """
    def __init__(self, logger: Logger, bcrypt_adapter: BcryptAdapter) -> None:
        self.logger = logger
        self.bcrypt_adapter = bcrypt_adapter

    async def hash(self, value: str) -> Result[Dict[str, str]]:
        """
        Generates a random UUID as salt, prepends it to the value, and hashes.
        Returns:
            Result.ok({'hash': str, 'salt': str}) on success,
            Result.fail(Exception) on error.
        """
        try:
            salt = uuid.uuid4().hex
            combined = f"{salt}{value}"
            result = await self.bcrypt_adapter.hash(combined)

            if result.is_failure:
                return Result.fail(result.error)

            return Result.ok({
                'hash': result.get_value(),
                'salt': salt,
            })
        except Exception as err:
            return Result.fail(err)

    async def compare(self, value: str, salt: str, hash_str: str) -> Result[bool]:
        """
        Prepends salt to the value and compares to the provided hash.
        Returns:
            Result.ok(True|False) on success,
            Result.fail(Exception) on error.
        """
        try:
            combined = f"{salt}{value}"
            result = await self.bcrypt_adapter.compare(combined, hash_str)

            if result.is_failure:
                return Result.fail(result.error)

            return Result.ok(result.get_value())
        except Exception as err:
            return Result.fail(err)
