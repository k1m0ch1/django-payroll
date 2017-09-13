from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.template import loader, Context
import django_tables2 as tables
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from system.models import Perusahaan, Departemen, Bagian, Golongan, Jabatan, Konfigurasi
from system.models import Bank, Agama, WargaNegara, StatusMenikah, Modules, Inventory, Absensi
from system.models import LokasiPerusahaan, Karyawan, HariRaya, KaryawanShift, Shift, GajiPokok
from system.models import MasaTenggangClosing, TunjanganKaryawan, PotonganKaryawan
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from sys import getsizeof
from django.core import serializers
import json
from dateutil.parser import parse

modules = Modules.objects.all()
allmenu = Modules.objects.only('name')

@login_required()
def karyawan(request, karyawan_id):
	per = Perusahaan.objects.all()
	dep = Departemen.objects.all()
	bag = Bagian.objects.all()
	gol = Golongan.objects.all()
	jab = Jabatan.objects.all()
	wg = WargaNegara.objects.all()
	sm = StatusMenikah.objects.all()
	bank = Bank.objects.all()
	agama = Agama.objects.all()
	kar = Karyawan.objects.get(pk=karyawan_id)
	gajipokok = GajiPokok.objects.get(karyawan_id=karyawan_id)

	return render(request, "karyawan/form.html", { 'mode' : 'Ubah', 'module' : getModule(request), 
													   'idpk' : 0, 'dsb' : modules, 'parent' : getParent(request), 'departemen':dep,
													   'bagian': bag, 'golongan':gol, 'jabatan': jab, 'warganegara' : wg,
													   'statusmenikah' : sm, 'bank':bank, 'agama':agama,
													   'perusahaan': per, 'karyawan': kar, 'gajipokok': gajipokok })

@login_required()
def karyawan_save(request, karyawan_id):
	k = Karyawan.objects.select_for_update().filter(id=karyawan_id)
	g = GajiPokok.objects.filter(karyawan_id=karyawan_id)

	k.update(NIK = request.POST['NIK'], name = request.POST['nama1'],
			shortname = request.POST['nama1'], tempatlahir = request.POST['tempatlahir'],
			tanggallahir = parse(request.POST['tanggallahir']).strftime("%Y-%m-%d"), gender = request.POST['gender'],
			alamat = request.POST['alamat'], kota = request.POST['kota'],
			provinsi = request.POST['provinsi'], telepon = request.POST['telepon'],
			handphone = request.POST['handphone'], statuskaryawan = request.POST['statuskaryawan'],
			masakaryawan = parse(request.POST['masakaryawan']).strftime("%Y-%m-%d"), ktpid = request.POST['ktp'],
			warganegara_id = request.POST['warganegara'], agama_id = request.POST['agama'],
			statusmenikah_id = request.POST['statusmenikah'], bank_id = request.POST['bank'],
			norek = request.POST['norekening'], atasnama = request.POST['atasnama'],
			fingerid = request.POST['fingerid'], NPWP = request.POST['NPWP'],
			KPJ = request.POST['KPJ'], jumlahhari = request.POST['jumlahhari'],
			departemen_id = request.POST['departemen'], bagian_id = request.POST['bagian'],
			golongan_id = request.POST['golongan'], #jabatan_id = request.POST['jabatan'],
			perusahaan_id= request.POST['perusahaan'])

	if len(g)>0:
		g.update(name="Gaji Pokok ", gajipokok=request.POST['gajipokok'], jumlahhari = request.POST['jumlahhari'],
					tmakan = request.POST['tmakan'], transportnonexec = request.POST['transportnonexec'])
	else:
		g = GajiPokok(karyawan_id=k.id, name="Gaji Pokok " + k.name, gajipokok=request.POST['gajipokok'], jumlahhari = request.POST['jumlahhari'],	
					tmakan = request.POST['tmakan'], transportnonexec = request.POST['transportnonexec'])
		g.save()

	return redirect("karyawan-index")

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
def masatenggangclosing(request, masatenggangclosing_id):
	d = MasaTenggangClosing.objects.get(pk=masatenggangclosing_id)
	return render(request, "masatenggangclosing/form.html", { 'data' : d , 'mode' : 'Ubah', 'module' : getModule(request), 
													   'idpk' : d.id, 'dsb' : modules, 'parent' : getParent(request)})

@login_required()
def masatenggangclosing_save(request, masatenggangclosing_id):
	d = MasaTenggangClosing.objects.select_for_update().filter(id=masatenggangclosing_id)
	d.update(name=request.POST['name'], tanggal = parse(request.POST['tanggal']).strftime("%Y-%m-%d"), sd = parse(request.POST['sd']).strftime("%Y-%m-%d"), desc=request.POST['desc'])
	return redirect("masatenggangclosing-index")

@login_required()
def hariraya(request, hariraya_id):
	d = HariRaya.objects.get(pk=hariraya_id)
	return render(request, "hariraya/form.html", { 'data' : d , 'mode' : 'Ubah', 'module' : getModule(request), 
													   'idpk' : d.id, 'dsb' : modules, 'parent' : getParent(request)})
	
@login_required()
def hariraya_save(request, hariraya_id):
	d = HariRaya.objects.select_for_update().filter(id=hariraya_id)
	d.update(name=request.POST['name'], tanggal = parse(request.POST['tanggal']).strftime("%Y-%m-%d"), sd = parse(request.POST['sd']).strftime("%Y-%m-%d"), desc=request.POST['desc'])
	return redirect("hariraya-index")

@login_required()
def tunjangan(request, tunjangan_id):
	d = TunjanganKaryawan.objects.get(pk=tunjangan_id)
	ms = MasaTenggangClosing.objects.all()
	return render(request, "tunjangan/form.html", { 'ms': ms, 'data' : d , 'mode' : 'Ubah', 'module' : getModule(request), 
													   'idpk' : d.id, 'dsb' : modules, 'parent' : getParent(request)})
	
@login_required()
def tunjangan_save(request, tunjangan_id):
	d = TunjanganKaryawan.objects.select_for_update().filter(id=tunjangan_id)
	d.update(masatenggangclosing_id = request.POST['masatenggang'], jabatan=request.POST['jabatan'], kemahalan = request.POST['kemahalan'])
	return redirect("tunjangankaryawan-index")

@login_required()
def potongan(request, potongan_id):
	d = PotonganKaryawan.objects.get(pk=potongan_id)
	ms = MasaTenggangClosing.objects.all()
	return render(request, "potongan/form.html", { 'ms': ms, 'data' : d , 'mode' : 'Ubah', 'module' : getModule(request), 
													   'idpk' : d.id, 'dsb' : modules, 'parent' : getParent(request)})
	
@login_required()
def potongan_save(request, potongan_id):
	d = PotonganKaryawan.objects.select_for_update().filter(id=potongan_id)
	d.update(masatenggangclosing_id = request.POST['masatenggang'], pinjkaryawan=request.POST['pinjaman'], cicil_pinjkaryawan = request.POST['cicil'])
	return redirect("potongankaryawan-index")

@login_required()
def karyawanshift(request, karyawanshift_id):
	d = KaryawanShift.objects.get(pk=karyawanshift_id)
	shift = Shift.objects.all()
	return render(request, "karyawanshift/form.html", { 'shift': shift, 'data' : d , 'mode' : 'Ubah', 'module' : getModule(request), 
													   'idpk' : d.id, 'dsb' : modules, 'parent' : getParent(request)})
	
@login_required()
def karyawanshift_save(request, karyawanshift_id):
	d = KaryawanShift.objects.select_for_update().filter(id=karyawanshift_id)
	tanggal = request.POST['tanggal']
	tglawal = parse([x.strip() for x in tanggal.split(' ')][0]).strftime("%Y-%m-%d")
	tglakhir = parse([x.strip() for x in tanggal.split(' ')][2]).strftime("%Y-%m-%d")
	d.update(tglawal = tglawal, shift_id=request.POST['shift'], tglakhir = tglakhir)
	return redirect("karyawan-shift-index")

@login_required()
def perusahaan_save(request, departemen_id):
	d = Perusahaan.objects.select_for_update().filter(id=perusahaan_id)
	d.update(name=request.POST['name'], desc=request.POST['desc'])
	return redirect("perusahaan-index")

@login_required()
def perusahaan(request, departemen_id):
	d = Perusahaan.objects.get(pk=perusahaan_id)
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
	return render(request, "shift/form.html", { 'data' : d, 'mode' : 'Ubah', 'module' : getModule(request), 
													   'idpk' : shift_id, 'dsb' : modules, 'parent' : getParent(request)})

@login_required()
def shift_save(request, shift_id):
	d = Shift.objects.select_for_update().filter(id=shift_id)
	d.update(name=request.POST['name'], jammasuk=request.POST['masuk'], jamkeluar=request.POST['keluar'], desc=request.POST['desc'])
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