from flask import jsonify


class RestAPIError(Exception):
    def __init__(self, status_code=500, payload=None):
        self.status_code = status_code
        self.payload = payload

    def to_response(self):
        return jsonify({'error': self.payload}), self.status_code


class BadRequestError(RestAPIError):
    def __init__(self, payload=None):
        super().__init__(400, payload)


class PageNotFound(RestAPIError):
    def __init__(self, payload=None):
        if payload is None:
            payload = {'message': 'Not Found'}
        super().__init__(404, payload)


class InternalServerErrorError(RestAPIError):
    def __init__(self, payload=None):
        super().__init__(500, payload)
