from rest_framework.permissions import BasePermission

class IsOwnerOrParticipant(BasePermission):
    """
    Custom permission to ensure users can access only their own messages and conversations.
    """

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'participants'):  # For Conversations
            return request.user in obj.participants.all()
        elif hasattr(obj, 'sender'):  # For Messages
            return obj.sender == request.user or request.user in obj.conversation.participants.all()
        return False
