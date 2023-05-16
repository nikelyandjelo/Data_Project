from django.contrib import admin
from django.urls import path, include
# from main_page import views

urlpatterns = [
    path('admin/', admin.site.urls, name='unique_admin_name'),
    path('', include('main_page.urls')),
    path('upload/', include('main_page.urls'))
]

   
