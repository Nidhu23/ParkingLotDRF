from rest_framework.response import Response
from rest_framework import status
import rest_framework
from registration.models import User
from registration.redis_setup import get_redis_instance
from . import settings
import jwt


def jwt_decode(view_func):
    def wrap(request, *args, **kwargs):
        try:
            payload = jwt.decode(request.headers.get('token'),
                                 settings.SECRET_KEY)
            username = payload.get('username')
            redis_instance = get_redis_instance()
            if redis_instance.exists(username) > 0:
                return view_func(request, *args, **kwargs)
            else:
                return Response("You are not logged in, Please login")
        except jwt.ExpiredSignatureError:
            return Response("Please login again")
        except Exception:
            return Response(exception=True)

    return wrap


def role_required(roles_allowed=[]):
    def check_permission(view_func):
        def wrap(request, *args, **kwargs):
            try:
                user = jwt.decode(request.headers.get('token'),
                                  settings.SECRET_KEY)
                username = user.get('username')
                user_details = User.objects.get(username=username).role
                role = user_details.role
                if role in roles_allowed:
                    return view_func(request, *args, **kwargs)
                else:
                    return Response("Forbidden access",
                                    status=status.HTTP_403_FORBIDDEN)
            except Exception:
                return Response("Error")

        return wrap

    return check_permission
