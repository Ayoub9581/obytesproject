from django.urls import path
from .views import StatusListAPIView

urlpatterns = [
    path('', StatusListAPIView.as_view(), name="last-message-api")
]
