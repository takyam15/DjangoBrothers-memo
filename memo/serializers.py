from rest_framework import serializers

from .models import Memo


class MemoListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Memo
        exclude = ('text',)


class MemoRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Memo
        fields = '__all__'


class MemoCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Memo
        exclude = ('created_datetime', 'updated_datetime')


class MemoUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Memo
        exclude = ('created_datetime', 'updated_datetime')


class MemoDestroySerializer(serializers.ModelSerializer):

    class Meta:
        model = Memo
        