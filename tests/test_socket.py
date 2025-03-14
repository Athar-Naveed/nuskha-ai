import socketio


sio = socketio.Client()


@sio.event
async def connect():
    print(f"User connected")
    await sio.emit("send_msg", "Hello from Server")



@sio.event
async def disconnect():
    print(f"User disconnected")
    await sio.emit("send_msg", "Goodbye from Server")


@sio.on("message")
async def handle_message(data):
    print(f"Message: {data}")
    # await sio.emit("send_msg", "Message received")

sio.connect("http://127.0.0.1:8000",socketio_path="/ws/socket.io")


# Send a test message
sio.emit("sendMessage", data={"text": "Hello AI!", "role": "user"})

# Keep connection open to receive responses
sio.wait()