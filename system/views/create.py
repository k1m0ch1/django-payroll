from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.template import loader, Context
import django_tables2 as tables
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from system.models import Perusahaan, Department, Bagian, Golongan, Jabatan
from system.models import Bank, Agama, WargaNegara, StatusMenikah

@login_required()
def department(request):
	return render(request, "department/form.html")

@login_required()
def department_save(request):
	nama = request.POST['name']
	desc = request.POST['desc']
	d = Department(name=nama, desc=desc)
	d.save()
	return redirect("department-index")

@login_required()
def bagian(request):
	return render(request, "include/base-form.html", { 'mode' : 'Tambah', 'module' : 'Bagian/ Division', 'idpk' : 0})

@login_required()
def bagian_save(request):
	nama = request.POST['name']
	desc = request.POST['desc']
	b = Bagian(name=nama, desc=desc)
	b.save()
	return redirect("bagian-index")