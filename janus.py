import asyncio
from janus_client import JanusSession, JanusEchoTestPlugin, JanusVideoRoomPlugin


# Protocol will be derived from base_url
async def main():
    base_url = "http://103.209.41.48:8088/janus"

    session = JanusSession(base_url=base_url)

    plugin_handle = JanusEchoTestPlugin()

    # Attach to Janus session
    await plugin_handle.attach(session=session)

    # Destroy plugin handle
    await plugin_handle.destroy()


if __name__ == "__main__":
    asyncio.run(main())
