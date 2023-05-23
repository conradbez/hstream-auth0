from hstream import hs
from hstream_auth0 import auth, auth_setup

hs = auth_setup(hs)
token = auth(hs, key = 'hstreamauth0')
print(token)
h = hs.text_input('test', )
hs.markdown(h)
hs.markdown(token)
hs.markdown("here")