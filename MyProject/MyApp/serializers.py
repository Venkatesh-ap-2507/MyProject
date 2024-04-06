from rest_framework import serializers
from .models import CustomUser
from .models import UploadedFile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser  # Specify the model
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }


    def create(self, validated_data):
        password = validated_data.pop('password',None)
        instance=self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ['title', 'visibility', 'description',
                  'cost', 'year_of_published', 'file']
