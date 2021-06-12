from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from rest_framework.parsers import MultiPartParser, JSONParser
from django.contrib.auth import get_user_model

from .serializers import *


@permission_classes([AllowAny])
class CheckEmailUniqueView(generics.GenericAPIView):
    serializer_class = CheckEmailUniqueSerializer

    def get(self, request):
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        return Response(
            data,
            status=status.HTTP_200_OK,
        )


class CustomUserDetailsView(generics.GenericAPIView):
    serializer_class = None

    def get(self, request):
        user = request.user
        return Response(
            data={
                'email': user.email,
                'nickname': user.nickname,
                'gender': user.gender,
                'is_subscribed': user.is_subscribed,
                'profile_image': str(user.profile_image)
            },
            status=status.HTTP_200_OK,
            content_type="application/json"
        )


    def put(self, request):
        CustomUser = get_user_model()
        email = request.user.email
        
        if email is None:
            return CustomValidation('given email is empty', 'email', status.HTTP_400_BAD_REQUEST).get_response()
        if not CustomUser.objects.filter(email=email).exists():
            return CustomValidation('given email doesn\'t exist', 'email', status.HTTP_404_NOT_FOUND).get_response()
        
        data = request.data

        user_object = CustomUser.objects.get(email=email)

        user_object.nickname = data.get('nickname', user_object.nickname)
        user_object.gender = data.get('gender', user_object.gender)

        user_object.save()
        serializer = UserSerializer(user_object)

        return Response(data=serializer.data, status=status.HTTP_204_NO_CONTENT, content_type="application/json")



class UploadImageView(generics.GenericAPIView):
    serializer_class = UploadImageSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        return Response(
            data,
            status=status.HTTP_200_OK,
        )
