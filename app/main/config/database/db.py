# from sqlalchemy import create_engine, text
# from sqlalchemy.orm import sessionmaker
# from app.main.adapter.logger import logger
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine



# # Ajuste conforme suas credenciais
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost:5432/dbname"

# # Cria engine e sessão
# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# def init_db():
#     try:
#         # Testa conexão básica
#         with engine.connect() as conn:
#             conn.execute(text("SELECT 1"))
#         # Testa conexão com o banco de dados
#         logger.info("Database connection successful")
#     except Exception as e:
#         logger.error(f"Database connection failed: {e}")
#         raise

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.main.adapter.logger_adapter import logger

# Ajuste conforme suas credenciais
SQLALCHEMY_DATABASE_URL = "postgresql://1XZpQoTgk34MdLH8xW5Y:9YkdwRuTnJc2Boqx4EhV@localhost:5443/miia_db"
ASYNC_DATABASE_URL = "postgresql+asyncpg://1XZpQoTgk34MdLH8xW5Y:9YkdwRuTnJc2Boqx4EhV@localhost:5443/miia_db"


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,
    future=True,
)
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
) 
 

def init_db():
    try:
        with engine.connect() as conn:
             conn.execute(text("SELECT 1"))
        logger.info("Database connection successful")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise

Base = declarative_base()