import asyncio
import websockets
import os

# Store all connected clients
connected_clients = set()

async def handler(websocket):
    connected_clients.add(websocket)
    print("✅ New client connected! Total clients:", len(connected_clients))
    
    try:
        async for message in websocket:
            print(f"📨 Broadcast message: {message}")
            
            # Send to ALL connected clients (including the sender)
            for client in connected_clients.copy():
                if client.open:  # only send if still connected
                    try:
                        await client.send(f"🦉 Meowl Notifier: {message}")
                    except:
                        pass  # client might have disconnected
    except Exception:
        print("Client disconnected")
    finally:
        connected_clients.remove(websocket)
        print("❌ Client disconnected. Remaining:", len(connected_clients))

async def main():
    port = int(os.environ.get("PORT", 8765))
    
    async with websockets.serve(handler, "0.0.0.0", port):
        print("🚀 Meowl Notifier Broadcast Server is running!")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main()) 
