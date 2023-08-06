import logging as log
import json
from urllib3 import request
from .response_models import BaseRequestModel, BaseResponse
from requests import Session
from typing import Optional, Tuple, Dict, Any, List
from aiohttp import ClientSession, ClientResponse
from contextlib import asynccontextmanager, contextmanager
from aiohttp.streams import StreamReader
from functools import cached_property
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings

disable_warnings(InsecureRequestWarning)

MIME_HTML = "text/html"
MIME_JSON = "application/json"


class BaseFormatter(object):
    __slots__ = ["data_", "column_map", "key", "iterator"]

    def __get__(self, instance, owner) -> Dict[str, Any]:
        raise NotImplementedError("Descriptor method is not implemented")

    def __set__(self, instance, value: Tuple[BaseResponse, List[str], str]):
        (self.data_, self.column_map, self.key) = value


class BaseFetcher(object):
    __slots__ = ["base_url", "__request", "__session", "__asession"]
    key = "Default"
    column_map = []
    data = BaseFormatter()
    response_class = BaseResponse

    def __init__(self,
                 default_count_per_page=50,
                 start_index=0,
                 search_value=None,
                 search_regex=False,
                 page_number=1,
                 ordering="asc"
                 ):
        self.base_url = f"https://thecoindetective.com/coins/list/data/{self.key}"
        self.__request = BaseRequestModel.from_params(
            page_number=page_number,
            default_count_per_page=default_count_per_page,
            start_index=start_index,
            search_value=search_value,
            search_regex=search_regex,
            ordering=ordering
        )

    @contextmanager
    def _session_(self) -> Session:
        try:
            self.__session = Session()
            self.__session.verify = False
            yield self.__session
        finally:
            self.__session.close()

    @asynccontextmanager
    async def _asession_(self) -> ClientSession:
        try:
            self.__asession = ClientSession()
            yield self.__asession
        finally:
            await self.__asession.close()

    @cached_property
    def counts(self) -> Optional[Tuple[int, int]]:
        try:
            data = self.fetch_first()
            return data.recordsFiltered, data.recordsTotal
        except Exception as e:
            log.error(e, exc_info=True)
            return None

    @cached_property
    async def a_counts(self) -> Optional[Tuple[int, int]]:
        try:
            data = await self.async_fetch_first()
            return data.recordsFiltered, data.recordsTotal
        except Exception as e:
            log.error(e, exc_info=True)
            return None

    @staticmethod
    def str_to_json(data_: str) -> Dict[str, Any]:
        return json.loads(data_)

    async def bytes_to_json(self, res: StreamReader) -> Dict[str, Any]:
        data_ = await res.read()
        return self.str_to_json(data_.decode())

    def url(self, request_params: BaseRequestModel = None) -> str:
        request_params_ = (self.__request if not request_params else request_params).params
        # replacing Python specific values
        url = f"{self.base_url}?{request.urlencode(request_params_)}" \
            .replace("=None", "") \
            .replace("False", "false")
        return url

    def fetch_first(self, request_: BaseRequestModel = None):
        _request_ = self.__request if not request_ else request_
        with self._session_() as session:
            res = session.get(self.url(request_params=_request_))
            if res.ok:
                if res.headers.get("Content-Type") == MIME_HTML:
                    data_ = self.str_to_json(res.content.decode())
                elif res.headers.get("Content-Type") == MIME_JSON:
                    data_ = res.json()
                res_ = self.response_class(**data_)
                self.data = (res_, self.column_map, self.key)
                return res_
            else:
                log.warning(f"request returned {res.status_code}")
                raise Exception(f"request returned {res.status_code}")

    def fetch_all_records(self):
        request_ = self.__request.copy(deep=True, update={"length": self.counts[0]})
        self.fetch_first(request_=request_)

    async def async_fetch_first(self, request_: BaseRequestModel = None):
        _request_ = self.__request if not request_ else request_
        async with self._asession_() as session:
            async with session.get(self.url(request_params=_request_), verify_ssl=False) as res:
                response: ClientResponse = res
                if response.ok:
                    if response.content_type == MIME_HTML:
                        data_ = await self.bytes_to_json(response.content)
                    elif response.content_type == MIME_JSON:
                        data_ = await response.json()
                    res_ = self.response_class(**data_)
                    self.data = (res_, self.column_map, self.key)
                    return res_
                else:
                    log.warning(f"request returned {response.status}")
                    raise Exception(f"request returned {response.status}")

    async def async_fetch_all_records(self):
        counts = await self.a_counts
        request_ = self.__request.copy(deep=True, update={"length": counts[0]})
        await self.async_fetch_first(request_=request_)
