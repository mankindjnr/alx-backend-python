from rest_framework import serializers
from . import models

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'created_at']

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()
    conversation = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = models.Message
        fields = ['message_id', 'sender', 'conversation', 'message_body', 'sent_at']

# StringRelatedField returns the string representation of the related field
class ConversationSerializer(serializers.ModelSerializer):
    participants = serializers.StringRelatedField(many=True)
    messages = MessageSerializer(many=True, read_only=True) #nested messages

    class Meta:
        model = models.Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at']