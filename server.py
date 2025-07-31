import os
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from rembg import remove
from PIL import Image
import io

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "https://bgerasee.netlify.app/",
    "https://*.netlify.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    input_image = Image.open(file.file).convert("RGBA")
    output_image = remove(input_image)

    output_bytes = io.BytesIO()
    output_image.save(output_bytes, format="PNG")
    output_bytes.seek(0)

    return StreamingResponse(output_bytes, media_type="image/png")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("server:app", host="0.0.0.0", port=port)