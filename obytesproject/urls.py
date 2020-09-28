from django.contrib import admin
from django.conf import settings
from django.shortcuts import redirect
from django.urls import path, include
from django.conf.urls.static import static
from Hashtag.views import HashtagStatusListView, get_all_hashtag
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', lambda request: redirect('/status/list'), name="home"),
    # path('', include('django.contrib.auth.urls')),
    path('auth/', include('accounts.urls', namespace="auth")),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('accounts/', include('allauth.urls')),
    path('status/', include('status.urls', namespace="status")),
    path('hashtag/status/<str:hashtag>/', HashtagStatusListView.as_view()),
    path('hashtag/all/', get_all_hashtag, name='all-hashtag'),
    path('api/status/', include('status.api.urls'), name='all-status-api'),
    path('admin/', admin.site.urls),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
