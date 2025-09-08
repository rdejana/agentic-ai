

import asyncio
import sys


from mcp.client.session import ClientSession
from mcp.client.streamable_http import streamablehttp_client

async def main():
    url = "http://localhost:8080"

    try:
        async with streamablehttp_client(url) as streams:
            async with ClientSession(streams[0], streams[1]) as session:
                await session.initialize()
                response =  await session.list_tools()
                tools = response.tools
                print("\nConnected to server with tools:", [tool.name for tool in tools])

    except Exception as e:
        print(f"Error connecting to server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
