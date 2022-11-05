import jwt
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from authentication.models import User

from .models import Tickets, TicketsAnswer


class TicketsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tickets
        fields = '__all__'


class TicketsAnswerSerializer(serializers.ModelSerializer):
    # ticket = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='detail_answer'
    # )
    class Meta:
        model = TicketsAnswer
        fields = '__all__'

    def create(self, validated_data):
        
        return TicketsAnswer.objects.create(**validated_data)
