from fastapi import APIRouter, Request, Response
from app.context.user.external.factory.user_login_factory import makeUserLoginFactory
from app.context.user.external.factory.user_register_factory import makeUserRegisterFactory
from app.main.adapter.logger_adapter import logger
from fastapi import APIRouter, Depends
from app.main.adapter.auth import get_current_user

userRouter = APIRouter(
    prefix="/user",               # ← here!
    tags=["user"],                # optional, but helps in the auto-docs
    # dependencies=[Depends(get_current_user)],  # if you want auth on *every* endpoint
)

@userRouter.post("/register")
# current_user: dict = Depends(get_current_user)
async def registerUser(
    request: Request, response: Response
):
    # it's a not good practice. 
    # The correct wait is send makeUserRegisterFactory for a middleware and the middleware will call the controller, 
    # but for now it's ok because is A TEST
    controller = await makeUserRegisterFactory(request, response)
    await controller.execute(request,response)
    return {}

@userRouter.post("/login")
async def loginUser(
    request: Request, response: Response
):
    # it's a not good practice. 
    # The correct wait is send makeUserLoginFactory for a middleware and the middleware will call the controller, 
    # but for now it's ok because is A TEST
    controller = await makeUserLoginFactory(request, response)
    result = await controller.execute(request,response)
    return result