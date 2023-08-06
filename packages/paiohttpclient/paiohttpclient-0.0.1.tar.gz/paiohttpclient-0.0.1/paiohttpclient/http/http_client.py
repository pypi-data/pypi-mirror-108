import asyncio
import logging
from typing import Any, List, Optional, Type, Union
from urllib.parse import urlencode

import aiohttp
import graphql
import tenacity
import ujson
from aiohttp import FormData
from pydantic import BaseModel

from .graphql_response import GraphQLResponse
from .http_error import HttpError
from ..utils import jsonable_encoder

RequestBody = Optional[Union[str, bytes, dict, list, BaseModel, FormData]]
RequestBodyPrepared = Optional[Union[str, bytes, dict, list, FormData]]
Response = Optional[Union[str, dict, list, BaseModel, GraphQLResponse[Any, Any]]]


class HttpClient:
    logger: logging.Logger = None

    def __init__(
            self,
            base_url: str,
            common_headers: dict = None,
            common_params: dict = None,
            common_body: dict = None,
    ):
        self.logger = logging.getLogger(self.__class__.__qualname__)
        self.base_url = base_url.strip(' /')
        self.common_headers = common_headers or {}
        self.common_params = common_params or {}
        self.common_body = common_body or {}

    def __prepare_url(self, path: str, params: dict = None) -> str:
        path = path.strip(' /')
        params = self.common_params | (params or {})
        url = f"{self.base_url.strip(' /')}/{path}".strip(' /')

        if bool(params):
            try:
                url += f"?{urlencode(params, doseq=True)}"
            except Exception as e:
                raise ValueError(f'Incorrect params. {e}')

        return url

    def __prepare_headers(self, headers: dict) -> dict[str, Any]:
        return self.common_headers | (headers or {})

    def __prepare_request_data(
            self,
            body: RequestBody,
            as_form: bool = False,
            as_graphql: bool = False
    ) -> RequestBodyPrepared:
        body = body or {}

        if isinstance(body, bytes):
            return body

        if isinstance(body, str):
            if as_graphql:
                return {
                    "query": graphql.print_ast(
                        graphql.parse(
                            graphql.Source(
                                body,
                                "GraphQL request"
                            )
                        )
                    )
                }

            return body.strip()
        else:
            if as_graphql:
                raise ValueError('GraphQL query should be a string!')

        if isinstance(body, FormData):
            for k, v in self.common_body.items():
                body.add_field(k, v)

            return body

        body_data = jsonable_encoder(body)

        if isinstance(body_data, dict):
            body_data = self.common_body | body_data

        if as_form:
            form = FormData()

            for k, v in body_data:
                form.add_field(name=k, value=v)

            return form

        return body_data

    async def __process_response(
            self,
            response: Union[aiohttp.ClientResponse, None],
            response_model: Type[BaseModel] = None,
            error_response_model: Type[BaseModel] = None,
            text_response: bool = False,
    ) -> Optional[Union[str, BaseModel, List[BaseModel], dict, List[dict]]]:
        if not bool(response):
            if text_response:
                return ""

            return {}

        try:
            response_text = (await response.text(encoding='utf-8')).strip()
        except Exception as e:
            self.logger.error(f"Unable to read response text. {type(e)}. {e}")
            raise HttpError(response.status)

        if text_response or not bool(response_text):
            return response_text

        if 200 > response.status or response.status > 206:
            if bool(error_response_model):
                try:
                    return error_response_model.parse_obj(ujson.loads(response_text))
                except Exception:
                    pass

            self.logger.debug(f"Response status is {response.status}. Raw body: {response_text}")
            raise HttpError(response.status, {"message": response_text})

        try:
            processed_response = response_json = ujson.loads(response_text)
            self.logger.debug(
                f"Raw response: {response_text}. "
                f"Response model is {response_model.__class__.__qualname__ if bool(response_model) else None}"
            )

            if bool(response_model):
                try:
                    processed_response = response_model.parse_obj(response_json)
                except Exception as e:
                    self.logger.error(
                        f'Unable to parse response object of {response_model.__class__.__qualname__}. {type(e)}. {e}'
                    )
                    # TODO: Custom error
                    raise ValueError(f'Response don\'t match request params (response_model)')

            return processed_response
        except Exception as e:
            self.logger.error(f"Unable to process response. {type(e)}. {e}")
            raise HttpError(response.status, data={'message': response_text})

    async def __execute_request(
            self,
            method: str,
            url: str,
            headers: dict,
            request_data: RequestBody,
            response_model: Type[BaseModel] = None,
            error_response_model: Type[BaseModel] = None,
            text_response: bool = False,
            timeout: float = 10,
            **kwargs
    ) -> Response:
        self.logger.debug(f"[{method}] {url}. Data: {request_data}")

        session_args = {"json_serialize": ujson.dumps, "headers": headers}

        if bool(timeout):
            session_args |= {"timeout": aiohttp.ClientTimeout(total=timeout)}

        session = aiohttp.ClientSession(**session_args)

        if isinstance(request_data, (str, bytes, FormData,)):
            kwargs['data'] = request_data
        else:
            kwargs['json'] = request_data

        async with session:
            async with session.request(method, url, **kwargs) as response:
                try:
                    return await self.__process_response(
                        response,
                        response_model=response_model,
                        error_response_model=error_response_model,
                        text_response=text_response,
                    )
                except HttpError:
                    raise
                except Exception as e:
                    self.logger.error(
                        f'Unable to process response in {method.upper()} request to {url}. {type(e)}. {e}'
                    )
                    raise HttpError

    async def request(
            self,
            method: str,
            path: str,
            *,
            params: dict = None,
            headers: dict = None,
            body: RequestBody = None,
            body_as_form: bool = False,
            body_as_graphql: bool = False,
            retry_count: int = 3,
            response_model: Type[BaseModel] = None,
            error_response_model: Type[BaseModel] = None,
            text_response: bool = False,
            timeout: float = 10,
            **kwargs
    ) -> Response:
        url = self.__prepare_url(path, params)
        headers = self.__prepare_headers(headers)
        request_data = self.__prepare_request_data(body, as_form=body_as_form, as_graphql=body_as_graphql)
        _execute_request = tenacity.retry(
            stop=tenacity.stop_after_attempt(max(1, retry_count)),
            reraise=True,
        )(self.__execute_request)

        try:
            return await _execute_request(
                method=method,
                url=url,
                headers=headers,
                request_data=request_data,
                response_model=response_model,
                error_response_model=error_response_model,
                text_response=text_response,
                timeout=timeout,
                **kwargs
            )
        except (asyncio.TimeoutError, TimeoutError):
            raise HttpError(503, {"message": "Service Unavailable. Timeout error"})
        except asyncio.CancelledError:
            raise HttpError(503, {"message": "Service Unavailable. Operation cancelled"})
        except HttpError as e:
            raise e
        except Exception as e:
            self.logger.error(f'[{method.upper()}] Unable to make request to {url}. {type(e)}. {e}')
            raise HttpError

    async def graphql_request(
            self,
            query: str,
            *,
            path: str = '/graphql',
            params: dict = None,
            headers: dict = None,
            retry_count: int = 3,
            data_model: Union[Type[BaseModel], Type[dict]] = dict,
            error_model: Union[Type[BaseModel], Type[dict]] = dict,
            text_response: bool = False,
            timeout: float = 10,
    ) -> GraphQLResponse[Any, Any]:
        return await self.post(
            path,
            params=params,
            headers=headers,
            body=query,
            body_as_graphql=True,
            retry_count=retry_count,
            response_model=GraphQLResponse[data_model, error_model],
            text_response=text_response,
            timeout=timeout,
        )

    async def get(
            self,
            path: str,
            *,
            params: dict = None,
            headers: dict = None,
            body: RequestBody = None,
            body_as_form: bool = False,
            retry_count: int = 3,
            response_model: Type[BaseModel] = None,
            error_response_model: Type[BaseModel] = None,
            text_response: bool = False,
            timeout: float = 10,
            **kwargs
    ):
        return await self.request(
            'GET',
            path,
            params=params,
            headers=headers,
            body=body,
            body_as_form=body_as_form,
            retry_count=retry_count,
            response_model=response_model,
            error_response_model=error_response_model,
            text_response=text_response,
            timeout=timeout,
            **kwargs
        )

    async def post(
            self,
            path: str,
            *,
            params: dict = None,
            headers: dict = None,
            body: RequestBody = None,
            body_as_form: bool = False,
            retry_count: int = 3,
            response_model: Type[BaseModel] = None,
            error_response_model: Type[BaseModel] = None,
            text_response: bool = False,
            timeout: float = 10,
            **kwargs
    ):
        return await self.request(
            'POST',
            path,
            params=params,
            headers=headers,
            body=body,
            body_as_form=body_as_form,
            retry_count=retry_count,
            response_model=response_model,
            error_response_model=error_response_model,
            text_response=text_response,
            timeout=timeout,
            **kwargs
        )

    async def put(
            self,
            path: str,
            *,
            params: dict = None,
            headers: dict = None,
            body: RequestBody = None,
            body_as_form: bool = False,
            retry_count: int = 3,
            response_model: Type[BaseModel] = None,
            error_response_model: Type[BaseModel] = None,
            text_response: bool = False,
            timeout: float = 10,
            **kwargs
    ):
        return await self.request(
            'PUT',
            path,
            params=params,
            headers=headers,
            body=body,
            body_as_form=body_as_form,
            retry_count=retry_count,
            response_model=response_model,
            error_response_model=error_response_model,
            text_response=text_response,
            timeout=timeout,
            **kwargs
        )

    async def patch(
            self,
            path: str,
            *,
            params: dict = None,
            headers: dict = None,
            body: RequestBody = None,
            body_as_form: bool = False,
            retry_count: int = 3,
            response_model: Type[BaseModel] = None,
            error_response_model: Type[BaseModel] = None,
            text_response: bool = False,
            timeout: float = 10,
            **kwargs
    ):
        return await self.request(
            'PATCH',
            path,
            params=params,
            headers=headers,
            body=body,
            body_as_form=body_as_form,
            retry_count=retry_count,
            response_model=response_model,
            error_response_model=error_response_model,
            text_response=text_response,
            timeout=timeout,
            **kwargs
        )

    async def delete(
            self,
            path: str,
            *,
            params: dict = None,
            headers: dict = None,
            body: RequestBody = None,
            body_as_form: bool = False,
            retry_count: int = 3,
            response_model: Type[BaseModel] = None,
            error_response_model: Type[BaseModel] = None,
            text_response: bool = False,
            timeout: float = 10,
            **kwargs
    ):
        return await self.request(
            'DELETE',
            path,
            params=params,
            headers=headers,
            body=body,
            body_as_form=body_as_form,
            retry_count=retry_count,
            response_model=response_model,
            error_response_model=error_response_model,
            text_response=text_response,
            timeout=timeout,
            **kwargs
        )
