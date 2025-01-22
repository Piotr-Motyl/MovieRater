from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken import views
from api import urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(urls)),
    path("auth/", views.obtain_auth_token),
]
