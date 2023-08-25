import os
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory=os.getcwd() + "\\..\\web\\pages\\")


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("feedback_form.html", {"request": request})


async def run_web():
    config = uvicorn.Config(f"{__name__}:app", port=8080, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8080)