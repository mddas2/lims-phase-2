from django.urls import path
from . import consumers

websocket_urlpatterns = [
    #path('synchronously/chat/<str:email/',consumers.MySyncConsumer.as_asgi()),
    path('asynchronous/chat/<str:email>/',consumers.MyAyncConsumer.as_asgi()),
]