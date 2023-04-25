import asyncio
from lantern import run_server

async def main():
    await run_server()

if __name__ == "__main__":
    asyncio.run(main())