from rest_framework import serializers, status
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import GENDER_SELECTION, LEVEL_SELECTION
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import update_last_login
from utils.validation import CustomValidation

CustomUser = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'nickname', 'is_subscribed', 'profile_image')


# Reference: https://stackoverflow.com/questions/53969386/how-to-save-extra-fields-on-registration-using-custom-user-model-in-drf-django
class UserRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField(
        required=True,
        max_length=100
    )

    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()
        data_dict['nickname'] = self.validated_data.get('nickname', '')
        data_dict['gender'] = self.validated_data.get('gender', '')
        return data_dict


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password", None)

        user = authenticate(email=email, password=password)
        if user is None:
            return {'user': 'None'}
        try:
            update_last_login(None, user)
        except CustomUser.DoesNotExist:
            raise CustomValidation('User with given email and password does not exist', 'message', status.HTTP_409_CONFLICT)
        return {
            'user': {
                'email': user.email,
                'nickname': user.nickname,
                'gender': user.gender,
                'is_subscribed': user.is_subscribed,
                'profile_image': user.profile_image
            },
        } 

class CheckEmailUniqueSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100)

    def validate(self, attrs):
        email = attrs['email']
        if CustomUser.objects.filter(email=email).exists():
            raise CustomValidation('given email is in use', 'email', status.HTTP_409_CONFLICT)
        return {
            'message': 'given email is unique'
        }


class UploadImageSerializer(serializers.Serializer):
    image = serializers.ImageField()

    def validate(self, attrs):

        return {
            'message': 'Success!'
        }
