"""
    loginpass.idporten
    ~~~~~~~~~~~~~~~

    Loginpass Backend of Azure AD.

    :copyright: (c) 2018 by Hsiaoming Yang
    :license: AGPLv3+, see LICENSE for more details.
"""

from ._core import UserInfo, OAuthBackend


class IDPorten(OAuthBackend):
    OAUTH_TYPE = '2.0'
    OAUTH_NAME = 'idporten'
    OAUTH_CONFIG = {
        'api_base_url': 'https://oidc-ver1.difi.no/',
        'access_token_url': 'https://oidc-ver1.difi.no/idporten-oidc-provider/token"',
        'authorize_url': 'https://oidc-ver1.difi.no/idporten-oidc-provider/authorize',
        'client_kwargs': {'scope': 'openid profile'},
        # 'acr_values': 'Level4'},
    }
    # JWK_SET_URL = '{}/{}/discovery/keys'.format(base_url, prefix)

    def profile(self, **kwargs):
        resp = self.get('user', **kwargs)
        resp.raise_for_status()
        data = resp.json()
        params = {
            'sub': str(data['id']),
            'name': data['name'],
            'email': data.get('email'),
            'preferred_username': data['login'],
            'profile': data['html_url'],
            'picture': data['avatar_url'],
            'website': data.get('blog'),
        }
        return UserInfo(params)


    # def parse_openid(self, token, nonce=None):
    #     return parse_id_token(
    #         self, token['id_token'],
    #         {"iss": {"values": [base_url]} },
    #         token.get('access_token'), nonce
    #     )
