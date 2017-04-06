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
def department(request, department_id):
	d = Department.objects.get(pk=department_id)
	return render(request, "department/form.html", { 'data' : d })

@login_required()
def department_save(request, department_id):
	d = Department.objects.select_for_update().filter(id=department_id)
	d.update(name=request.POST['name'], desc=request.POST['desc'])
	return redirect("department-index")

@login_required()
def bagian(request, bagian_id):
	b = Bagian.objects.get(pk=bagian_id)
	return render(request, "include/base-form.html", { 'data' : b , 'mode' : 'Tambah', ' module' : 'Bagian/ Division', 'idpk' : bagian_id})

@login_required()
def bagian_save(request, bagian_id):
	b = Bagian.objects.select_for_update().filter(id=bagian_id)
	b.update(name=request.POST['name'], desc=request.POST['desc'])
	return redirect("bagian-index")