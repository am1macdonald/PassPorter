from typing import Annotated

from dotenv import load_dotenv
from fastapi import FastAPI, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import SecretStr, BaseModel

from models.Token import TokenRequest
from resolvers.Authorize import Authorize
from resolvers.Consent import ConsentResolver
from resolvers.GetToken import GetTokenResolver
from resolvers.Redirect import RedirectResolver
from resolvers.ResetPassword import PasswordResetResolver
from resolvers.Sign_In import SigninResolver
from resolvers.Sign_Up import SignupResolver

load_dotenv()
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(request=request, name="index.jinja2")


@app.get("/sign-up", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse(request=request, name="forms/sign-up.jinja2",
                                      context={"to_extend": 'index.jinja2', "query_params": f"{request.query_params}"})


@app.post("/sign-up", response_class=HTMLResponse)
async def signup_response(email: Annotated[str, Form()], password: Annotated[SecretStr, Form()],
                          confirm: Annotated[SecretStr, Form()], request: Request):
    return SignupResolver(request, templates).resolve(email, password, confirm)


@app.get("/sign-in", response_class=HTMLResponse)
async def sign_in_page(request: Request):
    swap = True
    if request.query_params.get("client_id"):
        swap = False
    response = templates.TemplateResponse(request=request, name="forms/sign-in.jinja2",
                                          context={"to_extend": "index.jinja2", "query_params": request.query_params,
                                                   "swap": swap})
    response.headers.update({
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache",
        "Expires": "0"
    })
    return response


@app.post("/sign-in", response_class=HTMLResponse)
async def sign_in_response(email: Annotated[str, Form()], password: Annotated[SecretStr, Form()], request: Request):
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


@app.get("/authorize")
async def authorize(request: Request, client_id: str, redirect_uri: str, response_type: str, scope: str):
    return Authorize(request, templates).resolve_get(client_id, redirect_uri, response_type, scope)


@app.post("/authorize")
async def authorize(authorized: Annotated[str, Form()], request: Request):
    return Authorize(request, templates).resolve_post(authorized)


@app.get("/consent")
async def allow_access(request: Request):
    return ConsentResolver(request, templates).resolve_get()


@app.get("/redirect")
async def allow_access(request: Request):
    return RedirectResolver(request).resolve()


@app.post("/get-token")
async def get_token(request: Request, item: TokenRequest):
    return GetTokenResolver(request, templates).resolve(item)
