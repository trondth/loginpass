"""
    loginpass.idporten
    ~~~~~~~~~~~~~~~

    Loginpass Backend of Azure AD.

    :copyright: (c) 2018 by Hsiaoming Yang
    :license: AGPLv3+, see LICENSE for more details.
"""

from authlib.specs.oidc import UserInfo
from ._core import OAuthBackend, parse_id_token


def create_idporten_backend(name):
    """Build Azure Active Directory OAuth Backend."""

    base_url = 'https://oidc-ver1.difi.no/'
    prefix = 'idporten-oidc-provider'

    authorize_url = '{}/{}/authorize'.format(base_url, prefix)
    token_url = '{}/{}/token'.format(base_url, prefix)

    class IDPorten(OAuthBackend):
        OAUTH_TYPE = '2.0,oidc'
        OAUTH_NAME = name
        OAUTH_CONFIG = {
            'api_base_url': 'graph.microsoft.com',
            'access_token_url': token_url,
            'authorize_url': authorize_url,
            'client_kwargs': {'scope': 'openid profile', 
                'acr_values': 'Level4'},
        }
        JWK_SET_URL = '{}/{}/discovery/keys'.format(base_url, prefix)

        def profile(self, **kwargs):
            url = '{}/{}/userinfo'.format(base_url, prefix)
            resp = self.get(url, **kwargs)
            resp.raise_for_status()
            return UserInfo(**resp.json())

        def parse_openid(self, token, nonce=None):
            return parse_id_token(
                self, token['id_token'], jwt_claims_options,
                token.get('access_token'), nonce
            )

    return IDPorten


Idporten = create_idporten_backend('idporten')
