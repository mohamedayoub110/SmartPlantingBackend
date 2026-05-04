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
        <style>
          body { text-align:center; font-family:Arial; background:#111; color:#eee; margin:0; padding:20px; }
          img  { max-width:90%; border:3px solid #444; border-radius:8px; }
          #fps { font-size:14px; color:#aaa; margin-top:8px; }
        </style>
      </head>
      <body>
        <h1>Smart Planting ESP32-CAM</h1>
        <img id="feed" src="/latest.jpg">
        <p id="fps">Connecting...</p>
        <script>
          let frames = 0, last = Date.now();
          function refresh() {
            const img = document.getElementById('feed');
            const next = new Image();
            next.onload = function() {
              img.src = next.src;
              frames++;
              const now = Date.now();
              if (now - last >= 1000) {
                document.getElementById('fps').textContent = frames + ' fps';
                frames = 0; last = now;
              }
              setTimeout(refresh, 50);
            };
            next.onerror = function() { setTimeout(refresh, 500); };
            next.src = '/latest.jpg?t=' + Date.now();
          }
          refresh();
        </script>
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