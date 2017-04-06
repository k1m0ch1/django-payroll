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
def perusahaan_index(request):
	perusahaan = Perusahaan.objects.all()
	return render(request, "perusahaan/dashboard.html", { 'perusahaan' : perusahaan})

@login_required()
def department_index(request):
	department = Department.objects.all()
	return render(request, "include/base-dashboard.html", { 'ulang' : department, 'module' : DEPARTEMEN})

@login_required()
def bagian_index(request):
	bagian = Bagian.objects.all()
	return render(request, "include/base-dashboard.html", { 'ulang' : bagian, 'module' : BAGIAN})

@login_required()
def golongan_index(request):
	golongan = Golongan.objects.all()
	return render(request, "include/base-dashboard.html", { 'ulang' : golongan, 'module' : GOLONGAN})

@login_required()
def jabatan_index(request):
	jabatan = Jabatan.objects.all()
	return render(request, "include/base-dashboard.html", { 'ulang' : jabatan, 'module' : JABATAN})

@login_required()
def bank_index(request):
	bank = Bank.objects.all()
	return render(request, "include/base-dashboard.html", { 'ulang' : bank, 'module' : BANK})

@login_required()
def agama_index(request):
	agama = Agama.objects.all()
	return render(request, "include/base-dashboard.html", { 'ulang' : agama, 'module' : AGAMA})

@login_required()
def warganegara_index(request):
	warganegara = WargaNegara.objects.all()
	return render(request, "include/base-dashboard.html", { 'ulang' : warganegara, 'module' : WARGANEGARA})

@login_required()
def statusmenikah_index(request):
	statusmenikah = StatusMenikah.objects.all()
	return render(request, "include/base-dashboard.html", { 'ulang' : statusmenikah, 'module' : STATUSMENIKAH})