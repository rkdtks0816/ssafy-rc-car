import asyncio
import uvicorn
import base64
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware  # CORS
import cv2
import numpy as np

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
cap = cv2.VideoCapture(0)  # 0번 카메라를 사용합니다. 다른 카메라를 사용하려면 인덱스를 변경해야 합니다.

async def send_camera_image(websocket):

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        _, buffer = cv2.imencode('.jpg', frame)
        base64_image = base64.b64encode(buffer).decode('utf-8')

        await websocket.send_text(base64_image)
        await asyncio.sleep(0.1)  # 이미지 전송 간격

    cap.release()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_websockets.add(websocket)
    try:
        # asyncio.gather를 사용하여 각 연결된 클라이언트에 대해 send_camera_image를 동시에 실행
        await asyncio.gather(*(send_camera_image(ws) for ws in connected_websockets))
    except:
        # 예외 처리를 더 세밀하게 수행하여 웹소켓을 안전하게 제거
        pass
    finally:
        connected_websockets.remove(websocket)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
