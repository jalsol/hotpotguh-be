from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User
from .serializer import UserSerializer


@api_view(['GET'])
def get_user(request):
    all_users = User.objects.all()
    serializer = UserSerializer(all_users, many=True)
    return Response(data=serializer.data, status=200)


@api_view(['GET'])
def login(request):
    username = request.query_params['username']
    password = request.query_params['password']

    if username != 'admin' or password != 'admin':
        return Response(status=401, data={'message': 'Login failed'})

    return Response(status=200, data={'message': 'Login successfully'})
