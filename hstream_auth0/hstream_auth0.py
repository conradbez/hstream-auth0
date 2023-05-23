from starlette.responses import FileResponse 
import os
from hstream.components import component_wrapper, ComponentsGeneric
from pathlib import Path
# from hstream.components import Components
@component_wrapper
def getToken(hs, *args, **kwargs):
        try:
            assert kwargs['key'] == 'auth0'
        except:
            raise ValueError('key must be hstreamauth0, please use `getToken(hs, key = "auth0")`')
        f = open(Path(__file__).parent  / "index.html","r")
        lines = f.readlines()
        html = ''.join(lines)
        html = html.replace('{{DOMAIN}}', 'dev-fs6qumz9.us.auth0.com')
        html = html.replace('{{CLIENT_ID}}', '3YqE0osoSb4ahj4oNcGKTh1P7gIe9Sgl')
        hs.doc.asis(html)
        
        @hs.app.get("/callback")
        async def callback():
            """
            This is the callback route that will set the auth0 token once the server has authenticated the user
            """
            auth0_html_file = Path(__file__).parent  / "callback.html"
            return FileResponse(auth0_html_file)

def getUserInfo(token, domain):
    if not token or len(token) < 10:
        return False

    domain = "https://"+domain
    if domain[-13:] != '.us.auth0.com':
        print('domain should end with ".us.auth0.com" (no slash)')
        raise ValueError
    
    from six.moves.urllib.request import urlopen
    import json
    from functools import wraps
    from jose import jwt
    jsonurl = urlopen(domain+"/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}

    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=["RS256"],
                audience=domain+"/api/v2/",
                issuer=domain+'/'
            )
        except jwt.ExpiredSignatureError:
            raise 
        except jwt.JWTClaimsError:
            raise 
        except Exception:
            raise 
        return payload
        return payload['sub']
    
    # example
    #     try:
    #         t = ""
    #         token = token[1:-1] # remove "" from string
    #         print(token)
    #         sub = getVerifiedSubFromToken(token, domain='dev-fs6qumz9.us.auth0.com')
    #         print(sub)
    #     except:
    #         print('fail')

