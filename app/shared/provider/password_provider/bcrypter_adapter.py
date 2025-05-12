import bcrypt
import asyncio

from app.shared.protocol.result import Result

class BcryptAdapter:
    """
    Asynchronous wrapper around Python's bcrypt library,
    returning a Result[T] for both hash and compare operations.

    Dependencies:
      - pip install bcrypt
    """

    @staticmethod
    async def hash(value: str) -> Result[str]:
        """
        Hashes the provided value with a 16-round salt.
        Returns:
            Result.ok(hash_str) on success,
            Result.fail(exception) on error.
        """
        try:
            # bcrypt.hashpw is CPU-bound; run in threadpool
            salt = bcrypt.gensalt(rounds=16)
            raw_hash = await asyncio.to_thread(bcrypt.hashpw, value.encode('utf-8'), salt)
            hash_str = raw_hash.decode('utf-8')
            return Result.ok(hash_str)
        except Exception as err:
            return Result.fail(err)

    @staticmethod
    async def compare(value: str, hash_str: str) -> Result[bool]:
        """
        Compares a plaintext value against the provided bcrypt hash.
        Returns:
            Result.ok(True|False) on success,
            Result.fail(exception) on error.
        """
        try:
            def _check():
                return bcrypt.checkpw(value.encode('utf-8'), hash_str.encode('utf-8'))

            is_valid = await asyncio.to_thread(_check)
            return Result.ok(is_valid)
        except Exception as err:
            return Result.fail(err)
