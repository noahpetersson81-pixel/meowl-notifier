from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import uvicorn
import os
import json

app = FastAPI(title="Meowl Notifier")

connected_clients = set()

@app.get("/")
async def home():
    return HTMLResponse("<h1>🦉 Meowl Notifier is running!</h1><p>WebSocket at: /ws</p>")

@app.post("/send")
async def receive_from_roblox(data: dict):
    """Receive data from Roblox scanner and broadcast it"""
    message = json.dumps({
        "type": "brainrot_found",
        "data": data,
        "timestamp": os.time()
    })
    
    print(f"📨 Received from Roblox: {len(data.get('brainrots', []))} brainrots")
    
    # Broadcast to all WebSocket clients
    for client in list(connected_clients):
        if client.client_state.CONNECTED:
            try:
                await client.send_text(message)
            except:
                connected_clients.discard(client)
    
    return {"status": "sent", "clients": len(connected_clients)}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)
    print(f"✅ New client connected! Total: {len(connected_clients)}")
    
    try:
        while True:
            data = await websocket.receive_text()  # optional: receive from clients
            print(f"From client: {data}")
    except WebSocketDisconnect:
        pass
    finally:
        connected_clients.discard(websocket)
        print(f"❌ Client disconnected. Remaining: {len(connected_clients)}")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8765))
    uvicorn.run(app, host="0.0.0.0", port=port)
