from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from resolvers.Signup import signup

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def root(request: Request):
    return {'message': 'wow'}

@app.get("/sign-up", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse(request=request, name="forms/signup.jinja2")

@app.post("/sign-up", response_class=HTMLResponse)
async def signup_response(request):
    signup(request)
    return {"message": "success"}


@app.get("/sign-in", response_class=HTMLResponse)
async def say_hello():
    with open("templates/fragments/floater.html", 'r') as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)


@app.get("/reset-password", response_class=HTMLResponse)
async def say_hello():
    with open("templates/fragments/floater.html", 'r') as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)
