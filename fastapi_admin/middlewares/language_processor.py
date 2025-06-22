from starlette.middleware.base import RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from fastapi_admin.i18n import set_locale


async def language_processor(request: Request, call_next: RequestResponseEndpoint) -> Response:
    lang = request.cookies.get("lang") or "en_US"
    set_locale(lang)
    response = await call_next(request)
    return response