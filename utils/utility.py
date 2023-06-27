from rest_framework import viewsets, mixins
from .response_handler import ResponseMsg
from rest_framework.response import Response


class BaseModelViewSet(viewsets.GenericViewSet):
    # pass
    def finalize_response(self, request, response, *args, **kwargs):
        # Finalize the response before it's returned to the client
        if response.status_code >= 400:
            return response.data
        else:
            data = response.data
            error = False
            message = "Success"
        # print(data, error, message)
        rh = ResponseMsg(data=data, error=error, message=message)
        return rh.response


class FullBaseViewset(
    BaseModelViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    pass
