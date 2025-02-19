from asyncio import create_task
from contextlib import asynccontextmanager

from fastapi import FastAPI, Security

from src.common.authentication import auth_with_jwt
from src.common.config import config
from src.routes.prediction_router import prediction_router
from src.routes.cached_router import cached_router
from src.background_worker import SampleBackgroundWorker


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load model
    # app.state.prediction_model = InferenceSession("my_model.onnx")
    # Run background task
    create_task(SampleBackgroundWorker().run())
    yield


app = FastAPI(
    title="My FastApi template",
    description="",
    swagger_ui_oauth2_redirect_url="/swagger/oauth2-redirect",
    swagger_ui_init_oauth={
        "usePkceWithAuthorizationCodeGrant": True,
        "clientId": config.CLIENT_ID,
    },
    lifespan=lifespan,
)


app.include_router(
    prediction_router, prefix="/api", dependencies=[Security(auth_with_jwt)]
)
app.include_router(
    cached_router, prefix="/api", dependencies=[Security(auth_with_jwt)]
)
