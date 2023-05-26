from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls, name='unique_admin_name'),
    path('', include('main_page.urls')),
]

   
