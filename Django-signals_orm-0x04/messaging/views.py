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