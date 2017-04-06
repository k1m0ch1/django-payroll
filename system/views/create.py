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
def department(request):
	return render(request, "include/base-form.html", { 'mode' : 'Tambah', 'module' : DEPARTEMEN, 'idpk' : 0})

@login_required()
def department_save(request):
	nama = request.POST['name']
	desc = request.POST['desc']
	d = Department(name=nama, desc=desc)
	d.save()
	return redirect("department-index")

@login_required()
def bagian(request):
	return render(request, "include/base-form.html", { 'mode' : 'Tambah', 'module' : BAGIAN, 'idpk' : 0})

@login_required()
def bagian_save(request):
	nama = request.POST['name']
	desc = request.POST['desc']
	b = Bagian(name=nama, desc=desc)
	b.save()
	return redirect("bagian-index")

@login_required()
def golongan(request):
	return render(request, "include/base-form.html", { 'mode' : 'Tambah', 'module' : GOLONGAN, 'idpk' : 0})

@login_required()
def golongan_save(request):
	nama = request.POST['name']
	desc = request.POST['desc']
	g = Golongan(name=nama, desc=desc)
	g.save()
	return redirect("golongan-index")

@login_required()
def jabatan(request):
	return render(request, "include/base-form.html", { 'mode' : 'Tambah', 'module' : JABATAN, 'idpk' : 0})

@login_required()
def jabatan_save(request):
	nama = request.POST['name']
	desc = request.POST['desc']
	j = Jabatan(name=nama, desc=desc)
	j.save()
	return redirect("jabatan-index")

@login_required()
def bank(request):
	return render(request, "include/base-form.html", { 'mode' : 'Tambah', 'module' : BANK, 'idpk' : 0})

@login_required()
def bank_save(request):
	nama = request.POST['name']
	desc = request.POST['desc']
	b = Bank(name=nama, desc=desc)
	b.save()
	return redirect("bank-index")

@login_required()
def agama(request):
	return render(request, "include/base-form.html", { 'mode' : 'Tambah', 'module' : AGAMA, 'idpk' : 0})

@login_required()
def agama_save(request):
	nama = request.POST['name']
	desc = request.POST['desc']
	a = Agama(name=nama, desc=desc)
	a.save()
	return redirect("agama-index")

@login_required()
def warganegara(request):
	return render(request, "include/base-form.html", { 'mode' : 'Tambah', 'module' : WARGANEGARA, 'idpk' : 0})

@login_required()
def warganegara_save(request):
	nama = request.POST['name']
	desc = request.POST['desc']
	w = WargaNegara(name=nama, desc=desc)
	w.save()
	return redirect("warganegara-index")