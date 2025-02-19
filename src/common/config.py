from pydantic import BaseModel


class Config(BaseModel):
    # Authentication
    OAUTH_AUTH_ENDPOINT: str = "TODO"
    OAUTH_TOKEN_ENDPOINT: str = "TODO"
    CLIENT_ID: str = "TODO"
    TENANT_ID: str = "TODO"

    # Logging
    LOGGER_LEVEL: str = "INFO"

    # TODO:
    # Add some nice on demand fetching of environment variables from e.g. 
    # azure app configuration to reduce onboarding time for new developers .


config = Config()
