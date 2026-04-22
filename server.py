import asyncio
import websockets
import os
from http import HTTPStatus

# Store all connected WebSocket clients
connected_clients = set()

async def health_check(path, request_headers):
    """Handle normal HTTP requests (for Render health checks)"""
    if path == "/" or path == "/health":
        return HTTPStatus.OK, [], b"Meowl Notifier is healthy! 🦉\n"
    return None  # Let WebSocket handler take over for other paths

async def ws_handler(websocket):
    connected_clients.add(websocket)
    print(f"✅ New client connected! Total: {len(connected_clients)}")
    
    try:
        async for message in websocket:
            print(f"📨 Broadcast: {message}")
            # Broadcast to everyone
            for client in connected_clients.copy():
                if client.open:
                    try:
                        await client.send(f"🦉 Meowl Notifier: {message}")
                    except:
                        pass
    except Exception as e:
        print("Client error:", e)
    finally:
        connected_clients.discard(websocket)
        print(f"❌ Client disconnected. Remaining: {len(connected_clients)}")

async def main():
    port = int(os.environ.get("PORT", 8765))
    
    async with websockets.serve(
        ws_handler,
        "0.0.0.0",
        port,
        process_request=health_check   # ← This fixes the health check error
    ):
        print("🚀 Meowl Notifier Broadcast Server is running with health check!")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
