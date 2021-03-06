from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

app_name = 'Accounts'

urlpatterns = [
	path('login/', views.Login.as_view(), name='login'),
	path('logout_success/', auth_views.LogoutView.as_view(), name='logout'),
	path('register/', views.Register.as_view(), name='register'),
]