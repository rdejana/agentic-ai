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
                result = await session.call_tool("greet", {"name": "Ryan"})
                print("")
                for a in result.content:
                    print("tool result = ", a.text)

    except Exception as e:
        print(f"Error connecting to server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    service_url = ""
    asyncio.run(main())
