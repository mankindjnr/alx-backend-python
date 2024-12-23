from django.urls import path, include
from rest_framework import routers
from .views import ConversationViewSet, MessageViewSet, UserViewSet
from rest_framework_nested.routers import NestedDefaultRouter

router = routers.DefaultRouter()

router.register(r'conversations', ConversationViewSet, basename='conversation')

# Create a nested router for messages under conversations
nested_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
nested_router.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(nested_router.urls)),
    path('register/', UserViewSet.as_view({'post': 'create'}), name='user-register'),
]