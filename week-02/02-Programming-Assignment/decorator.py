from functools import wraps
import json


def to_json(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        data = func(*args, **kwargs)
        return json.dumps(data)
    return decorated
