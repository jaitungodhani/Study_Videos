from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data["user_data"] = {
            'id': self.user.id,
            'email': self.user.email,
            'profile_picture': self.user.profile_picture.url if self.user.profile_picture else None
        }
        return data