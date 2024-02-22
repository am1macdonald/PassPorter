from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from resolvers.Signup import signup

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
async def signup_response(request):
    signup(request)
    return {"message": "success"}


@app.get("/sign-in", response_class=HTMLResponse)
async def sign_in(request: Request):
    return templates.TemplateResponse(request=request, name="forms/sign-in.jinja2")


@app.get("/forgot-password", response_class=HTMLResponse)
async def forgot_password(request: Request):
    return templates.TemplateResponse(request=request, name="forms/forgot-password.jinja2")


@app.get("/reset-password", response_class=HTMLResponse)
async def reset_password(request: Request):
    return templates.TemplateResponse(request=request, name="forms/reset-password.jinja2")

