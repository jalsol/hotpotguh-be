from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User
from .serializer import UserSerializer
from django.contrib.auth.hashers import make_password, check_password


@api_view(['GET'])
def get_user(request):
    all_users = User.objects.all()
    serializer = UserSerializer(all_users, many=True)
    return Response(data=serializer.data, status=200)


@api_view(['POST'])
def login(request):
    username = request.data['username']
    password = request.data['password']

    user = User.objects.filter(username=username)
    if not user:
        return Response(status=403, data=({'message': 'User not found'}))

    user = user[0]
    if not check_password(password=password, encoded=user.password):
        return Response(status=403, data={'message': 'Wrong password'})

    return Response(status=200, data={
        'message': 'Logging in successfully',
        'token': 'i_love_dnnc',
    })


@api_view(['POST'])
def register(request):
    try:
        new_user = User(
            username=request.data['username'],
            email=request.data['email'],
            first_name=request.data['firstName'],
            last_name=request.data['lastName'],
            password=make_password(request.data['password']),
        )
        new_user.save()
    except:
        return Response(status=424, data={'message': 'Registeration failed'})

    return Response(status=201, data={'message': 'Registeration successfully'})
