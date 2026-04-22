import asyncio
import websockets
import os
from http import HTTPStatus

connected_clients = set()

# Simple HTTP response for Render health checks and browser visits
async def http_handler(path, headers):
    if path in ("/", "/health"):
        return HTTPStatus.OK, [], b"Meowl Notifier is running! 🦉\n"
    return None  # Let WebSocket handler handle other paths

async def ws_handler(websocket, path):
    connected_clients.add(websocket)
    print(f"✅ New client connected! Total: {len(connected_clients)}")
    
    try:
        async for message in websocket:
            print(f"📨 Broadcast: {message}")
            for client in connected_clients.copy():
                if client.open:
                    try:
                        await client.send(f"🦉 Meowl Notifier: {message}")
                    except:
                        pass
    except:
        pass
    finally:
        connected_clients.discard(websocket)
        print(f"❌ Client disconnected. Remaining: {len(connected_clients)}")

async def main():
    port = int(os.environ.get("PORT", 8765))
    
    async with websockets.serve(
        ws_handler,
        "0.0.0.0",
        port,
        process_request=http_handler,
        ping_interval=20,      # Helps keep connections alive
        ping_timeout=30
    ):
        print("🚀 Meowl Notifier Broadcast Server is running (with health check fix)!")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
