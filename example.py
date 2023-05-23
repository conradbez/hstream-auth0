from hstream import hs
from hstream_auth0 import getToken, getUserInfo

hs.nav(['Home'], 0)

token = getToken(hs, key = "auth0")
user = getUserInfo(token, 'dev-fs6qumz9.us.auth0.com', )

if user:
    hs.markdown(user['sub'])