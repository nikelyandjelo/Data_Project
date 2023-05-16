from django.contrib import admin
from django.urls import path
from main_page import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('add_income/', views.add_income, name='add_income'),
    path('add_expense/', views.add_expense, name='add_expense'),
]