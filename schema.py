from pydantic import BaseModel, ValidationError, EmailStr, constr
from typing import Any, Dict, Optional, Type
import json
from aiohttp import web

ERROR_TYPE = Type[web.HTTPUnauthorized] | Type[web.HTTPForbidden] | Type[web.HTTPNotFound]


def raise_http_error(error_class: ERROR_TYPE, message: str | dict):
    raise error_class(
        text=json.dumps({"status": "error", "description": message}),
        content_type="application/json", )


class CreatePost(BaseModel):
    title: Optional[str]
    description: Optional[str]
    user_id: int


class CreateUser(BaseModel):
    username: str
    password: Optional[constr(min_length=5)]
    users_email: Optional[EmailStr]


SCHEMA_TYPE = Type[CreatePost] | Type[CreateUser]


def validate(data: Dict[str, Any], schema: SCHEMA_TYPE):
    try:
        validated = schema(**data)
        return validated.dict()
    except ValidationError as er:
        raise web.HTTPBadRequest(text=json.dumps({'status': 'error', 'message': er.errors()}),
                                 content_type='application/json')
