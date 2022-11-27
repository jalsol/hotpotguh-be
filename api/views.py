from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User, Vendor, BaseTree, Tree
from django.contrib.auth.hashers import make_password, check_password
import datetime


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
        'user_id':  user.id,
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
def get_basetrees_with_space(request, space):
    basetrees = BaseTree.objects.filter(space=space)
    return Response(status=200, data=basetrees.values())


@api_view(['GET'])
def get_single_basetree(request, id):
    basetree = BaseTree.objects.filter(id=id)
    return Response(status=200, data=basetree.values()[0])


@api_view(['POST'])
def add_tree(request):
    user_id = request.data['user_id']
    basetree_id = request.data['tree_id']

    user = User.objects.get(id=user_id)
    basetree = BaseTree.objects.get(id=basetree_id)

    tree = Tree(
        base=basetree,
        user=user,
    )

    tree.save()
    return Response(status=201, data={'message': 'Adding new tree to user successfully'})


@api_view(['GET'])
def get_trees_of_user(request, user_id):
    user = User.objects.get(id=user_id)
    trees_query = Tree.objects.filter(user=user)

    data = []

    for obj in trees_query:
        data.append({
            'id': obj.id,
            'base_name': obj.base.name,
            'base_space': obj.base.space,
            'base_period': obj.base.period,
            'base_period_display': obj.base.period_display,
            'base_temperature': obj.base.temperature,
            'base_upper_temperature': obj.base.upper_temperature,
            'base_pH_level': obj.base.pH_level,
            'base_upper_pH_level': obj.base.upper_pH_level,
            'base_moisture_level': obj.base.moisture_level,
            'base_upper_moisture_level': obj.base.upper_moisture_level,
            'base_image_path': obj.base.image_path,
            'base_description': obj.base.description,
            'creation_date': obj.creation_date,
            'user_id': obj.user.id,
        })

    return Response(status=200, data=data)


@api_view(['GET'])
def check_checklist(request, user_id):
    user = User.objects.get(id=user_id)
    trees_query = Tree.objects.filter(user=user)

    payload = []

    for tree in trees_query:
        tree_payload = {}

        tree_payload['tree_id'] = tree.id

        current_time = datetime.date.today()
        creation_time = tree.creation_date
        period_count = (
            current_time - creation_time).total_seconds() // (60 * 60 * 24 * 7) // tree.base.period

        begin_window = creation_time + \
            datetime.timedelta(days=(tree.base.period * period_count * 7))
        end_window = creation_time + \
            datetime.timedelta(
                days=(tree.base.period * (period_count + 1) * 7))

        if tree.water_task and (begin_window <= tree.water_task < end_window):
            tree_payload['water_task'] = 'true'
        else:
            tree_payload['water_task'] = 'false'

        if tree.fertilize_task and (begin_window <= tree.fertilize_task < end_window):
            tree_payload['fertilize_task'] = 'true'
        else:
            tree_payload['fertilize_task'] = 'false'

        if tree.sunbathe_task and (begin_window <= tree.sunbathe_task < end_window):
            tree_payload['sunbathe_task'] = 'true'
        else:
            tree_payload['sunbathe_task'] = 'false'

        payload.append(tree_payload)

    return Response(status=200, data=payload)


@api_view(['POST'])
def tick_checklist(request, task_name, tree_id):
    tree = Tree.objects.get(id=tree_id)

    if task_name == 'water_task':
        tree.water_task = datetime.date.today()
    elif task_name == 'fertilize_task':
        tree.fertilize_task = datetime.date.today()
    elif task_name == 'sunbathe_task':
        tree.sunbathe_task = datetime.date.today()

    tree.save()

    return Response(status=200)


@api_view(['GET'])
def check_streak(request, user_id):
    user = User.objects.get(id=user_id)
    trees_query = Tree.objects.filter(user=user)
    lose_streak = False

    for tree in trees_query:
        current_time = datetime.date.today()
        creation_time = tree.creation_date
        period_count = (
            current_time - creation_time).total_seconds() // (60 * 60 * 24 * 7) // tree.base.period

        begin_window = creation_time + \
            datetime.timedelta(days=(tree.base.period * period_count * 7))
        end_window = creation_time + \
            datetime.timedelta(
                days=(tree.base.period * (period_count + 1) * 7))

        if not (tree.water_task and (begin_window <= tree.water_task < end_window)):
            lose_streak = True

        if not (tree.fertilize_task and (begin_window <= tree.fertilize_task < end_window)):
            lose_streak = True

        if not (tree.sunbathe_task and (begin_window <= tree.sunbathe_task < end_window)):
            lose_streak = True

        if lose_streak:
            break

    if lose_streak:
        user.streak = 0
    else:
        user.streak += 1

    user.save()

    return Response(status=200, data={'lose_streak': lose_streak})
