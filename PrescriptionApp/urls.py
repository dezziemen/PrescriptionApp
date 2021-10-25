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
    path('', views.Home.as_view(), name='home'),
    path('home/admin/', views.AdminHome.as_view(), name='admin_home'),
    path('home/doctor/', views.DoctorHome.as_view(), name='doctor_home'),
    # path('home/pharmacist/', views.PharmacistHome.as_view(), name='pharmacist_home'),
    # path('home/patient/', views.PatientHome.as_view(), name='patient_home'),
    path('', include('Accounts.urls')),
    path('user/view/<int:pk>/', views.ViewUser.as_view(), name='view_user'),
    path('user/edit/<int:pk>/', views.EditUser.as_view(), name='edit_user'),
    path('user/create/', views.CreateCustomUser.as_view(), name='create_user'),
    path('user/delete/<int:pk>/', views.DeleteUser.as_view(), name='delete_user'),
    path('user/prescribe/<int:pk>/', views.Prescribe.as_view(), name='prescribe'),
    path('user/view_patient/<int:pk>/', views.ViewPatient.as_view(), name='view_patient'),
    path('create_medicine/', views.CreateMedicine.as_view(), name='create_medicine'),
    path('edit_prescription/<int:pk>/cart/<int:med_pk>/', views.EditPrescription.as_view(), name='edit_prescription'),
    path('delete_medicine/<int:pk2>/medicine/<int:pk>/', views.DeleteMedicine.as_view(), name='delete_medicine'),
]
