from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User, Vendor, BaseTree
from django.contrib.auth.hashers import make_password, check_password


@api_view(['GET'])
def sekrit(request):
    import csv
    with open('api/data_tree.csv') as file:
        reader = csv.reader(file)

        for row in reader:
            print(row)
            name, space, period, period_display, temperature, upper_temperature, pH_level, upper_pH_level, moisture_level, upper_moisture_level, image_path, description = row

            base_tree = BaseTree(
                name=name,
                space=space,
                period=period,
                period_display=period_display,
                temperature=temperature,
                upper_temperature=upper_temperature,
                pH_level=pH_level,
                upper_pH_level=upper_pH_level,
                moisture_level=moisture_level,
                upper_moisture_level=upper_moisture_level,
                image_path=image_path,
                description=description
            )

            base_tree.save()

    print('done')

    return Response(status=200)


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
def get_all_vendors(request):
    return Response(status=200, data=Vendor.objects.all().values())


@api_view(['GET'])
def get_single_vendor(request, id):
    vendor = Vendor.objects.filter(id=id)
    return Response(status=200, data=vendor.values()[0])


@api_view(['POST'])
def toggle_favorite(request, id):
    pass


@api_view(['GET'])
def get_all_basetrees(request):
    return Response(status=200, data=BaseTree.objects.all().values())


@api_view(['GET'])
def get_single_basetree(request, id):
    basetree = BaseTree.objects.filter(id=id)
    return Response(status=200, data=basetree.values()[0])
