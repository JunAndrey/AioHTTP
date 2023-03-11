import json
from asyncio.log import logger
from aiohttp import web
from db import Session


@web.middleware
async def session_middleware(request: web.Request, handler):
    async with Session() as session:
        request["session"] = session
        return await handler(request)


def json_error(status_code: int, exception: Exception) -> web.Response:
    return web.Response(
        status=status_code,
        body=json.dumps({
            'error': exception.__class__.__name__,
            'detail': str(exception)
        }).encode('utf-8'),
        content_type='application/json')


async def error_middleware(app: web.Application, handler):
    async def middleware_handler(request):
        try:
            response = await handler(request)
            if response.status == 404:
                return json_error(response.status, Exception(response.message))
            return response
        except web.HTTPException as ex:
            if ex.status == 404:
                return json_error(ex.status, ex)
            raise
        except Exception as e:
            logger.warning('Request {} has failed with exception: {}'.format(request, repr(e)))
            return json_error(500, e)

    return middleware_handler
