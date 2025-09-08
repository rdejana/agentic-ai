
from contextlib import AsyncExitStack
import asyncio
import sys

class ChatClient:
    def __init__(self):
        print("Creating client")

    async def chat_loop(self):
        print("\nMCP Client Started!")
        print("Type your queries or 'quit' to exit.")

        while True:
            try:
                query = input("\nQuery: ").strip()

                if query.lower() == 'quit':
                    break

                response = "echo " + query
                print("\n" + response)

            except Exception as e:
                print(f"\nError: {str(e)}")

    async def cleanup(self):
            """Clean up resources"""
            #await self.exit_stack.aclose()
            print("cleanup")


async def main():
    client = ChatClient()
    try:
        #await client.connect_to_server(sys.argv[1])
        await client.chat_loop()
    finally:
        await client.cleanup()

if __name__ == "__main__":

    asyncio.run(main())