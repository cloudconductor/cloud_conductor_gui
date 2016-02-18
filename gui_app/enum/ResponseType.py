from enum import Enum


class Response(Enum):
    OK = 200
    Created = 201
    Accepted = 202
    Unauthorized = 401
    Bad_Request = 400
    No_Content = 204
