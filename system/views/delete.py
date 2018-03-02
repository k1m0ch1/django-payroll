from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.template import loader, Context
import django_tables2 as tables
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from system.models import Perusahaan, Departemen, Bagian, Golongan, Jabatan
from system.models import Bank, Agama, WargaNegara, StatusMenikah, Bonusthr
from system.models import LokasiPerusahaan, Shift, Inventory, Konfigurasi, Karyawan, MasaTenggangClosing, TunjanganKaryawan, PotonganKaryawan
from system.models import KaryawanShift, bpjs as BPJS, Mesin
from django.contrib import messages

@login_required()
def perusahaan(request, perusahaan_id):
	p = Perusahaan.objects.filter(id=perusahaan_id)
	p.delete()
	return redirect("perusahaan-index")

@login_required()
def bonusthr(request, bonusthr_id):
	b = Bonusthr.objects.filter(id=bonusthr_id)
	b.delete()
	return redirect("bonusthr-index")

@login_required()
def departemen(request, departemen_id):
	d = Departemen.objects.filter(id=departemen_id)
	d.delete()
	return redirect("departemen-index")

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

@login_required()
def statusmenikah(request, statusmenikah_id):
	if statusmenikah_id == 1 :
		messages.success(request, 'Data Default tidak boleh di hapus')
	else:
		messages.success(request, 'Data Berhasil di hapus')
		s = StatusMenikah.objects.filter(id=statusmenikah_id)
		s.delete()

	return redirect("statusmenikah-index")

@login_required()
def profile_perusahaan(request, lokasiperusahaan_id):
	s = LokasiPerusahaan.objects.filter(id=lokasiperusahaan_id)
	s.delete()
	return redirect("profile-perusahaan-index")

@login_required()
def hariraya(request, hariraya_id):
	s = HariRaya.objects.filter(id=hariraya_id)
	s.delete()
	return redirect("hariraya-index")

@login_required()
def shift(request, shift_id):
	s = Shift.objects.filter(id=shift_id)
	s.delete()
	return redirect("shift-index")

@login_required()
def inventory(request, inventory_id):
	s = Inventory.objects.filter(id=inventory_id)
	s.delete()
	return redirect("inventory-index")

@login_required()
def konfigurasi(request, konfigurasi_id):
	s = Konfigurasi.objects.filter(id=konfigurasi_id)
	s.delete()
	return redirect("konfigurasi-index")

@login_required()
def karyawan(request, karyawan_id):
	s = Karyawan.objects.filter(id=karyawan_id)
	s.delete()
	return redirect("karyawan-index")

@login_required()
def masatenggangclosing(request, masatenggangclosing_id):
	s = MasaTenggangClosing.objects.filter(id=masatenggangclosing_id)
	s.delete()
	return redirect("masatenggangclosing-index")

@login_required()
def tunjangan(request, tunjangan_id):
	s = TunjanganKaryawan.objects.filter(id=tunjangan_id)
	s.delete()
	return redirect("tunjangankaryawan-index")

@login_required()
def potongan(request, potongan_id):
	s = PotonganKaryawan.objects.filter(id=potongan_id)
	s.delete()
	return redirect("potongankaryawan-index")

@login_required()
def karyawanshift(request, karyawanshift_id):
	s = KaryawanShift.objects.filter(id=karyawanshift_id)
	s.delete()
	return redirect("karyawan-shift-index")

@login_required()
def bpjs(request, bpjs_id):
	s = PotonganKaryawan.objects.filter(id=bpjs_id)
	s.update(bpjs=0)
	return redirect("bpjs-index")

@login_required()
def mesin(request, mesin_id):
	s = Mesin.objects.filter(id=mesin_id)
	s.delete()
	return redirect("mesin-index")