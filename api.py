import asyncio
import uvicorn
import base64
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware  # CORS
import cv2

app = FastAPI()

# CORS
origins = [
    "http://192.168.110.164:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

connected_websockets = set()

async def send_camera_image(websocket):
    cap = cv2.VideoCapture(0)  # 0번 카메라를 사용합니다. 다른 카메라를 사용하려면 인덱스를 변경해야 합니다.

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        _, buffer = cv2.imencode('.jpg', frame)
        base64_image = base64.b64encode(buffer).decode('utf-8')

        await websocket.send_text(base64_image)

    cap.release()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_websockets.add(websocket)
    try:
        while True:
            for websocket in connected_websockets:
                await send_camera_image(websocket)
            await asyncio.sleep(0.1)  # 이미지 전송 간격
    except:
        connected_websockets.remove(websocket)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
