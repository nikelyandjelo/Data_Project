from django.urls import path
from . import views
from registration.views import register,login_view
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('income/', views.income_list, name='income_list'),
    path('add_income/', views.add_income, name='add_income'),
    path('expense/', views.expense_list, name='expense_list'),
    path('add_expense/', views.add_expense, name='add_expense'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('home/', views.home_view, name='home'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('graph_income/', views.graph_income, name='graph_income'),
    path('graph_expense/', views.graph_expense, name='graph_expense'),
    path('compare/', views.compare_income_expense, name='compare'),
    path('send_email/', views.send_email, name='email_form'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)