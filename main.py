from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse, FileResponse
import os

app = FastAPI()

UPLOAD_PATH = "latest.jpg"

@app.get("/")
def home():
    return HTMLResponse("""
    <html>
      <head>
        <title>Smart Planting Camera</title>
        <meta http-equiv="refresh" content="2">
      </head>
      <body style="text-align:center; font-family:Arial;">
        <h1>Smart Planting ESP32-CAM</h1>
        <img src="/latest.jpg" style="max-width:90%; border:2px solid black;">
        <p>Auto-refreshes every 2 seconds</p>
      </body>
    </html>
    """)

@app.post("/upload")
async def upload_image(image: UploadFile = File(...)):
    with open(UPLOAD_PATH, "wb") as f:
        f.write(await image.read())
    return {"status": "received"}

@app.get("/latest.jpg")
def latest_image():
    if os.path.exists(UPLOAD_PATH):
        return FileResponse(UPLOAD_PATH, media_type="image/jpeg")
    return HTMLResponse("<h2>No image uploaded yet</h2>")