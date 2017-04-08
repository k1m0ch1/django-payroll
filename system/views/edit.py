from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.template import loader, Context
import django_tables2 as tables
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from system.models import Perusahaan, Departemen, Bagian, Golongan, Jabatan
from system.models import Bank, Agama, WargaNegara, StatusMenikah, Modules
from system.models import LokasiPerusahaan

modules = Modules.objects.all()
allmenu = Modules.objects.only('name')

@login_required()
def departemen(request, departemen_id):
	d = Departemen.objects.get(pk=departemen_id)
	return render(request, "include/base-form.html", { 'data' : d , 'mode' : 'Ubah', 'module' : getModule(request), 
													   'idpk' : departemen_id, 'dsb' : modules, 'parent' : getParent(request)})

@login_required()
def departemen_save(request, departemen_id):
	d = Departemen.objects.select_for_update().filter(id=departemen_id)
	d.update(name=request.POST['name'], desc=request.POST['desc'])
	return redirect("departemen-index")

@login_required()
def bagian(request, bagian_id):
	b = Bagian.objects.get(pk=bagian_id)
	return render(request, "include/base-form.html", { 'data' : b , 'mode' : 'Ubah', 'module' : getModule(request), 
													   'idpk' : bagian_id, 'dsb' : modules, 'parent' : getParent(request)})

@login_required()
def bagian_save(request, bagian_id):
	b = Bagian.objects.select_for_update().filter(id=bagian_id)
	b.update(name=request.POST['name'], desc=request.POST['desc'])
	return redirect("bagian-index")

@login_required()
def golongan(request, golongan_id):
	g = Golongan.objects.get(pk=golongan_id)
	return render(request, "include/base-form.html", { 'data' : g , 'mode' : 'Ubah', 'module' : getModule(request),
													   'idpk' : golongan_id, 'dsb' : modules, 'parent' : getParent(request)})

@login_required()
def golongan_save(request, golongan_id):
	g = Golongan.objects.select_for_update().filter(id=golongan_id)
	g.update(name=request.POST['name'], desc=request.POST['desc'])
	return redirect("golongan-index")

@login_required()
def jabatan(request, jabatan_id):
	j = Jabatan.objects.get(pk=jabatan_id)
	return render(request, "include/base-form.html", { 'data' : j , 'mode' : 'Ubah', 'module' : getModule(request), 
													   'idpk' : jabatan_id, 'dsb' : modules, 'parent' : getParent(request)})

@login_required()
def jabatan_save(request, jabatan_id):
	j = Jabatan.objects.select_for_update().filter(id=jabatan_id)
	j.update(name=request.POST['name'], desc=request.POST['desc'])
	return redirect("jabatan-index")

@login_required()
def bank(request, bank_id):
	b = Bank.objects.get(pk=bank_id)
	return render(request, "include/base-form.html", { 'data' : b , 'mode' : 'Ubah', 'module' : getModule(request), 
													   'idpk' : bank_id, 'dsb' : modules, 'parent' : getParent(request)})

@login_required()
def bank_save(request, bank_id):
	b = Bank.objects.select_for_update().filter(id=bank_id)
	b.update(name=request.POST['name'], desc=request.POST['desc'])
	return redirect("bank-index")

@login_required()
def agama(request, agama_id):
	a = Agama.objects.get(pk=agama_id)
	return render(request, "include/base-form.html", { 'data' : a , 'mode' : 'Ubah', 'module' : getModule(request), 
													   'idpk' : agama_id, 'dsb' : modules, 'parent' : getParent(request)})

@login_required()
def agama_save(request, agama_id):
	a = Agama.objects.select_for_update().filter(id=agama_id)
	a.update(name=request.POST['name'], desc=request.POST['desc'])
	return redirect("agama-index")

@login_required()
def warganegara(request, warganegara_id):
	w = WargaNegara.objects.get(pk=warganegara_id)
	return render(request, "include/base-form.html", { 'data' : w , 'mode' : 'Ubah', 'module' : getModule(request), 
													   'idpk' : warganegara_id, 'dsb' : modules, 'parent' : getParent(request)})

@login_required()
def warganegara_save(request, warganegara_id):
	w = WargaNegara.objects.select_for_update().filter(id=warganegara_id)
	w.update(name=request.POST['name'], desc=request.POST['desc'])
	return redirect("warganegara-index")

@login_required()
def statusmenikah(request, statusmenikah_id):
	s = StatusMenikah.objects.get(pk=statusmenikah_id)
	return render(request, "include/base-form.html", { 'data' : s , 'mode' : 'Ubah', 'module' : getModule(request), 
													   'idpk' : statusmenikah_id, 'dsb' : modules, 'parent' : getParent(request)})

@login_required()
def statusmenikah_save(request, statusmenikah_id):
	s = StatusMenikah.objects.select_for_update().filter(id=statusmenikah_id)
	s.update(name=request.POST['name'], desc=request.POST['desc'])
	return redirect("statusmenikah-index")

@login_required()
def profile_perusahaan(request, lokasiperusahaan_id):
	s = LokasiPerusahaan.objects.get(pk=lokasiperusahaan_id)
	return render(request, "profile-perusahaan/form.html", { 'data' : s , 'mode' : 'Ubah', 'module' : "Lokasi Perusahaan", 
													   		 'idpk' : lokasiperusahaan_id, 'dsb' : modules, 'parent' : getParent(request)})

@login_required()
def profile_perusahaan_save(request, lokasiperusahaan_id):
	s = LokasiPerusahaan.objects.select_for_update().filter(id=lokasiperusahaan_id)
	s.update(alamat=request.POST['name'], desc=request.POST['desc'])
	return redirect("profile-perusahaan-index")

@login_required()
def profile_edit(request):
	s = Perusahaan.objects.get(pk=1)
	return render(request, "include/base-form.html", { 'data' : s , 'mode' : 'Ubah', 'module' : getModule(request), 
													   		 'idpk' : 1, 'dsb' : modules, 'parent' : getParent(request)})

@login_required()
def profile_edit_save(request):
	s = Perusahaan.objects.select_for_update().filter(id=1)
	s.update(name=request.POST['name'], desc=request.POST['desc'])
	return redirect("profile-perusahaan-index")


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