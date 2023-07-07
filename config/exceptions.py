from ninja import Schema
from ninja_extra import status
from ninja_extra.exceptions import APIException


class ExceptionSchema(Schema):
    message: str
    status_code: int


class BadRequestException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = "Bad request"


class DuplicateInstanceException(APIException):
    status_code = status.HTTP_409_CONFLICT
    message = "Duplicate instance"


class UnprocessableEntityException(APIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    message = "Unprocessable entity"


class InstanceNotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    message = "Instance not found"
