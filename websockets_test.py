import asyncio
import websockets
import json

# Replace this with your actual JWT token
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InBlcnNvbjIiLCJyb2xlIjoidXNlciIsImV4cCI6MTc1MjkxNzExNn0.3vhmpYMDJcXDs7k2eAKLtkeUVrskAYTllT2BDqKOvYc"

async def websocket_test():
    uri = f"ws://localhost:8000/ws/1?token={TOKEN}"
    async with websockets.connect(uri) as websocket:
        # Send a chat message
        message = {"content": "Hello from Python client!"}
        await websocket.send(json.dumps(message))
        print("Sent:", message)

        # Listen for incoming messages (including own message echoed back)
        while True:
            response = await websocket.recv()
            print("Received:", response)

asyncio.run(websocket_test())
