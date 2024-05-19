from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import asyncio
import threading
import subprocess
import sys
import os

app = Flask(__name__)
socketio = SocketIO(app, async_mode="gevent", cors_allowed_origins="*")


# Run asyncio event loop in a separate thread
def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


loop = asyncio.new_event_loop()
t = threading.Thread(target=start_loop, args=(loop,))
t.start()


async def run_janus_client():
    process = await asyncio.create_subprocess_exec(
        sys.executable,
        "janus_client_script.py",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    while True:
        line = await process.stdout.readline()
        if line:
            output = line.decode("utf-8").strip()
            socketio.emit("janus_message", {"message": output})
        else:
            break


@app.route("/")
def index():
    return render_template("index.html")


@socketio.on("connect")
def handle_connect():
    print("Client connected")


@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")


@socketio.on("message")
def handle_message(data):
    action = data.get("action")
    if action == "start_call":
        asyncio.run_coroutine_threadsafe(run_janus_client(), loop)
        emit("response", {"status": "call_started"})


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
