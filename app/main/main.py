from fastapi import APIRouter, FastAPI
from app.main.config.server.server import configure_app
from app.main.config.database.db import init_db
from app.main.adapter.logger_adapter import logger
from app.context.hello.routes import router as hello_router
from app.context.user.external.route.user_route import userRouter

api_v1 = APIRouter(prefix="/api/v1")


app = FastAPI()

# Middlewares (CORS etc.)
configure_app(app)

# Rota /api
api_v1.include_router(hello_router)
api_v1.include_router(userRouter)
app.include_router(api_v1)


# Teste de conexão com Banco
init_db()


logger.info("Application startup complete")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)