from django.urls import path
from . import consumers

websocket_urlpatterns = [
  path('ws/<int:id>/<int:my_id>/', consumers.PersonalChatConsumer.as_asgi()),
]