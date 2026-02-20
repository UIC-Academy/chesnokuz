from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi import status


class AnasbekSleepyException(Exception):
    def __init__(self, msg):
        self.msg = msg


async def zero_division_error_exc(
    request: Request,
    exc: ZeroDivisionError,
):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "message": exc.args[0],
        },
    )


async def anasbek_sleepy_error_exc(request: Request, exc: AnasbekSleepyException):
    return JSONResponse(
        status_code=status.HTTP_406_NOT_ACCEPTABLE, content={"message": exc.msg}
    )
