from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        custom_response_data = {"data": {}, "error": True, "message": str(getattr(exc, "detail", str(exc)))}

        return Response(custom_response_data, status=response.status_code)

    custom_response_data = {"data": {}, "error": True, "message": str(exc)}

    return Response(custom_response_data, status=status.HTTP_400_BAD_REQUEST)
