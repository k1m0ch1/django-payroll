from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.template import loader, Context
import django_tables2 as tables
from django.template import RequestContext
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from system.models import Perusahaan, Departemen, Modules, Karyawan

modules = Modules.objects.all()

@login_required()
def index(request):
	banyak = Karyawan.objects.all().count()
	dataPayroll = { 'dsb' : modules, 'banyakKaryawan' :  banyak }
	return render(request, "dashboard.html", dataPayroll)

def loginpage(request):
	return render(request, "login.html", { 'login' : "firsttime"})

def loginrequest(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username, password=password)
	if user is not None:
		auth_login(request, user)
		return render(request, "login.html", { 'login' : "berhasil"})
	else:
		return render(request, "login.html", { 'login' : "gagal"})

@login_required()
def logout_view(request):
	logout(request)
	return render(request, "login.html", { 'login' : "logout"})

@login_required()
def perusahaan_edit(request):
	return HttpResponse("edit")

@login_required()
def departemen_edit(request):
	return HttpResponse("edit")

@login_required()
def perusahaan_delete(request):
	return HttpResponse("Delete")

@login_required()
def departemen_delete(request):
	return HttpResponse("Delete")