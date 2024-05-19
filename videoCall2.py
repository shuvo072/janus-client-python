import asyncio
from janus_client import JanusSession, JanusVideoCallPlugin
from aiortc.contrib.media import MediaPlayer, MediaRecorder


async def main():
    # Create session
    session = JanusSession(
        base_url="ws://103.209.41.48:8188/janus",
    )

    # Create plugin
    plugin_handle = JanusVideoCallPlugin()

    # Attach to Janus session
    await plugin_handle.attach(session=session)

    # Prepare username and media stream
    username = "testusernamein"
    result = await plugin_handle.register(username=username)

    # player = MediaPlayer(
    #     "/dev/video0",
    #     format="v4l2",
    #     options={
    #         "video_size": "640x480",
    #     },
    # )
    # recorder = MediaRecorder("./videocall_record_out.mp4")

    # player = MediaPlayer(
    #     "/dev/video1", format="v4l2", options={"video_size": "640x480"}
    # )
    # recorder = MediaRecorder("./videocall_record_out.mp4")

    await asyncio.sleep(60)
    # result = await plugin_handle.on_receive()

    # Wait awhile then hangup

    result = await plugin_handle.hangup()

    # Destroy plugin
    await plugin_handle.destroy()

    # Destroy session
    await session.destroy()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
