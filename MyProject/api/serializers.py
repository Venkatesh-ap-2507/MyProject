from rest_framework import serializers
from MyApp.models import CustomUser
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        Model = CustomUser
        fields = ['username', 'email', 'password']
