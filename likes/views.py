from rest_framework import viewsets, mixins
from .models import Likes
from core.permissions import IsSubscribedStudent, IsAdmin
from utils.response_handler import ResponseMsg 
from rest_framework.response import Response
from .serializers import LikesSerializer

# Create your views here.

class LikesView(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Likes.objects.order_by("created_at")
    serializer_class = LikesSerializer
    permission_classes = [IsSubscribedStudent | IsAdmin]
    
    def create(self, request, *args, **kwargs):
        response_data = super().create(request, *args, **kwargs)
        response = ResponseMsg(
            data= response_data.data,
            error=False,
            message="Likes Successfully!!"
        )
        return Response(response.response)
    
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        response = ResponseMsg(
            data= {},
            error=False,
            message="Likes remove Successfully!!"
        )
        return Response(response.response)
    
    def perform_destroy(self, instance):
        instance.soft_delete()

