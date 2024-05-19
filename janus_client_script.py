import asyncio
from janus_client import JanusSession, JanusVideoCallPlugin
from aiortc.contrib.media import MediaPlayer


async def main():
    # Create session
    session = JanusSession(base_url="ws://103.209.41.48:8188/janus")

    # Create plugin
    plugin_handle = JanusVideoCallPlugin()

    # Attach to Janus session
    await plugin_handle.attach(session=session)

    # Prepare username and media stream
    username = "testusernamein"
    username_out = "testusernameout"

    player = MediaPlayer(
        "/dev/video0",
        format="v4l2",
        options={
            "video_size": "640x480",
        },
    )

    # Register myself as testusernameout
    result = await plugin_handle.register(username=username_out)
    print(result)

    # Call testusernamein
    result = await plugin_handle.call(username=username, player=player)
    print(result)

    # Wait awhile then hangup
    await asyncio.sleep(40)

    result = await plugin_handle.hangup()
    print(result)

    # Destroy plugin
    await plugin_handle.destroy()

    # Destroy session
    await session.destroy()


if __name__ == "__main__":
    asyncio.run(main())
