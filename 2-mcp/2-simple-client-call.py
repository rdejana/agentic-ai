from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio
import sys

async def main():
    command = "mcp_servers/bin/mcp_example"
    server_params = StdioServerParameters(
        command=command,
        env=None
    )
    try:
        async with stdio_client(server_params) as servers:
            async with ClientSession(servers[0], servers[1]) as session:
                await session.initialize()
                result = await session.call_tool("greet", {"name": "Ryan"})
                print("")
                for a in result.content:
                    print("tool result = ", a.text)
    except Exception as e:
        print(f"Error connecting to server: {e}")
        sys.exit(1)



if __name__ == "__main__":
    asyncio.run(main())
