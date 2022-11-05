from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-user/', include('authentication.urls')),
    path('api-tickets/', include('tickets.urls')),
]
