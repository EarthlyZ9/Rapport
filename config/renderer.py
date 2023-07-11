import orjson as orjson
from ninja.renderers import BaseRenderer


class ResponseRenderer(BaseRenderer):
    media_type = "application/json"

    def render(self, request, data, *, response_status):
        if response_status >= 400:
            res = dict(code=response_status, **data)
            return orjson.dumps(res)
        else:
            return orjson.dumps(data)
