import jwt
from pydoc_data import topics
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import User

from .models import Tickets, TicketsAnswer
from .serializers import TicketsAnswerSerializer, TicketsSerializer
from .tasks import hello_world


def GetUser(request):
    token = request.COOKIES.get('jwt')
    if not token:
        raise AuthenticationFailed('Unauthenticated!')
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')
    user = User.objects.get(id=payload['id'])
    return user.id


def GetAdmin(request):
    token = request.COOKIES.get('jwt')
    if not token:
        raise AuthenticationFailed('Unauthenticated!')
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')
    user = User.objects.get(id=payload['id'], is_staff=True, is_superuser=True)
    if user is None:
        return None
    else:
        return user


class SendTicket(APIView):
    def post(self, request):
        user = GetUser(request)
        serializer = TicketsSerializer(
            data={'topic': request.data['topic'], 'description': request.data['description'], 'idUser': user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class AllTicketsUser(APIView):
    def get(self, request):
        user = GetUser(request)
        tickets = Tickets.objects.filter(idUser_id=user)
        serializer = TicketsSerializer(tickets, many=True)
        return Response({"Tickets": serializer.data})


class CheckAnswerUser(APIView):
    def get(self, request):
        user = GetUser(request)
        tickets = TicketsAnswer.objects.filter(idTickets__idUser=user)
        serializer = TicketsAnswerSerializer(tickets, many=True)
        return Response({"TicketsAnswer": serializer.data})


class SendAnswerUser(APIView):
    def get(self, request, pk):
        user = GetUser(request)
        if user is not None:
            try:
                ticket = TicketsAnswer.objects.get(idTickets__idUser=user, id=pk)
            except TicketsAnswer.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = TicketsAnswerSerializer(ticket)
            return Response(serializer.data)
        else:
            raise AuthenticationFailed('Unauthenticated Admin!')

    def post(self, request, pk):
        user = GetUser(request)
        serializer = TicketsSerializer(
            data={'topic': request.data['topic'], 'description': request.data['description'], 'idUser': user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class AllTicketsAdmin(APIView):
    def get(self, request):
        user = GetAdmin(request)
        if user is not None:
            tickets = Tickets.objects.all()
            serializer = TicketsSerializer(tickets, many=True)
            return Response({"Tickets": serializer.data})
        else:
            raise AuthenticationFailed('Unauthenticated Admin!')


class DetailTicketsAdmin(APIView):
    def get(self, request, pk):
        user = GetAdmin(request)
        if user is not None:
            try:
                ticket = Tickets.objects.get(pk=pk)
            except Tickets.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = TicketsSerializer(ticket)
            return Response(serializer.data)
        else:
            raise AuthenticationFailed('Unauthenticated Admin!')

    def post(self, request, pk):
        user = GetAdmin(request)
        if user is not None:
            ticket = Tickets.objects.get(pk=pk)
            serializer = TicketsAnswerSerializer(
                data={'answer': request.data['answer'], 'idTickets': ticket.id, 'idAdmin': user.id})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            raise AuthenticationFailed('Unauthenticated Admin!')
