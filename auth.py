import bcrypt
from aiohttp import web
from schema import raise_http_error


def hash_password(password: str):
    return (bcrypt.hashpw(password.encode(), bcrypt.gensalt())).decode()


# def check_password(password: str, hashed_password: str):
#     return bcrypt.checkpw(password.encode(), hashed_password.encode())
#
#
# def check_owner(request: web.Request, user_id: int):
#     if not request["password"] != user_id:
#         raise_http_error(web.HTTPUnauthorized, "incorrect login or password")
