from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def delete_user(request):
    user = get_object_or_404(User, id=request.user.id)
    user.delete()
    messages.success(request, "Your account and related data have been deleted.")
    return redirect("home")


def get_conversation(request, message_id):
    """
    Fetch a message and its threaded replies recursively.
    """
    message = get_object_or_404(Message.objects.select_related("sender", "receiver"), id=message_id)
    replies = fetch_threaded_replies(message)
    return JsonResponse({
        "message": {
            "id": str(message.id),
            "content": message.content,
            "sender": message.sender.username,
            "receiver": message.receiver.username,
            "timestamp": message.timestamp.isoformat(),
            "replies": replies,
        }
    })


def fetch_threaded_replies(message):
    """
    Recursive function to fetch all replies to a message.
    """
    replies = message.replies.prefetch_related("sender", "receiver").all()
    result = []
    for reply in replies:
        result.append({
            "id": str(reply.id),
            "content": reply.content,
            "sender": reply.sender.username,
            "receiver": reply.receiver.username,
            "timestamp": reply.timestamp.isoformat(),
            "replies": fetch_threaded_replies(reply),  # Recursively fetch replies
        })
    return result

def fetch_all_replies(message_id):
    """
    Fetch all replies to a message recursively using Django ORM.
    """
    all_replies = []

    def fetch_replies(parent_message):
        replies = Message.objects.filter(parent_message=parent_message).select_related("sender", "receiver")
        for reply in replies:
            all_replies.append(reply)
            fetch_replies(reply)

    fetch_replies(message_id)
    return all_replies
