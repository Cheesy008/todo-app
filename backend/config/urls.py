from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from apps.users.urls import urlpatterns as user_urlpatterns
from apps.tasks.urls import urlpatterns as tasks_urlpatterns


api_urlpatterns = [
    *user_urlpatterns,
    *tasks_urlpatterns,
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(api_urlpatterns)),
    path("api/docs/", include("docs.urls")),
]

