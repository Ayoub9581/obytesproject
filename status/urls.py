from django.urls import path
from .views import CreateStatusView, ListMessageView, StatusUpdateView
app_name = 'status'

urlpatterns = [
    path('list', ListMessageView.as_view(), name='message-list'),
    path('add', CreateStatusView.as_view(), name='add-message'),
    path('update/<pk>', StatusUpdateView.as_view(), name='update-list')
]
