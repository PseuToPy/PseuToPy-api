import enum

class HttpStatus(str, enum.Enum):
    OK = 200,
    BAD_REQUEST = 400,
    UNPROCESSABLE_ENTITY = 422