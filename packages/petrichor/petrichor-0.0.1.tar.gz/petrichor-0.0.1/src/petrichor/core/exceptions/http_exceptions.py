"""This module is for custom http exceptions.

To make the exceptions layer as independant as possible on the chosen framework.
"""
import fastapi
from starlette import status


class NotFound(fastapi.HTTPException):
    """Use this exception when you would normally return 404 NOT FOUND."""

    def __init__(self, detail=None):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class Conflict(fastapi.HTTPException):
    """Use this exception when you would normally return Conflict."""

    def __init__(self, detail="Such an entry already exists"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class Unauthorized(fastapi.HTTPException):
    """Use this exception when you would normally return 401 UNAUTHORIZED."""

    def __init__(self, detail=None):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class UnprocessableEntity(fastapi.HTTPException):
    """Use this exception when you would normally return 422 UNPROCESSABLE ENTITY."""

    def __init__(self, detail=None):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)
