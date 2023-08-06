from json.decoder import JSONDecodeError
from datetime import datetime
import requests
import logging
import typing
import json
import os

UNIMPORTANT_HEADERS = [
    'Accept-Encoding',
    'Accept',
    'Connection',
    'Content-Length',
    'Date',
    'Vary',
    'Content-Encoding'
]


class BaseClient:
    session: requests.Session
    base_url: str
    check_err = True
    log = False

    def __init__(self, session: requests.Session, log: bool, base_url: str):
        BaseClient.base_url = base_url
        BaseClient.session = session
        BaseClient.log = log
        if log:
            (
                [os.remove('responses/' + f) for f in os.listdir('responses')]
                if os.path.isdir('responses')
                else os.mkdir('responses')
            )

    def log_request(self, request: requests.Response) -> None:
        logging.info(
            f'{request.request.method} {request.url}')

        body = json.loads(request.request.body) if request.request.body else ''

        try:
            json_response = request.json()
        except json.decoder.JSONDecodeError:
            json_response = ''

        request.request.headers = {k: v for k, v in request.request.headers.items()
                                   if k not in UNIMPORTANT_HEADERS}

        request.headers = {k: v for k, v in request.request.headers.items()
                           if k not in UNIMPORTANT_HEADERS}

        data = {
            'request': {
                'method': request.request.method,
                'url': request.request.url,
                'headers': dict(request.request.headers),
                'body': body
            },
            'response': {
                'status_code': request.status_code,
                'headers': dict(request.headers),
                'body': json_response
            }
        }

        time = datetime.now().strftime("%Hh%Mm%Ss%f %d-%m-%Y")
        with open(f'responses/request {time}.json', 'w') as w:
            json.dump(data, w, indent=4)

    def make_request(self, endpoint_data: dict, **kwargs) -> typing.Optional[requests.Response]:
        if isinstance(kwargs.get('json'), dict):
            kwargs['json'] = {k: v for k, v in kwargs.get('json').items() if v}

        url = self.base_url
        url += endpoint_data['url'].format(**kwargs.pop('format_data')) \
            if kwargs.get('format_data') \
            else endpoint_data['url']

        req = self.session.request(
            method=endpoint_data['method'],
            url=url,
            **kwargs
        )

        if self.log:
            self.log_request(req)

        # Useful for tests
        if not self.check_err:
            return req

        if not req.ok:
            try:
                data = req.json()
                if 'error' in data:
                    key = data['error'].get('key')
                    message = data['error'].get('message')
                    return logging.error(f'[{req.status_code}] [{key}] - {message}')
            except JSONDecodeError:
                pass

            return logging.error(f'[{req.status_code}] ({req.url}) \nResponse: {req.text}')

        return req

    def update_headers(self, key: str, value: typing.Any) -> None:
        self.session.headers.update({key: value})

    def set_auth_header(self, token: str) -> None:
        if not token:
            return logging.warn('No token was provided')

        self.update_headers(key='Authorization', value=f'Bearer {token}')

    @staticmethod
    def get_response_json(resp: requests.Response) -> typing.Optional[dict]:
        """Get JSON from requests.Response
        Args:
            resp (requests.Response): [Response Object]
        Returns:
            dict: [JSON]
        """
        if not resp:
            return

        try:
            data = resp.json()
        except:
            return

        return data['payload'] if 'payload' in data else data


class BaseModel:
    @classmethod
    def array_from_json(cls, json_data: typing.Union[list]) -> typing.List:
        json_data = json_data.get(
            'payload') if 'payload' in json_data else json_data

        return [cls(**d) for d in json_data] if json_data else []

    @classmethod
    def from_json(cls, json_data: typing.Union[list, dict]) -> typing.Any:
        json_data = json_data.get(
            'payload') if 'payload' in json_data else json_data

        return cls(**json_data) if json_data else None

    @classmethod
    def from_request(cls, request: requests.Response) -> typing.Any:
        json_data = BaseClient.get_response_json(request)

        return (cls.array_from_json(json_data)
                if isinstance(json_data, list)
                else cls.from_json(json_data)
                )
