from types import resolve_bases
import requests
from starlette.responses import Response
import uvicorn
from fastapi import FastAPI
from starlette.requests import Request
from src.utils.restful import success, error
import io
from starlette.responses import StreamingResponse
import base64
import numpy as np
import urllib
import cv2

app = FastAPI()


@app.get("/api")
async def index(request: Request):
    print(request.headers)
    print(request.headers.get("user-agent"))
    ip = request.client.host
    port = request.client.port

    return success(data=str(ip) + ":" + str(port))


@app.get("/robot")
async def read_root():
    version = 3.8
    message = f"Hello world! From FastAPI running on Uvicorn with Gunicorn. Using Python {version}"
    return {"message": message}


@app.get("/check")
async def get_ip():
    url = "https://api.kuku.me/tool/peeping/check/1351"
    resp = requests.get(url)
    file = open(r"cover.png", "rb")
    return StreamingResponse(io.BytesIO(file.read()), media_type="image/png")


if __name__ == "__main__":
    # CONFIG_PATH = Path(".") / "config.yml"
    # config = load_yaml(CONFIG_PATH)["api"]
    uvicorn.run(app, host="0.0.0.0", port=8082)

