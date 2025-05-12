from typing import Protocol, runtime_checkable

from sqlalchemy import select
from app.context.user.external.model.user_model import UserModel


@runtime_checkable
class AbstractUserRepository(Protocol):
    async def by_email(self, email: str) -> UserModel | None: ...
    async def registerUser(self, user: UserModel) -> UserModel: ...
    async def userExists(self, email: str) -> bool: ...
    
class UserRepository(AbstractUserRepository):
    def __init__(self, db):
        self.db = db

    async def by_email(self, email: str) -> UserModel | None:
        user = await self.db.query(UserModel).filter(UserModel.email == email).first()
        return user
    
    async def by_document(self, document: str) -> UserModel | None:
        stmt = select(UserModel).where(UserModel.document == document)
        result = await self.db.execute(stmt)
        return result.scalars().first()
    
    async def userExists(self, email: str) -> bool:
        user = await self.by_email(email)
        return user is not None

    async def registerUser(self, user: UserModel) -> UserModel:
        self.db.add(user)
        await self.db.commit()
        # await self.db.refresh(user)
        return user