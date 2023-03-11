from aiohttp import ClientSession
import asyncio


async def main():
    async with ClientSession() as session:
        # response = await session.post('http://127.0.0.1:8080/user/',
        #                               json={'username': 'BiDon', 'password': 'ksjsjhuyemfom',
        #                                     'users_email': 'Bidon@gmail.com'})

        # response = await session.patch('http://127.0.0.1:8080/user/1/',
        #                                json={'username': 'Big_Chipolino', 'users_email': 'Big_lino@gmail.com'})
        response = await session.post('http://127.0.0.1:8080/post/',
                                      json={"title": "read_me", "description": "uvlekatelno", "user_id": 2})

        # response = await session.patch("http://127.0.0.1:8080/post/3/", json={"title": "YO", "description": "opyat 25",
        #                                                                       "user_id": 1})

        # response = await session.delete("http://127.0.0.1:8080/post/5/")

        print(response.status)
        print(await response.json())

        response = await session.get("http://127.0.0.1:8080/post/1/")
        print(response.status)
        print(await response.text())


asyncio.run(main())
