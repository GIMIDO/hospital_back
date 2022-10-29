from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from functools import wraps
from django.http import HttpResponseForbidden


def get_access_token(employee):
    refresh = RefreshToken.for_user(employee)
    accessToken = refresh.access_token
    accessToken["name"] = employee.name
    accessToken["role"] = employee.role

    return str(accessToken)

def authorise_only(function):
    @wraps(function)
    def wrap(self, request, *args, **kwargs):
        validated_token = validate_token(request=request)
        if validated_token is None:
            return HttpResponseForbidden()
        else:
            return function(self, request, *args, **kwargs)
        
    return wrap

def is_not_doctor(function):
    @wraps(function)
    def wrap(self, request, *args, **kwargs):
        validated_token = validate_token(request=request)
        if validated_token is None:
            return HttpResponseForbidden()
        else:
            role = validated_token.payload.get("role")
            if (role == "Admin" or role == "Reception"):
                return function(self, request, *args, **kwargs)
            else:
                return HttpResponseForbidden()
        
    return wrap

def is_admin(function):
    @wraps(function)
    def wrap(self, request, *args, **kwargs):
        validated_token = validate_token(request=request)
        if validated_token is None:
            return HttpResponseForbidden()
        else:
            role = validated_token.payload.get("role")
            if (role == "Admin"):
                return function(self, request, *args, **kwargs)
            else:
                return HttpResponseForbidden()
        
    return wrap

def validate_token(request):
    jwt_auth = JWTAuthentication()
    header = jwt_auth.get_header(request)
    if header is None:
        return None

    raw_token = jwt_auth.get_raw_token(header)
    if raw_token is None:
        return None

    validated_token = jwt_auth.get_validated_token(raw_token)

    return validated_token

def verify_request_token(token):
    jwt_auth = JWTAuthentication()
    validated_token = jwt_auth.get_validated_token(token)
    if validated_token is None:
        return None
    
    role = validated_token.payload.get("role")
    name = validated_token.payload.get("name")
    if role is None:
        return None
    if role == "Admin" or role == "Reception" or role == "Doctor":
        return (role, name)
    else:
        return None