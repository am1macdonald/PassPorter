from typing import Annotated

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from resolvers.Sign_Up import SignupResolver

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(request=request, name="index.jinja2")


@app.get("/sign-up", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse(request=request, name="forms/sign-up.jinja2")


@app.post("/sign-up", response_class=HTMLResponse)
async def signup_response(email: Annotated[str, Form()], password: Annotated[str, Form()],
                          confirm: Annotated[str, Form()], request: Request):
    SignupResolver(request)
    print(email)
    return templates.TemplateResponse(request=request, name="views/signup_success.jinja2")


@app.get("/sign-in", response_class=HTMLResponse)
async def sign_in(request: Request):
    return templates.TemplateResponse(request=request, name="forms/sign-in.jinja2")


@app.get("/forgot-password", response_class=HTMLResponse)
async def forgot_password(request: Request):
    return templates.TemplateResponse(request=request, name="forms/forgot-password.jinja2")


@app.get("/reset-password", response_class=HTMLResponse)
async def reset_password(request: Request):
    return templates.TemplateResponse(request=request, name="forms/reset-password.jinja2")
