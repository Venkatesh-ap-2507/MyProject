from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response

class RegisterView(APIView):
    def post(self,request):
        print(request.POST.get('username'))
        print(request.POST.get('email'))
        print(request.POST.get('pass1'))
        print("hello")
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
