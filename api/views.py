from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User, Vendor
from django.contrib.auth.hashers import make_password, check_password


# @api_view(['GET'])
# def sekrit(request):
#     import csv
#     with open('api/data_shop.csv') as file:
#         reader = csv.reader(file)

#         for row in reader:
#             name, district, address, contact, business_hours, rating = row
#             vendor = Vendor(
#                 name=name,
#                 district=district,
#                 address=address,
#                 contact=contact,
#                 business_hours=business_hours,
#                 rating=rating,
#             )

#             vendor.save()

#     print('done')

#     return Response(status=200)


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


@api_view(['GET'])
def get_all_vendors():
    return Response(status=200, data=Vendor.objects.all().values())


@api_view(['GET'])
def get_single_vendor(request, id):
    vendor = Vendor.objects.filter(id=id)
    return Response(status=200, data=vendor.values()[0])
