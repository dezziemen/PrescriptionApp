from django.http import HttpResponse
from django.views.generic import (
	View,
	ListView,
	FormView,
	UpdateView,
	DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from Accounts.models import CustomUser
from .forms import CreateCustomUserForm


class Home(LoginRequiredMixin, View):
	login_url = '/login/'

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			if request.user.user_type == 'admin':
				return redirect('admin_home')
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
			address_checkbox = self.request.GET.get('address_checkbox')
			all_results = CustomUser.objects.none()
			if id_checkbox:
				all_results = all_results | CustomUser.objects.filter(id__icontains=search_query)
			if email_checkbox:
				all_results = all_results | CustomUser.objects.filter(email__icontains=search_query)
			if full_name_checkbox:
				all_results = all_results | CustomUser.objects.filter(full_name__icontains=search_query)
			if phone_number_checkbox:
				all_results = all_results | CustomUser.objects.filter(phone_number__icontains=search_query)
			if address_checkbox:
				all_results = all_results | CustomUser.objects.filter(address__icontains=search_query)
			return all_results
		else:
			return CustomUser.objects.all()

	def get_context_data(self, **kwargs):
		context = super(AdminHome, self).get_context_data(**kwargs)
		context['sort_type'] = self.request.GET.get('sort_type')
		if not context['sort_type']:
			context['sort_type'] = 'id_sort'
		print(f"sort type: {context['sort_type']}")
		if self.request.GET.get('search_query'):
			context['search_query'] = self.request.GET.get('search_query')
			context['id_checkbox'] = self.request.GET.get('id_checkbox')
			context['email_checkbox'] = self.request.GET.get('email_checkbox')
			context['full_name_checkbox'] = self.request.GET.get('full_name_checkbox')
			context['phone_number_checkbox'] = self.request.GET.get('phone_number_checkbox')
			context['address_checkbox'] = self.request.GET.get('address_checkbox')
		else:
			context['search_query'] = False
			context['id_checkbox'] = True
			context['email_checkbox'] = True
			context['full_name_checkbox'] = True
			context['phone_number_checkbox'] = True
			context['address_checkbox'] = True
		return context


class EditUser(UpdateView):
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


class CreateCustomUser(FormView):
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


class DeleteUser(DeleteView):
	model = CustomUser
	success_url = '/'