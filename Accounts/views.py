from django.shortcuts import render
from django.views.generic import FormView
from .forms import PatientRegisterForm
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView


class Register(FormView):
	template_name = 'registration/register.html'
	form_class = PatientRegisterForm
	success_url = '/login/'

	def form_valid(self, form):
		if form.is_valid():
			user = form.save(commit=False)
			user.email = form.cleaned_data.get('email')
			user.user_type = 'patient'
			form.save()
			login(self.request, user)
		return super().form_valid(form)


class Login(LoginView):
	template_name = 'registration/login.html'
	success_url = '/'
