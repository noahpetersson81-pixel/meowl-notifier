import asyncio
import websockets
import os

async def handler(websocket):
    print("✅ Meowl Notifier: Client connected!")
    try:
        async for message in websocket:
            print(f"📨 Received from client: {message}")
            # You can customize this reply
            await websocket.send(f"🦉 Meowl Notifier says: {message}")
    except Exception:
        print("Client disconnected")
    finally:
        print("❌ Connection closed")

async def main():
    # Render requires using the PORT environment variable
    port = int(os.environ.get("PORT", 8765))
    
    async with websockets.serve(handler, "0.0.0.0", port):
        print("🚀 Meowl Notifier WebSocket server is running!")
        await asyncio.Future()  # keep the server alive

if __name__ == "__main__":
    asyncio.run(main())