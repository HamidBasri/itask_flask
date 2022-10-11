from functools import wraps
from flask import request, current_app
from api.utils import logger
import api.utils.errors as errors
from api.components.users.model import User
import jwt
from datetime import datetime, timedelta


def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get("Authorization", "").split()

        if len(auth_headers) != 2:
            return errors.INVALID_TOKEN

        try:
            token = auth_headers[1]
            data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            user = User.query.get(int(data["sub"]))
            if not user:
                raise RuntimeError("User not found")
            return f(user, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return errors.EXPIRED_TOKEN  # 401 is Unauthorized HTTP status code
        except (jwt.InvalidTokenError, Exception) as e:
            logger.error(e)
            return errors.INVALID_TOKEN

    return _verify


def create_token(payload):
    token = jwt.encode(
        {"sub": payload, "iat": datetime.utcnow(), "exp": datetime.utcnow() + timedelta(minutes=300)},
        current_app.config["SECRET_KEY"],
        algorithm="HS256",
    )

    return token


def has_permissions(*arguments):
    def decorator(f):
        @wraps(f)
        def _verify(*args, **kwargs):
            user = args[0]
            if not user:
                return errors.HEADER_NOT_FOUND
            if not arguments:
                return errors.PERMISSION_DENIED_403
            common_roles = set(arguments).intersection(set([role.name for role in user.roles]))
            if len(common_roles) == 0:
                return errors.PERMISSION_DENIED_403
            return f(*args, **kwargs)

        return _verify

    return decorator
