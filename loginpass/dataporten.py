"""
    loginpass.dataporten
    ~~~~~~~~~~~~~~~

    Loginpass Backend of Datporten

    :copyright: (c) 2019 by UiO
    :license: AGPLv3+, see LICENSE for more details.
"""
from ._core import OAuthBackend, parse_id_token
import requests


def create_dataporten_backend(name, scope="openid profile userid groups userid-feide", groups=True):

    class Dataporten(OAuthBackend):
        OAUTH_TYPE = '2.0,oidc'
        OAUTH_NAME = 'dataporten'
        OAUTH_CONFIG = {
            'api_base_url': 'https://groups-api.dataporten.no',
            'access_token_url': 'https://auth.dataporten.no/oauth/token',
            'authorize_url': 'https://auth.dataporten.no/oauth/authorization',
            'client_kwargs': {'scope': scope},
            # 'client_kwargs': {'scope': 'openid'},
            # 'acr_values': 'Level4'},
        }
        HOST = 'https://auth.dataporten.no'
        USERINFO_URL = 'https://auth.dataporten.no/openid/userinfo'
        JWK_SET_URL = 'https://auth.dataporten.no/openid/jwks'
        ENDSESSION_URL = 'https://auth.dataporten.no/logout'

        def parse_openid(self, token, nonce=None, val_login=False):
            print(token)
            access_token = token.get('access_token')
            id_token_content = parse_id_token(
                self, token['id_token'],
                {"iss": {"values": [self.HOST]}},
                access_token, nonce
                )
            print("ID_TOKEN_CONTENT: ")
            print(id_token_content)
            if groups and not val_login:
                headers = {
                    'authorization': "Bearer {}".format(token['access_token']),
                    'Accept': 'application/json'
                }
                response = requests.get(self.USERINFO_URL, headers=headers)
                print(response.text)
                return response.json()
            else:
                return id_token_content

    return Dataporten


Dataporten = create_dataporten_backend('dataporten')
