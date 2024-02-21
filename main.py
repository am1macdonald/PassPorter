from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from controllers.TemplateController import get_thing

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(request=request, name="index.jinja2", context={"mom": "mom", 'content': get_thing('fragments/floater.jinja2')})


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
