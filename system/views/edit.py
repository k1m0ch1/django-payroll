from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.template import loader, Context
import django_tables2 as tables
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from system.models import Perusahaan, Departemen, Bagian, Golongan, Jabatan, Konfigurasi
from system.models import Bank, Agama, WargaNegara, StatusMenikah, Modules, Inventory
from system.models import LokasiPerusahaan, Karyawan, HariRaya, KaryawanShift, Shift
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from sys import getsizeof
from django.core import serializers
import json
from dateutil.parser import parse

modules = Modules.objects.all()
allmenu = Modules.objects.only('name')

@login_required()
def karyawan_shift(request):
	idkaryawan = request.POST['idkaryawan']
	listid = [x.strip() for x in idkaryawan.split(',')]
	tanggal = request.POST['tanggal']
	tglawal = parse([x.strip() for x in tanggal.split(' ')][0]).strftime("%Y-%m-%d")
	tglakhir = parse([x.strip() for x in tanggal.split(' ')][2]).strftime("%Y-%m-%d")
	for y in range(0, len(listid)-1):
		ks  = KaryawanShift.objects.select_for_update().filter(karyawan_id=listid[y]).filter(tglawal=tglawal).filter(tglakhir=tglakhir)
		ks.update(shift_id=request.POST['shift'])
	return HttpResponse("Berhasil Simpan")

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
def shift(request, shift_id):
	d = Shift.objects.get(pk=shift_id)
	return render(request, "include/base-form.html", { 'data' : d , 'mode' : 'Ubah', 'module' : getModule(request), 
													   'idpk' : shift_id, 'dsb' : modules, 'parent' : getParent(request)})

@login_required()
def shift_save(request, shift_id):
	d = Shift.objects.select_for_update().filter(id=shift_id)
	d.update(name=request.POST['name'], desc=request.POST['desc'])
	return redirect("shift-index")

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

@login_required()
def hariraya(request, hariraya_id):
	s = HariRaya.objects.get(pk=hariraya_id)
	return render(request, "include/base-form.html", { 'data' : s , 'mode' : 'Ubah', 'module' : getModule(request), 
													   		 'idpk' : hariraya_id, 'dsb' : modules, 'parent' : getParent(request)})

@login_required()
def hariraya_save(request, hariraya_id):
	name = request.POST['name']
	tanggal = request.POST['desc']
	sd = request.POST['desc']
	desc = request.POST['desc']
	s = HariRaya.objects.select_for_update().filter(id=hariraya_id)
	s.update(name=name, tanggal=tanggal, sd=sd, desc=desc)
	return redirect("hariraya-index")


@login_required()
def inventory(request, inventory_id):
	s = Inventory.objects.get(pk=inventory_id)
	exfield = [{"name": "nomer","type":"text", "placeholder":"Nomer Barang", "label":"Nomer Barang", "data" : s.nomer}]
	return render(request, "include/base-dyn-form.html", { 'data' : s , 'mode' : 'Ubah', 'module' : getModule(request), 
													   		 'idpk' : inventory_id, 'dsb' : modules, 'parent' : getParent(request),
													   		 'exfield' : exfield
													   	})

@login_required()
def inventory_save(request, inventory_id):
	name = request.POST['name']
	nomer = request.POST['nomer']
	desc = request.POST['desc']
	s = Inventory.objects.select_for_update().filter(id=inventory_id)
	s.update(name=name, nomer=nomer, desc=desc)
	return redirect("inventory-index")

@login_required()
def konfigurasi(request, konfigurasi_id):
	s = Inventory.objects.get(pk=konfigurasi_id)
	exfield = [{"name": "value","type":"text", "placeholder":"Values", "label":"Value", "data" : s.value}]
	return render(request, "include/base-dyn-form.html", { 'data' : s , 'mode' : 'Ubah', 'module' : getModule(request), 
													   		 'idpk' : inventory_id, 'dsb' : modules, 'parent' : getParent(request),
													   		 'exfield' : exfield
													   	})

@login_required()
def konfigurasi_save(request, konfigurasi_id):
	name = request.POST['name']
	value = request.POST['value']
	desc = request.POST['desc']
	s = Inventory.objects.select_for_update().filter(id=konfigurasi_id)
	s.update(name=name, value=value, desc=desc)
	return redirect("konfigurasi-index")


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