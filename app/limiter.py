from fastapi import Request

from slowapi import Limiter
from slowapi.util import get_remote_address


def get_global_key(request: Request):
    return "global_rate_limit"


limiter = Limiter(key_func=get_remote_address)
