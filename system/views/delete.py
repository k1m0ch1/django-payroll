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
	d = Department.objects.filter(id=department_id)
	d.delete()
	return redirect("department-index")

@login_required()
def bagian(request, bagian_id):
	b = Bagian.objects.filter(id=bagian_id)
	b.delete()
	return redirect("bagian-index")

@login_required()
def golongan(request, golongan_id):
	g = Golongan.objects.filter(id=golongan_id)
	g.delete()
	return redirect("golongan-index")

@login_required()
def jabatan(request, jabatan_id):
	j = Jabatan.objects.filter(id=jabatan_id)
	j.delete()
	return redirect("jabatan-index")

@login_required()
def bank(request, bank_id):
	j = Bank.objects.filter(id=bank_id)
	j.delete()
	return redirect("bank-index")

@login_required()
def agama(request, agama_id):
	a = Agama.objects.filter(id=agama_id)
	a.delete()
	return redirect("agama-index")

@login_required()
def warganegara(request, warganegara_id):
	w = WargaNegara.objects.filter(id=warganegara_id)
	w.delete()
	return redirect("warganegara-index")