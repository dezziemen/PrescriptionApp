"""PrescriptionApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/admin/', views.AdminHome.as_view(), name='admin_home'),
    path('', views.Home.as_view(), name='home'),
    path('', include('Accounts.urls')),
    path('user/edit/<int:pk>/', views.EditUser.as_view(), name='edit_user'),
    path('user/create/', views.CreateCustomUser.as_view(), name='create_user'),
    path('user/delete/<int:pk>/', views.DeleteUser.as_view(), name='delete_user'),
    path('home/patient/', views.PatientHome.as_view(), name='patient_home'),
    path('home/pharmacist/', views.PharmacistHome.as_view(), name='pharmacist_home'),
    path('home/doctor/', views.DoctorHome.as_view(), name='doctor_home'),
]
