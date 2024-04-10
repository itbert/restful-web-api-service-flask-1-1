import json
import logger
from flask import Response


def dict_to_json(param: dict):
    json.dump(param)


def exception_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_code = getattr(e, "code", 500)
            logger.exception("Service exception: %s", e)
            r = dict_to_json({"message": e.message, "matches": e.message, "error_code": error_code})
            return Response(r, status=error_code, mimetype='application/json')
    wrapper.__name__ = func.__name__
    return wrapper
