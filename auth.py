from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
import os

router = APIRouter()

config = Config(environ={
    'GOOGLE_CLIENT_ID': os.getenv("GOOGLE_CLIENT_ID"),
    'GOOGLE_CLIENT_SECRET': os.getenv("GOOGLE_CLIENT_SECRET")
})

oauth = OAuth(config)
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={}
)

@router.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for('auth_callback')
    return await oauth.google.authorize_redirect(
        request,
        redirect_uri,
        scope="openid email profile"
    )

@router.get("/auth/callback")
async def auth_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)

    # Prefer userinfo for simplicity and reliability
    resp = await oauth.google.get("https://www.googleapis.com/oauth2/v3/userinfo", token=token)
    user_info = resp.json()

    request.session['user'] = {
        'id': user_info['sub'],
        'email': user_info['email'],
        'name': user_info['name']
    }

    return RedirectResponse(url="/")
