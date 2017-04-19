from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.template import loader, Context
import django_tables2 as tables
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from system.models import Perusahaan, Departemen, Bagian, Golongan, Jabatan
from system.models import Bank, Agama, WargaNegara, StatusMenikah, Modules
from system.models import LokasiPerusahaan, Karyawan, HariRaya, KaryawanShift, Shift
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from sys import getsizeof

modules = Modules.objects.all()
allmenu = Modules.objects.only('name')

@login_required()
def shift_index(request):
	k = Karyawan.objects.all()
	dep = Departemen.objects.all()
	bag = Bagian.objects.all()
	gol = Golongan.objects.all()
	jab = Jabatan.objects.all()
	shift = Shift.objects.all()
	ks = KaryawanShift.objects.all()

	karyawan_list = Karyawan.objects.all()
	page = request.GET.get('page', 1)
	paginator = Paginator(karyawan_list, 10)	
    
	try:
 		k = paginator.page(page)
	except PageNotAnInteger:
		k = paginator.page(1)
	except EmptyPage:
   		k = paginator.page(paginator.num_pages)

	return render(request, "karyawanshift/dashboard.html", { 'dsb' : modules, 'karyawan': k, 'departemen' : dep, 'bagian': bag,
															 'golongan' : gol, 'jabatan' : jab, 'ks': ks, 'shift' : shift})

@login_required()
def hariraya_index(request):
	hariraya = HariRaya.objects.all()
	return render(request, "hariraya/dashboard.html", { 'ulang' : hariraya, 'module' : getModule(request), 'dsb' : modules, 'parent' : getParent(request)})

@login_required()
def karyawan_index(request):
	karyawan_list = Karyawan.objects.all()
	page = request.GET.get('page', 1)
	paginator = Paginator(karyawan_list, 10)	
    
	try:
 		karyawan = paginator.page(page)
	except PageNotAnInteger:
		karyawan = paginator.page(1)
	except EmptyPage:
   		karyawan = paginator.page(paginator.num_pages)

	return render(request, "karyawan/dashboard.html", { 'karyawan' : karyawan, 'dsb' : modules})

@login_required()
def karyawan_detail(request, karyawan_id):
	karyawan = Karyawan.objects.get(pk=karyawan_id)
	return render(request, "karyawan/detail.html", {'karyawan':karyawan, 'dsb': modules})

@login_required()
def perusahaan_index(request):
	perusahaan = Perusahaan.objects.all()
	return render(request, "perusahaan/dashboard.html", { 'perusahaan' : perusahaan, 'dsb' : modules })

@login_required()
def departemen_index(request):
	departemen = Departemen.objects.all()
	return render(request, "include/base-dashboard.html", { 'ulang' : departemen, 'module' : getModule(request), 'dsb' : modules, 'parent' : getParent(request) })

@login_required()
def bagian_index(request):
	bagian = Bagian.objects.all()
	return render(request, "include/base-dashboard.html", { 'ulang' : bagian, 'module' : getModule(request), 'dsb' : modules, 'parent' : getParent(request)})

@login_required()
def golongan_index(request):
	golongan = Golongan.objects.all()
	return render(request, "include/base-dashboard.html", { 'ulang' : golongan, 'module' : getModule(request), 'dsb' : modules, 'parent' : getParent(request)})

@login_required()
def jabatan_index(request):
	jabatan = Jabatan.objects.all()
	return render(request, "include/base-dashboard.html", { 'ulang' : jabatan, 'module' : getModule(request), 'dsb' : modules, 'parent' : getParent(request)})

@login_required()
def bank_index(request):
	bank = Bank.objects.all()
	return render(request, "include/base-dashboard.html", { 'ulang' : bank, 'module' : getModule(request), 'dsb' : modules, 'parent' : getParent(request)})

@login_required()
def agama_index(request):
	agama = Agama.objects.all()
	return render(request, "include/base-dashboard.html", { 'ulang' : agama, 'module' : getModule(request), 'dsb' : modules, 'parent' : getParent(request)})

@login_required()
def warganegara_index(request):
	warganegara = WargaNegara.objects.all()
	return render(request, "include/base-dashboard.html", { 'ulang' : warganegara, 'module' : getModule(request), 'dsb' : modules, 'parent' : getParent(request)})

@login_required()
def statusmenikah_index(request):
	statusmenikah = StatusMenikah.objects.all()
	return render(request, "include/base-dashboard.html", { 'ulang' : statusmenikah, 'module' : getModule(request), 'dsb' : modules, 'parent' : getParent(request)})

@login_required()
def profile_perusahaan_index(request):
	lokasi = LokasiPerusahaan.objects.all()
	perusahaan = Perusahaan.objects.get(id=1)
	#return render(request, "profile-perusahaan/dashboard.html", { 'ulang' : lokasi, 'module' : PROFILEPERUSAHAAN})
	return render(request, "profile-perusahaan/dashboard.html", {'ulang': lokasi, 'perusahaan' : perusahaan, 'module' : getModule(request), 
																 'dsb' : modules, 'parent' : getParent(request)})

def getModule(request):
	getmodule = [x.strip() for x in request.get_full_path().split('/')][2]
	for sb in modules:
		if getmodule.upper() == sb.name:
			return sb.fungsi

def getParent(request):
	getmodule = [x.strip() for x in request.get_full_path().split('/')][2]
	for sb in modules:
		if getmodule.upper() == sb.name:
			return sb.menu