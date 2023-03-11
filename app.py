from middleware import error_middleware, session_middleware
from aiohttp import web
from schema import validate, CreatePost, CreateUser
from sqlalchemy.exc import IntegrityError
from db import engine, Base, Session, Announcement, User
from auth import hash_password
from sqlalchemy import select
import json


async def get_users_id(id):
    async with Session() as session:
        stmt = select(User).where(User.id == id)
        result = await session.execute(stmt)
        user = result.scalar()
        if user is None:
            raise web.HTTPNotFound(text=json.dumps({'status': 'error', 'message': 'user not found'}),
                                   content_type='application/json')

    await session.commit()
    return user


async def get_user(user_id: int, session: Session):
    user = await session.get(User, user_id)
    if user is None:
        raise web.HTTPNotFound(
            text=json.dumps({"status": "Error", "message": "User not found"}),
            content_type="application/json", )
    return user


class PostUser(web.View):
    async def get(self):
        session = self.request["session"]
        user_id = int(self.request.match_info["user_id"])
        user = await get_user(user_id, session)
        return web.json_response(
            {"id": user.id, "username": user.username, "users_email": user.users_email}
        )

    async def post(self):
        session = self.request["session"]
        json_data = validate(await self.request.json(), CreateUser)
        json_data["password"] = hash_password(json_data["password"])
        user = User(**json_data)
        session.add(user)
        try:
            await session.commit()
        except IntegrityError:
            raise web.HTTPConflict(
                text=json.dumps({"status": "Error", "message": "User already exists"}),
                content_type="application/json")
        return web.json_response(
            {
                "id": user.id,
                "username": user.username,
                "password": user.password,
                "users_email": user.users_email,
            }
        )

    async def patch(self):
        user_id = int(self.request.match_info["user_id"])
        user = await get_user(user_id, self.request["session"])
        json_data = validate(await self.request.json(), CreateUser)
        if "password" in json_data:
            json_data["password"] = hash_password(json_data["password"])
        for field, value in json_data.items():
            setattr(user, field, value)
        self.request["session"].add(user)
        await self.request["session"].commit()
        return web.json_response({"status": "success"})

    async def delete(self):
        user_id = int(self.request.match_info['user_id'])
        user = await get_user(user_id, self.request['session'])
        await self.request['session'].delete(user)
        await self.request['session'].commit()
        return web.json_response({'status': 'success'})


async def get_post(post_id: int, session: Session):
    post = await session.get(Announcement, post_id)
    if post is None:
        raise web.HTTPNotFound(
            text=json.dumps({"status": "Error", "message": "Post not found"}),
            content_type="application/json", )
    return post


class PostView(web.View):
    async def get(self):
        session = self.request["session"]
        post_id = int(self.request.match_info["post_id"])
        post = await get_post(post_id, session)
        return web.json_response(
            {
                "id": post.id,
                "title": post.title,
                "description": post.description,
                "user_id": post.user_id,
                "creation_date": post.creation_date.isoformat(),
            }
        )

    async def post(self):
        session = self.request["session"]
        json_data = validate(await self.request.json(), CreatePost)
        user = await get_users_id(json_data["user_id"])
        post = Announcement(**json_data)
        if post.user_id != user.id:
            raise web.HTTPNotFound()
        session.add(post)
        await session.commit()
        return web.json_response(
            {
                "title": post.title,
                "description": post.description,
                "user_id": user.id,
            }
        )

    async def patch(self):
        post_id = int(self.request.match_info["post_id"])
        post = await get_post(post_id, self.request["session"])
        json_data = validate(await self.request.json(), CreatePost)
        user = await get_users_id(json_data["user_id"])
        if post.user_id != user.id:
            raise web.HTTPNotFound()
        for field, value in json_data.items():
            setattr(post, field, value)
        self.request["session"].add(post)
        await self.request["session"].commit()
        return web.json_response({"status": "success"})

    async def delete(self):
        post_id = int(self.request.match_info["post_id"])
        post = await get_post(post_id, self.request["session"])
        await self.request["session"].delete(post)
        await self.request["session"].commit()
        return web.json_response({"status": "success"})


async def orm_context(app: web.Application):
    print("START")
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        # await conn.commit()
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()
    print("SHUTDOWN")


async def get_app():
    app = web.Application(middlewares=[session_middleware])
    app.middlewares.append(error_middleware)
    app.cleanup_ctx.append(orm_context)

    app.add_routes(
        [
            web.post("/post/", PostView),
            web.post("/user/", PostUser),
            web.get("/post/{post_id:\d+}/", PostView),
            web.get("/user/{user_id:\d+}/", PostUser),
            web.patch("/post/{post_id:\d+}/", PostView),
            web.patch("/user/{user_id:\d+}/", PostUser),
            web.delete("/post/{post_id:\d+}/", PostView),
            web.delete("/user/{user_id:\d+}/", PostUser),
        ]
    )

    return app
# get_app = get_app()
# if __name__ == "__main__":
    # get_app = get_app()
    # web.run_app(app)
