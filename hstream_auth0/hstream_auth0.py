from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from hstream.components import component_wrapper

AUTH0_DOMAIN = 'dev-fs6qumz9.us.auth0.com'

config = Config('.env')  # read config from .env file
oauth = OAuth(config)
oauth.register(
    name='auth0',
    server_metadata_url=f'https://{AUTH0_DOMAIN}/.well-known/openid-configuration',
    client_kwargs={
        # 'scope': 'openid email profile'
        'scope': 'read:current_user',
        'audience':f'https://{AUTH0_DOMAIN}/api/v2/',
    }
)



def auth_setup(hs):
    from fastapi import FastAPI
    from starlette.middleware.sessions import SessionMiddleware
    if not 'SessionMiddleware' in str(hs.app.user_middleware):
        # we only add the middleware once, otherwise we wipe out the cookies
        hs.app = FastAPI()
        hs.app.add_middleware(SessionMiddleware, secret_key="secret-string")
    else:
        print('SessionMiddleware already added')
    @hs.app.route('/login')
    async def login(request):
        # absolute url for callback
        # we will define it below
        redirect_uri = str(request.url_for('callback'))
        print(redirect_uri)
        # return await oauth.auth0.authorize_access_token(request)
        return await oauth.auth0.authorize_redirect(
                    redirect_uri=redirect_uri, request=request
                )
        # return await oauth.auth0.authorize_redirect(request, redirect_uri)
    
    @hs.app.route('/callback')
    async def callback(request):
        user = await oauth.auth0.authorize_access_token(request)
        token = user['access_token']
        html = """
        <script>
        function sendUserInfoBack(token) {
                let url = `/value_changed/hstreamauth0`
                fetch(url, {
                method: 'POST',
                body: new URLSearchParams({
                    'hstreamauth0': token
                })
                })
            }
            sendUserInfoBack("TOKEN")
            window.location.href = "/";
            </script>
        """.replace('TOKEN', str(token))
        print(token)
        # return RedirectResponse("/")
        return HTMLResponse(html)

    return hs

@component_wrapper
def auth(hs, *args, **kwargs):
    with hs.html('a', href='/login'):
        hs.markdown('Login')

# def login_button():

#     token = await oauth.auth0.authorize_access_token(request)