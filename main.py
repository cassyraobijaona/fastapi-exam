from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
import yaml

app = FastAPI()

with open("main.yaml", "r") as f:
    main_yaml = yaml.safe_load(f)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    app.openapi_schema = main_yaml
    return app.openapi_schema


app.openapi = custom_openapi


@app.get("/ping")
def ping():
    return {"message": "pong"}
