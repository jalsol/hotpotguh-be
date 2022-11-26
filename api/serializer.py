from rest_framework import serializers
from .models import User, BaseTree, Tree


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'description')


class BaseTreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseTree
        fields = '__all__'


class TreeSerializer(serializers.ModelSerializer):
    base = BaseTreeSerializer()

    class Meta:
        model = Tree
        fields = '__all__'
