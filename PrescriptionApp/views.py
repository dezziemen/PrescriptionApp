from django.http import HttpResponse
from django.views.generic import (
	View,
	ListView,
	FormView,
	TemplateView,
	DetailView,
	UpdateView,
	DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from Accounts.models import CustomUser
from Prescriptions.models import Prescription
from .forms import CreateCustomUserForm, ViewUserForm


class Home(LoginRequiredMixin, View):
	login_url = '/login/'

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			if request.user.user_type == 'admin':
				return redirect('admin_home')
			elif request.user.user_type == 'doctor':
				return redirect('doctor_home')
		else:
			return redirect('Accounts:login')


class AdminHome(LoginRequiredMixin, ListView):
	login_url = '/login/'
	template_name = 'admin/admin_home.html'

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			if request.user.user_type == 'admin':
				print('user is admin')
				return self.get(request, *args, **kwargs)
			else:
				return redirect('home')
		else:
			return redirect('Accounts:login')

	def get_queryset(self):
		if self.request.GET.get('search_query'):
			search_query = self.request.GET.get('search_query')
			id_checkbox = self.request.GET.get('id_checkbox')
			email_checkbox = self.request.GET.get('email_checkbox')
			full_name_checkbox = self.request.GET.get('full_name_checkbox')
			phone_number_checkbox = self.request.GET.get('phone_number_checkbox')
			user_type_checkbox = self.request.GET.get('user_type_checkbox')
			all_results = CustomUser.objects.none()
			if id_checkbox:
				all_results = all_results | CustomUser.objects.filter(id__icontains=search_query)
			if email_checkbox:
				all_results = all_results | CustomUser.objects.filter(email__icontains=search_query)
			if full_name_checkbox:
				all_results = all_results | CustomUser.objects.filter(full_name__icontains=search_query)
			if phone_number_checkbox:
				all_results = all_results | CustomUser.objects.filter(phone_number__icontains=search_query)
			if user_type_checkbox:
				all_results = all_results | CustomUser.objects.filter(user_type__icontains=search_query)
			return all_results
		else:
			return CustomUser.objects.all()

	def get_context_data(self, **kwargs):
		context = super(AdminHome, self).get_context_data(**kwargs)
		if self.request.GET.get('search_query'):
			context['search_query'] = self.request.GET.get('search_query')
			context['id_checkbox'] = self.request.GET.get('id_checkbox')
			context['email_checkbox'] = self.request.GET.get('email_checkbox')
			context['full_name_checkbox'] = self.request.GET.get('full_name_checkbox')
			context['phone_number_checkbox'] = self.request.GET.get('phone_number_checkbox')
			context['user_type_checkbox'] = self.request.GET.get('user_type_checkbox')
		else:
			context['search_query'] = False
			context['id_checkbox'] = True
			context['email_checkbox'] = True
			context['full_name_checkbox'] = True
			context['phone_number_checkbox'] = True
			context['user_type_checkbox'] = True
		return context


class EditUser(LoginRequiredMixin, UpdateView):
	login_url = '/login/'
	template_name = 'admin/edit_user.html'
	model = CustomUser
	fields = ['user_type', 'email', 'full_name', 'phone_number', 'address', ]
	success_url = '/'

	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			if request.user.user_type != 'admin':
				print('edit page: user is not admin')
				return redirect('home')
		return super().get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		if self.object.is_superuser:
			context['is_superuser'] = True
		return context


class CreateCustomUser(LoginRequiredMixin, FormView):
	login_url = '/login/'
	template_name = 'admin/create_user.html'
	form_class = CreateCustomUserForm
	success_url = '/home/admin/'

	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			if request.user.user_type == 'admin':
				return super(CreateCustomUser, self).get(request, *args, **kwargs)
			else:
				return redirect('home')
		return redirect('Accounts:login')

	def form_valid(self, form):
		user = form.save(commit=False)
		user.email = form.cleaned_data.get('email')
		form.save()
		return redirect(self.get_success_url())


class DeleteUser(LoginRequiredMixin, DeleteView):
	login_url = '/login/'
	model = CustomUser
	success_url = '/'

	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			if request.user.user_type != 'admin':
				return redirect('home')
		return super().get(request, *args, **kwargs)


class ViewUser(LoginRequiredMixin, UpdateView):
	login_url = '/login/'
	template_name = 'admin/view_user.html'
	model = CustomUser
	form_class = ViewUserForm
	success_url = '/'

	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			if request.user.user_type != 'admin':
				print('view page: user is not admin')
				return redirect('home')
		return super().get(request, *args, **kwargs)


class DoctorHome(LoginRequiredMixin, ListView):
	login_url = '/login/'
	model = CustomUser
	template_name = 'doctor/doctor_home.html'

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			if request.user.user_type == 'doctor':
				print('user is doctor')
				return self.get(request, *args, **kwargs)
			else:
				return redirect('home')
		else:
			return redirect('Accounts:login')

	def get_queryset(self):
		if self.request.GET.get('search_query'):
			search_query = self.request.GET.get('search_query')
			email_checkbox = self.request.GET.get('email_checkbox')
			full_name_checkbox = self.request.GET.get('full_name_checkbox')
			phone_number_checkbox = self.request.GET.get('phone_number_checkbox')
			all_results = CustomUser.objects.none()
			if email_checkbox:
				all_results = all_results | CustomUser.objects.filter(email__icontains=search_query)
			if full_name_checkbox:
				all_results = all_results | CustomUser.objects.filter(full_name__icontains=search_query)
			if phone_number_checkbox:
				all_results = all_results | CustomUser.objects.filter(phone_number__icontains=search_query)
			return all_results.filter(user_type='patient')
		return CustomUser.objects.all().filter(user_type='patient')

	def get_context_data(self, **kwargs):
		context = super(DoctorHome, self).get_context_data(**kwargs)
		if self.request.GET.get('search_query'):
			context['search_query'] = self.request.GET.get('search_query')
			context['email_checkbox'] = self.request.GET.get('email_checkbox')
			context['full_name_checkbox'] = self.request.GET.get('full_name_checkbox')
			context['phone_number_checkbox'] = self.request.GET.get('phone_number_checkbox')
		else:
			context['search_query'] = False
			context['email_checkbox'] = True
			context['full_name_checkbox'] = True
			context['phone_number_checkbox'] = True
		return context


class ViewPatient(LoginRequiredMixin, DetailView):
	login_url = '/login/'
	model = CustomUser
	template_name = 'doctor/view_patient.html'

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			if request.user.user_type == 'doctor':
				print('user is doctor')
				return self.get(request, *args, **kwargs)
			else:
				return redirect('home')
		else:
			return redirect('Accounts:login')

	def get_object(self, queryset=None):
		if queryset is None:
			queryset = self.get_queryset()
		pk = self.kwargs.get(self.pk_url_kwarg)
		queryset = queryset.filter(pk=pk)
		try:
			obj = queryset.get()
		except queryset.model.DoesNotExist:
			return HttpResponse("No CustomUser found matching the query")
		return obj


class Prescribe(LoginRequiredMixin, FormView):
	pass