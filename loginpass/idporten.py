"""
    loginpass.idporten
    ~~~~~~~~~~~~~~~

    Loginpass Backend of UiO

    :copyright: (c) 2019 by UiO
    :license: AGPLv3+, see LICENSE for more details.
"""
from ._core import OAuthBackend, parse_id_token
import requests


def create_idporten_backend(name, host, kontaktinfo=True, reauthentication=True):

    class IDPorten(OAuthBackend):
        OAUTH_TYPE = '2.0,oidc'
        OAUTH_NAME = name
        scope = "openid user/kontaktinformasjon.read" if kontaktinfo else "openid"
        OAUTH_CONFIG = {
            'api_base_url': host,
            'access_token_url': 'https://{}/idporten-oidc-provider/token'.format(host),
            'authorize_url': 'https://{}/idporten-oidc-provider/authorize'.format(host),
            'client_kwargs': {'scope': scope, 
                              'prompt': 'login' if reauthentication else 'none'},
            # 'acr_values': 'Level4'},
        }
        ISS_URL = 'https://{}/idporten-oidc-provider/'.format(host)
        KONTAKTINFO_URL = 'https://{}/kontaktinfo-oauth2-server/rest/v1/person'.format(host)
        JWK_SET_URL = 'https://{}/idporten-oidc-provider/jwk'.format(host)
        ENDSESSION_URL = 'https://{}/idporten-oidc-provider/endsession'.format(host)
    
        def parse_openid(self, token, nonce=None, val_login=False):
            id_token_content = parse_id_token(
                    self, token['id_token'],
                    {"iss": {"values": [self.ISS_URL]}},
                    # {},
                    token.get('access_token'), nonce
                    )
            if kontaktinfo and not val_login:
                headers = {
                    'authorization': "Bearer {}".format(token['access_token']),
                    'Accept': 'application/json'
                }
                response = requests.get(self.KONTAKTINFO_URL, headers=headers)
                return response.json()
            else:
                return id_token_content

    return IDPorten


IDPorten = create_idporten_backend('idporten', 'oidc.difi.no')
