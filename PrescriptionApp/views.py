import datetime

from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.views.generic import (
	View,
	ListView,
	FormView,
	TemplateView,
	DetailView,
	CreateView,
	UpdateView,
	DeleteView,
	RedirectView,
)
from django.views.generic.base import ContextMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from Accounts.models import CustomUser
from Prescriptions.models import Prescription, MedicineCart, MedicineQuantity, Medicine
from Accounts.forms import CreateCustomUserForm, ViewUserForm
from Prescriptions.forms import PrescriptionCreationForm, MedicineQuantityCreationForm, MedicineCreationForm, ViewPrescriptionForm


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


class AdminHome(LoginRequiredMixin, TemplateView):
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

	def get_context_data(self, **kwargs):
		context = super(AdminHome, self).get_context_data(**kwargs)
		context['items'] = []
		all_results = CustomUser.objects.none()
		if self.request.GET.get('search_query'):
			search_query = self.request.GET.get('search_query')
			id_checkbox = self.request.GET.get('id_checkbox')
			email_checkbox = self.request.GET.get('email_checkbox')
			full_name_checkbox = self.request.GET.get('full_name_checkbox')
			phone_number_checkbox = self.request.GET.get('phone_number_checkbox')
			user_type_checkbox = self.request.GET.get('user_type_checkbox')
			context.update({
				'search_query': search_query,
				'id_checkbox': id_checkbox,
				'email_checkbox': email_checkbox,
				'full_name_checkbox': full_name_checkbox,
				'phone_number_checkbox': phone_number_checkbox,
				'user_type_checkbox': user_type_checkbox,
			})
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
		else:
			all_results = CustomUser.objects.all()
			context.update({
				'search_query': False,
				'id_checkbox': True,
				'email_checkbox': True,
				'full_name_checkbox': True,
				'phone_number_checkbox': True,
				'user_type_checkbox': True,
			})
		for result in all_results:
			context['items'].append([
				result.id,
				[
					result.id,
					result.email,
					result.full_name,
					result.phone_number,
					result.user_type,
				]
			])
		context['titles'] = [
			'ID',
			'Email',
			'Full Name',
			'Phone Number',
			'User Type',
		]
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


class DoctorHome(LoginRequiredMixin, TemplateView):
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

	def get_context_data(self, **kwargs):
		context = super(DoctorHome, self).get_context_data(**kwargs)
		context['items'] = []
		all_results = CustomUser.objects.none()
		if self.request.GET.get('search_query'):
			search_query = self.request.GET.get('search_query')
			email_checkbox = self.request.GET.get('email_checkbox')
			full_name_checkbox = self.request.GET.get('full_name_checkbox')
			phone_number_checkbox = self.request.GET.get('phone_number_checkbox')
			if email_checkbox:
				all_results = all_results | CustomUser.objects.filter(email__icontains=search_query)
			if full_name_checkbox:
				all_results = all_results | CustomUser.objects.filter(full_name__icontains=search_query)
			if phone_number_checkbox:
				all_results = all_results | CustomUser.objects.filter(phone_number__icontains=search_query)
			all_results = all_results.filter(user_type='patient')
		else:
			all_results = CustomUser.objects.filter(user_type='patient')
		for result in all_results:
			context['items'].append([
				result.id,
				[
					result.email,
					result.full_name,
					result.phone_number,
				]
			])
		context['titles'] = [
			'Email',
			'Full Name',
			'Phone Number',
		]
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


class ViewPatient(LoginRequiredMixin, UpdateView):
	login_url = '/login/'
	model = CustomUser
	form_class = ViewUserForm
	template_name = 'doctor/view_patient.html'

	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			if request.user.user_type != 'doctor':
				print('user is not doctor')
				return redirect('home')
		return super().get(request, *args, **kwargs)

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

	def get_context_data(self, **kwargs):
		context = super(ViewPatient, self).get_context_data(**kwargs)
		pk = self.kwargs.get(self.pk_url_kwarg)
		prescriptions = Prescription.objects.filter(patient_id=pk)
		context['items'] = []
		for item in prescriptions:
			context['items'].append([
				item.id,
				[
					item.date,
					item.doctor,
					item.pharmacist,
					item.collected
				]
			])
		context['titles'] = [
			'Date',
			'Doctor',
			'Pharmacist',
			'Collected',
		]
		return context


class Prescribe(LoginRequiredMixin, CreateView):
	login_url = '/login/'
	model = MedicineQuantity
	form_class = MedicineQuantityCreationForm
	template_name = 'doctor/create_prescription.html'

	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			if request.user.user_type != 'doctor':
				return redirect('home')
		return super().get(request, *args, **kwargs)

	def get_success_url(self, **kwargs):
		return reverse_lazy('prescribe', kwargs={'pk': self.kwargs.get(self.pk_url_kwarg)})

	def form_valid(self, form):
		medicine = form.save(commit=False)
		pk = self.kwargs.get(self.pk_url_kwarg)
		medicine_cart, _ = MedicineCart.objects.get_or_create(patient_id=pk)
		print(medicine.prescription)
		medicine.prescription = None
		medicine.medicine_cart = medicine_cart
		print(medicine)
		medicine.save()
		return super().form_valid(form)

	def get_context_data(self, **kwargs):
		pk = self.kwargs.get(self.pk_url_kwarg)
		context = super(Prescribe, self).get_context_data()
		# select_related gets the Medicine ForeignKey in MedicineQuantity
		context['items'] = []
		results = MedicineQuantity.objects.filter(medicine_cart__patient_id=pk).select_related('medicine')
		for item in results:
			context['items'].append([
				item.id,
				[
					item.medicine,
					item.quantity,
					item.medicine.tablets,
					item.medicine.volume,
				]
			])
			# Ensure that MedicineQuantity is not linked to any Prescriptions yet
			item.prescription = None
		context['titles'] = [
			'Medicine',
			'Quantity',
			'Tablets',
			'Volume',
		]
		# for item in context['items']:
		# 	item.prescription = None
		# 	print(item)
		context['cart'], _ = MedicineCart.objects.get_or_create(patient_id=pk)
		context['pk'] = pk
		return context


class CreateMedicine(LoginRequiredMixin, CreateView):
	login_url = '/login/'
	form_class = MedicineCreationForm
	template_name = 'doctor/create_medicine.html'
	success_url = '/'

	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			if request.user.user_type != 'doctor':
				return redirect('home')
		return super().get(request, *args, **kwargs)


class EditCartItem(LoginRequiredMixin, UpdateView):
	login_url = '/login/'
	model = MedicineQuantity
	fields = ['medicine', 'quantity']
	template_name = 'doctor/edit_cart_item.html'

	def get_success_url(self, **kwargs):
		patient_pk = MedicineQuantity.objects.get(pk=self.kwargs.get('pk')).medicine_cart.patient_id
		return reverse_lazy('prescribe', kwargs={'pk': patient_pk})

	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			if request.user.user_type != 'doctor':
				return redirect('home')
		return super().get(request, *args, **kwargs)

	def get_object(self, queryset=None):
		obj = MedicineQuantity.objects.get(id=self.kwargs.get('pk'))
		return obj

	def get_context_data(self, **kwargs):
		context = super(EditCartItem, self).get_context_data()
		return context


class DeleteMedicine(LoginRequiredMixin, DeleteView):
	login_url = '/login/'
	model = MedicineQuantity

	def get_success_url(self, **kwargs):
		patient_pk = MedicineQuantity.objects.get(pk=self.kwargs.get('pk')).medicine_cart.patient_id
		return reverse_lazy('prescribe', kwargs={'pk': patient_pk})

	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			if request.user.user_type != 'doctor':
				return redirect('home')
		return super().get(request, *args, **kwargs)


class SubmitPrescription(LoginRequiredMixin, View):
	login_url = '/login/'

	def dispatch(self, request, *args, **kwargs):
		print('submitting...')
		pk = self.kwargs.get('pk')
		medicine_quantity = MedicineQuantity.objects.filter(medicine_cart__patient_id=pk)
		prescription = Prescription(doctor=request.user, patient_id=pk)
		prescription.save()
		for med in medicine_quantity:
			print(f'Before: {med.prescription}, {med.medicine_cart}')
			med.prescription = prescription
			med.medicine_cart = None
			print(f'After: {med.prescription}, {med.medicine_cart}')
			med.save()
		return redirect('view_patient', pk=pk)


class ViewPrescription(LoginRequiredMixin, UpdateView):
	template_name = 'doctor/view_prescription.html'
	model = Prescription
	form_class = ViewPrescriptionForm

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			if request.user.user_type == 'doctor':
				return self.get(request, *args, **kwargs)
			else:
				return redirect('home')
		else:
			return redirect('Accounts:login')

	def get_context_data(self, *, object_list=None, **kwargs):
		pk = self.kwargs.get('pk')
		context = super(ViewPrescription, self).get_context_data()
		medicine_quantity = MedicineQuantity.objects.filter(prescription_id=pk).select_related('medicine')
		context['items'] = []
		for item in medicine_quantity:
			context['items'].append([
				item.id,
				[
					item.medicine,
					item.quantity,
					item.medicine.tablets,
					item.medicine.volume,
				]
			])
		context['titles'] = [
			'Medicine',
			'Quantity',
			'Tablets',
			'Volume',
		]
		context['prescription_id'] = pk
		for item in medicine_quantity:
			print(item)
		return context

	def get_object(self, queryset=None):
		pk = self.kwargs.get('pk')
		obj = Prescription.objects.select_related('doctor').get(id=pk)
		print(f'obj:\n{obj}')
		print(obj.doctor)
		return obj
