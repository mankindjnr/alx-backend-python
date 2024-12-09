from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Conversation, User, Message
from .serializers import ConversationSerializer, MessageSerializer
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['participants']

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation and add participants.
        """
        participants_ids = request.data.get('participants', [])
        if not participants_ids:
            return Response(
                {"error": "Participants are required to create a conversation."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        participants = User.objects.filter(user_id__in=participants_ids)
        if participants.count() != len(participants_ids):
            return Response(
                {"error": "Some participants do not exist."},
                status=status.HTTP_400_BAD_REQUEST
            )

        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['conversation']

    def create(self, request, *args, **kwargs):
        """
        Send a message to an existing conversation.
        """
        conversation_id = request.data.get('conversation_id')
        message_body = request.data.get('message_body')
        sender_id = request.data.get('sender_id')

        if not all([conversation_id, message_body, sender_id]):
            return Response(
                {"error": "conversation_id, message_body, and sender_id are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        conversation = get_object_or_404(Conversation, conversation_id=conversation_id)
        sender = get_object_or_404(User, user_id=sender_id)

        message = Message.objects.create(
            conversation=conversation,
            sender=sender,
            message_body=message_body
        )
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)