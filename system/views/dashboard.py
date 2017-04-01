from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.template import loader, Context
import django_tables2 as tables
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from system.models import Perusahaan, Department, Bagian, Unit, Golongan, Jabatan
from system.models import Bank, Agama, WargaNegara, StatusMenikah

@login_required()
def perusahaan_index(request):
	perusahaan = Perusahaan.objects.all()
	return render(request, "perusahaan/dashboard.html", { 'perusahaan' : perusahaan})

@login_required()
def department_index(request):
	department = Department.objects.all()
	return render(request, "department/dashboard.html", { 'department' : department})

@login_required()
def unit_index(request):
	unit = Unit.objects.all()
	return render(request, "unit/dashboard.html", { 'unit' : unit})

@login_required()
def bagian_index(request):
	bagian = Bagian.objects.all()
	return render(request, "bagian/dashboard.html", { 'bagian' : bagian})

@login_required()
def golongan_index(request):
	golongan = Golongan.objects.all()
	return render(request, "golongan/dashboard.html", { 'golongan' : golongan})

@login_required()
def jabatan_index(request):
	jabatan = Jabatan.objects.all()
	return render(request, "jabatan/dashboard.html", { 'jabatan' : jabatan})

@login_required()
def bank_index(request):
	bank = Bank.objects.all()
	return render(request, "bank/dashboard.html", { 'bank' : bank})

@login_required()
def agama_index(request):
	agama = Agama.objects.all()
	return render(request, "agama/dashboard.html", { 'agama' : agama})

@login_required()
def warganegara_index(request):
	warganegara = WargaNegara.objects.all()
	return render(request, "warganegara/dashboard.html", { 'warganegara' : warganegara})

@login_required()
def statusmenikah_index(request):
	statusmenikah = StatusMenikah.objects.all()
	return render(request, "statusmenikah/dashboard.html", { 'statusmenikah' : statusmenikah})