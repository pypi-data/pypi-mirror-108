# -*- coding: utf-8 -*-

from fastapi.responses import UJSONResponse

from hagworm.extend.base import Utils
from hagworm.extend.struct import Result


class RespBody(Result):

    def __init__(self, code=0, data=None, **kwargs):

        super().__init__(
            code, data,
            request_id=Utils.uuid1_urn(),
            **kwargs
        )


class Response(UJSONResponse):

    def render(self, content):
        return super().render(
            RespBody(data=content)
        )


class ErrorResponse(Response, Exception):

    def __init__(self, error_code, content=None, status_code=200, **kwargs):

        self._error_code = error_code

        Response.__init__(self, content, status_code, **kwargs)
        Exception.__init__(self, self.body.decode())

    def render(self, content):
        return UJSONResponse.render(
            self,
            RespBody(code=self._error_code, data=content)
        )
