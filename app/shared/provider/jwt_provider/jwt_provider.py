import jwt
from jwt import ExpiredSignatureError, InvalidTokenError as PyJwtInvalidTokenError
from datetime import datetime, timedelta
from typing import Union, Any

# Custom error classes to mirror TS counterparts
class ExpiredTokenError(Exception):
    def __init__(self):
        super().__init__("Expired token error")

class InvalidTokenError(Exception):
    def __init__(self):
        super().__init__("Invalid token error")

class JwtProvider:
    """
    Provides JWT encryption and decryption, mirroring the TS JwtProvider.

    encrypt(value, expires_in) -> str
    decrypt(token) -> Union[dict, str, None]
    """
    def __init__(self, secret: str) -> None:
        self.secret = secret

    @staticmethod
    def _parse_expires_in(expires: str) -> datetime:
        """Parses a string like '1d', '12h', '30m', '45s' into a UTC datetime."""
        unit = expires[-1]
        try:
            amount = int(expires[:-1])
        except ValueError:
            raise ValueError(f"Invalid expiresIn format: {expires}")

        kwargs = {}
        if unit == 'd':
            kwargs['days'] = amount
        elif unit == 'h':
            kwargs['hours'] = amount
        elif unit == 'm':
            kwargs['minutes'] = amount
        elif unit == 's':
            kwargs['seconds'] = amount
        else:
            raise ValueError(f"Unknown time unit in expiresIn: {unit}")

        return datetime.utcnow() + timedelta(**kwargs)

    async def encrypt(self, value: str, expires_in: str = '1d') -> str:
        """
        Generates a JWT for { id: value } with expiration.
        """
        exp_time = self._parse_expires_in(expires_in)
        payload = {'id': value, 'exp': exp_time}
        token = jwt.encode(payload, self.secret, algorithm='HS256')
        # PyJWT may return bytes in some versions
        if isinstance(token, bytes):
            token = token.decode('utf-8')
        return token

    async def decrypt(self, token: str) -> Union[dict[str, Any], str, None]:
        """
        Verifies and decodes the JWT.
        On success, returns the decoded payload (dict).
        On expiration, returns 'ExpiredTokenError'.
        On invalid token, returns 'InvalidTokenError'.
        """
        try:
            decoded = jwt.decode(token, self.secret, algorithms=['HS256'])
            return decoded
        except ExpiredSignatureError:
            err = ExpiredTokenError()
            return err.__class__.__name__
        except PyJwtInvalidTokenError:
            err = InvalidTokenError()
            return err.__class__.__name__
