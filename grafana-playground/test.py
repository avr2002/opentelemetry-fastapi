import httpx

BASE_URL = "http://localhost:8000"

async def call_hello():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/hello")
        print(f"Response from /hello: {response.json()}\n")

async def call_httpbin():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/httpbin")
        print(f"Response from /httpbin: {response.json()}\n")


async def call_jsonplaceholder_post():
    async with httpx.AsyncClient() as client:
        post_id = 1
        response = await client.get(f"{BASE_URL}/jsonplaceholder/posts/{post_id}")
        print(f"Response from /jsonplaceholder/posts: {response.json()}\n")

async def call_echo():
    async with httpx.AsyncClient() as client:
        payload = {"message": "Hello from httpx!"}
        response = await client.post(f"{BASE_URL}/echo", json=payload)
        print(f"Response from /echo: {response.json()}\n")

async def main():
    await call_hello()
    try:
        await call_httpbin()
    except:
        pass
    await call_jsonplaceholder_post()
    await call_echo()
    # await call_hello()
    # # await call_httpbin()
    # await call_jsonplaceholder_post()
    # await call_echo()

if __name__ == "__main__":
    import asyncio
    # asyncio.run(main())
    while True:
        asyncio.run(main())
    # for _ in range(10):
    #     asyncio.run(main())
