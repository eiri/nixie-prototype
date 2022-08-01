from typing import Union

from fastapi import FastAPI, Header, Request, Response, HTTPException
from fastapi.responses import PlainTextResponse

from nixie.api import Nixie, KeyError

import uvicorn


class FrontendHelper:
    def get_headers(self, n: Nixie, key: str):
        meta = n.read_meta(key)
        headers = {}
        for k, v in meta.items():
            if v is not None:
                headers[f'nixie-{k}'] = str(v)
        return headers


class NixieRootView(FrontendHelper):
    """View for Nixie root end-point"""

    def __init__(self, nx):
        self.nx = nx
        super().__init__()

    def read_keys(self):
        keys = self.nx.list()
        resp =  '\n'.join(keys)
        return PlainTextResponse(resp)

    async def create_counter(
        self,
        payload: Request,
        nixie_step: Union[int, None] = Header(default=1),
        nixie_name: Union[str, None] = Header(default=None),
        nixie_description: Union[str, None] = Header(default=None)
    ):
        start = 0
        body = await payload.body()
        if body != b'':
            start = int(body)
        key = self.nx.create(start, nixie_step, nixie_name, nixie_description)
        headers = self.get_headers(self.nx, key)
        return PlainTextResponse(key, headers=headers, status_code=201)


class NixieCounterView(FrontendHelper):
    """View for Nixie counter end-point"""

    def __init__(self, nx):
        self.nx = nx
        super().__init__()

    def read_counter(self, key):
        try:
            val = self.nx.read(key)
            headers = self.get_headers(self.nx, key)
            return PlainTextResponse(str(val), headers=headers)
        except KeyError as e:
            raise HTTPException(status_code=404, detail=f'{e}')

    def check_counter(self, key):
        if self.nx.exists(key):
            headers = self.get_headers(self.nx, key)
            return Response(headers=headers, status_code=204)
        else:
            raise HTTPException(status_code=404, detail=f'Key {key} not found')

    def update_counter(self, key):
        try:
            new_val = self.nx.next(key)
            headers = self.get_headers(self.nx, key)
            return PlainTextResponse(str(new_val), headers=headers)
        except KeyError as e:
            raise HTTPException(status_code=404, detail=f'{e}')

    def update_counter_meta(
        self,
        key,
        nixie_step: Union[int, None] = Header(default=1),
        nixie_name: Union[str, None] = Header(default=None),
        nixie_description: Union[str, None] = Header(default=None)
    ):
        try:
            self.nx.update_meta(key, nixie_step, nixie_name, nixie_description)
            headers = self.get_headers(self.nx, key)
            return Response(headers=headers, status_code=204)
        except KeyError as e:
            raise HTTPException(status_code=404, detail=f'{e}')

    def delete_counter(self, key):
        try:
            self.nx.delete(key)
            return Response(status_code=204)
        except KeyError as e:
            raise HTTPException(status_code=404, detail=f'{e}')


class Frontend:
    """REST frontend"""

    def __init__(self):
        self.nx = Nixie()
        #  FastAPI(version = "v2")
        self.app = FastAPI()
        # self.app.config.FALLBACK_ERROR_FORMAT = "text"

        rv = NixieRootView(self.nx)
        self.app.add_api_route(
            path = "/",
            endpoint = rv.read_keys,
            methods = ["GET"]
        )
        self.app.add_api_route(
            path = "/",
            endpoint = rv.create_counter,
            methods = ["POST"]
        )

        cv = NixieCounterView(self.nx)
        self.app.add_api_route(
            path = "/{key}",
            endpoint = cv.read_counter,
            methods = ["GET"]
        )
        self.app.add_api_route(
            path = "/{key}",
            endpoint = cv.check_counter,
            methods = ["HEAD"]
        )
        self.app.add_api_route(
            path = "/{key}",
            endpoint = cv.update_counter,
            methods = ["POST"]
        )
        self.app.add_api_route(
            path = "/{key}",
            endpoint = cv.update_counter_meta,
            methods = ["PATCH"]
        )
        self.app.add_api_route(
            path = "/{key}",
            endpoint = cv.update_counter_meta,
            methods = ["PATCH"]
        )
        self.app.add_api_route(
            path = "/{key}",
            endpoint = cv.delete_counter,
            methods = ["DELETE"]
        )
        return None

    def run(self, port=7312, debug=False):
        uvicorn.run(self.app, host="0.0.0.0", port=port)
