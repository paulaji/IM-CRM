from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # we need to add website.url using include to route through the website
    path('',include('website.urls')),
]
