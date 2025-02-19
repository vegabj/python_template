from fastapi import HTTPException, Request, Security
from fastapi.security import APIKeyCookie, OAuth2AuthorizationCodeBearer
from jwt import DecodeError, InvalidSignatureError, PyJWKClient, decode
from pydantic import BaseModel

from src.common.config import config

cookie_scheme = APIKeyCookie(name="access_token", auto_error=False)
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=config.OAUTH_AUTH_ENDPOINT,
    tokenUrl=config.OAUTH_TOKEN_ENDPOINT,
    scopes={f"api://{config.CLIENT_ID}/.default": "default"},
    auto_error=False,
)


class User(BaseModel):
    user_id: str
    roles: list[str] = []


def auth_with_jwt(
    request: Request,
    bearer_token: str = Security(oauth2_scheme),
    access_token: str = Security(cookie_scheme),
) -> User:
    token = bearer_token or access_token
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")
    decoded_jwt = _get_decoded_jwt(token)
    return User(user_id=decoded_jwt.get("oid"), roles=decoded_jwt.get("roles", []))


def _get_azure_sign_keys() -> PyJWKClient:
    jwks_uri = "https://login.microsoftonline.com/common/discovery/v2.0/keys"
    return PyJWKClient(jwks_uri, cache_jwk_set=True, lifespan=86400)


def _get_decoded_jwt(token: str):
    token = token.replace("Bearer ", "")

    audience = [f"api://{config.CLIENT_ID}"]
    issuer = f"https://login.microsoftonline.com/{config.TENANT_ID}/"

    azure_sign_keys = _get_azure_sign_keys()
    signing_key = azure_sign_keys.get_signing_key_from_jwt(token).key
    try:
        return decode(
            token, signing_key, audience=audience, issuer=issuer, algorithms=["RS256"]
        )
    except InvalidSignatureError as e:
        raise HTTPException(status_code=401, detail="Invalid token signature") from e
    except DecodeError as e:
        raise HTTPException(status_code=401, detail="Could not decode token") from e
