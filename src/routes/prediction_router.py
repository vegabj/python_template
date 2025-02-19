from fastapi import APIRouter, Request, Response

prediction_router = APIRouter(tags=["Prediction"])


@prediction_router.get("/health")
async def health(request: Request):
    return {"status": "ok" if request.state.get("prediction_model") else "not ready"}


@prediction_router.post("/predict")
async def predict(request: Request, features: dict):
    if "prediction_model" not in request.state:
        return Response("Model not loaded", status_code=500)
    return request.state["prediction_model"].run(None, {"input": features})
