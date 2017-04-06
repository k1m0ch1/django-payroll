from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.template import loader, Context
import django_tables2 as tables
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from system.models import Perusahaan, Department, Bagian, Golongan, Jabatan
from system.models import Bank, Agama, WargaNegara, StatusMenikah

BAGIAN 			= 'Bagian/ Division'
DEPARTEMEN 		= 'Departemen/ Department'
GOLONGAN 		= 'Golongan/ Category'
JABATAN 		= 'Jabatan/ Occupation'
BANK 			= 'Bank'
AGAMA 			= 'Agama/ Religion'
WARGANEGARA 	= 'Warga Negara/ Nationality'
STATUSMENIKAH 	= 'Status Menikah/ Marital Status'

@login_required()
def department(request, department_id):
	d = Department.objects.get(pk=department_id)
	return render(request, "include/base-form.html", { 'data' : d , 'mode' : 'Ubah', 'module' : DEPARTEMEN, 'idpk' : department_id})

@login_required()
def department_save(request, department_id):
	d = Department.objects.select_for_update().filter(id=department_id)
	d.update(name=request.POST['name'], desc=request.POST['desc'])
	return redirect("department-index")

@login_required()
def bagian(request, bagian_id):
	b = Bagian.objects.get(pk=bagian_id)
	return render(request, "include/base-form.html", { 'data' : b , 'mode' : 'Ubah', 'module' : BAGIAN, 'idpk' : bagian_id})

@login_required()
def bagian_save(request, bagian_id):
	b = Bagian.objects.select_for_update().filter(id=bagian_id)
	b.update(name=request.POST['name'], desc=request.POST['desc'])
	return redirect("bagian-index")

@login_required()
def golongan(request, golongan_id):
	g = Golongan.objects.get(pk=golongan_id)
	return render(request, "include/base-form.html", { 'data' : g , 'mode' : 'Ubah', 'module' : GOLONGAN, 'idpk' : golongan_id})

@login_required()
def golongan_save(request, golongan_id):
	g = Golongan.objects.select_for_update().filter(id=golongan_id)
	g.update(name=request.POST['name'], desc=request.POST['desc'])
	return redirect("golongan-index")

@login_required()
def jabatan(request, jabatan_id):
	j = Jabatan.objects.get(pk=jabatan_id)
	return render(request, "include/base-form.html", { 'data' : j , 'mode' : 'Ubah', 'module' : JABATAN, 'idpk' : jabatan_id})

@login_required()
def jabatan_save(request, jabatan_id):
	j = Jabatan.objects.select_for_update().filter(id=jabatan_id)
	j.update(name=request.POST['name'], desc=request.POST['desc'])
	return redirect("jabatan-index")

@login_required()
def bank(request, bank_id):
	b = Bank.objects.get(pk=bank_id)
	return render(request, "include/base-form.html", { 'data' : b , 'mode' : 'Ubah', 'module' : BANK, 'idpk' : bank_id})

@login_required()
def bank_save(request, bank_id):
	b = Bank.objects.select_for_update().filter(id=bank_id)
	b.update(name=request.POST['name'], desc=request.POST['desc'])
	return redirect("bank-index")

@login_required()
def agama(request, agama_id):
	a = Agama.objects.get(pk=agama_id)
	return render(request, "include/base-form.html", { 'data' : a , 'mode' : 'Ubah', 'module' : AGAMA, 'idpk' : agama_id})

@login_required()
def agama_save(request, agama_id):
	a = Agama.objects.select_for_update().filter(id=agama_id)
	a.update(name=request.POST['name'], desc=request.POST['desc'])
	return redirect("agama-index")

@login_required()
def warganegara(request, warganegara_id):
	w = WargaNegara.objects.get(pk=warganegara_id)
	return render(request, "include/base-form.html", { 'data' : w , 'mode' : 'Ubah', 'module' : WARGANEGARA, 'idpk' : warganegara_id})

@login_required()
def warganegara_save(request, warganegara_id):
	w = WargaNegara.objects.select_for_update().filter(id=warganegara_id)
	w.update(name=request.POST['name'], desc=request.POST['desc'])
	return redirect("warganegara-index")

@login_required()
def statusmenikah(request, statusmenikah_id):
	s = StatusMenikah.objects.get(pk=statusmenikah_id)
	return render(request, "include/base-form.html", { 'data' : s , 'mode' : 'Ubah', 'module' : STATUSMENIKAH, 'idpk' : statusmenikah_id})

@login_required()
def statusmenikah_save(request, statusmenikah_id):
	s = StatusMenikah.objects.select_for_update().filter(id=statusmenikah_id)
	s.update(name=request.POST['name'], desc=request.POST['desc'])
	return redirect("statusmenikah-index")