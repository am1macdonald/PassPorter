from typing import Annotated

import bcrypt
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import SecretStr

from resolvers.Authorize import Authorize
from resolvers.ResetPassword import PasswordResetResolver
from resolvers.Sign_In import SigninResolver
from resolvers.Sign_Up import SignupResolver

load_dotenv()
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(request=request, name="index.jinja2")


@app.get("/sign-up", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse(request=request, name="forms/sign-up.jinja2",
                                      context={"to_extend": 'index.jinja2'})


@app.post("/sign-up", response_class=HTMLResponse)
async def signup_response(email: Annotated[str, Form()], password: Annotated[SecretStr, Form()],
                          confirm: Annotated[SecretStr, Form()], request: Request):
    return SignupResolver(request, templates).resolve(email, password, confirm)


@app.get("/sign-in", response_class=HTMLResponse)
async def sign_page(request: Request):
    return templates.TemplateResponse(request=request, name="forms/sign-in.jinja2",
                                      context={"to_extend": "index.jinja2"})


@app.post("/sign-in", response_class=HTMLResponse)
async def sign_response(email: Annotated[str, Form()], password: Annotated[SecretStr, Form()], request: Request):
    return SigninResolver(request, templates).resolve(email, password)


@app.get("/forgot-password", response_class=HTMLResponse)
async def forgot_password_page(request: Request):
    return templates.TemplateResponse(request=request, name="forms/forgot-password.jinja2",
                                      context={"to_extend": "index.jinja2"})


@app.post("/forgot-password", response_class=HTMLResponse)
async def forgot_password_response(email: Annotated[str, Form()], request: Request):
    return PasswordResetResolver(request, templates).resolve_request(email)


@app.get("/reset-password/{token_id}", response_class=HTMLResponse)
async def reset_password(request: Request, token_id: SecretStr):
    return PasswordResetResolver(request, templates).resolve_get_reset(token_id)


@app.post("/reset-password", response_class=HTMLResponse)
async def reset_password(uuid: Annotated[SecretStr, Form()], password: Annotated[SecretStr, Form()],
                         confirm: Annotated[SecretStr, Form()], request: Request):
    return PasswordResetResolver(request, templates).resolve_reset_action(uuid, password, confirm)


@app.post("/authorize")
async def authorize(client_id: str, redirect_uri: str, response_type: str, scope: str):
    print(client_id)
    return Authorize()
# client_id=client_id: the application’s client ID (how the API identifies the application)
# redirect_uri=CALLBACK_URL: where the service redirects the user-agent after an authorization code is granted
# response_type=code: specifies that your application is requesting an authorization code grant
# scope=read
