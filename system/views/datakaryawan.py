from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.template import loader, Context
import django_tables2 as tables
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from system.models import Perusahaan, Departemen, Bagian, Golongan, Jabatan, Konfigurasi
from system.models import Bank, Agama, WargaNegara, StatusMenikah, Modules, Inventory, Absensi
from system.models import LokasiPerusahaan, Karyawan, HariRaya, KaryawanShift, Shift, GajiPokok, PotonganKaryawan
from system.models import PostingGaji, MasaTenggangClosing, IzinCuti, TunjanganKaryawan
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from sys import getsizeof
from django.core import serializers
import json
from dateutil.parser import parse
from datetime import datetime
import datetime
import xlwt
import re

modules = Modules.objects.all()
allmenu = Modules.objects.only('name')

@login_required()
def awal(request):

	idkaryawan = request.POST['idkaryawan']
	if idkaryawan.find("&") != -1 :
		listid = [x.strip() for x in idkaryawan.split('&')]
		a= ""
		mantap = ""
	
		a = Karyawan.objects
		if listid[0] != "":
			a = a.filter(perusahaan=listid[0])
			p = Perusahaan.objects.get(pk=listid[0])

		if listid[1] != "":
			a = a.filter(departemen=listid[1])

		if listid[2] != "":
			a = a.filter(bagian=listid[2])

		if listid[3] != "":
			a = a.filter(golongan=listid[3])

		#a = a.filter(tanggal__year=today.year).filter(tanggal__month=4)

		y = 0

		objs = [range(len(a))]

		objs.pop(0)
		wb = xlwt.Workbook()
		ws = wb.add_sheet('Data Karyawan',cell_overwrite_ok=True)

		ws.write(1, 6, "Data Karyawan")
		ws.write(2, 6, "Perusahaan : " + p.name)
		ws.write(4, 1, "No")
		ws.write(4, 2, "NIK")
		ws.write(4, 3, "Nama")
		ws.write(4, 4, "Departemen")
		ws.write(4, 5, "Golongan")
		ws.write(4, 6, "Bagian")
		ws.write(4, 7, "Jabatan")
		ws.write(4, 8, "NPWP")
		ws.write(4, 9, "Tanggal Masuk")
		ws.write(4, 10, "Masa Kerja")
		ws.write(4, 11, "Status Pajak")
		ws.write(4, 12, "Status Kary")
		ws.write(4, 13, "Tanggal Lahir")
		ws.write(4, 14, "Finger ID")
		ws.write(4, 15, "Sts Jamsostek")
		ws.write(4, 16, "Tanggal Keluar")
		ws.write(4, 17, "Alamat")
		ws.write(4, 18, "KPJ")
		ws.write(4, 19, "No Rekening Bank")
		ws.write(4, 20, "Agama")
		ws.write(4, 21, "Warga Negara")
		ws.write(4, 22, "Status Menikah")
		ws.write(4, 23, "Jenis Kelamin")
		ws.write(4, 24, "Basic Sallary")

		for b in a:
			y = y + 1
			k = Karyawan.objects.get(pk=b.id)
			g = GajiPokok.objects.get(karyawan_id=b.id)

			ws.write( y + 4, 1, y)
			ws.write( y + 4, 2, k.NIK)
			ws.write( y + 4, 3, k.name)
			ws.write( y + 4, 4, k.departemen.name)
			ws.write( y + 4, 5, k.golongan.name)
			ws.write( y + 4, 6, k.bagian.name)
			ws.write( y + 4, 7, "")
			ws.write( y + 4, 8, k.NPWP)
			ws.write( y + 4, 9, "" if k.tanggalmasuk == None else k.tanggalmasuk.strftime("%d-%m-%Y"))
			ws.write( y + 4, 10, "" if k.masakaryawan == None else k.masakaryawan.strftime("%d-%m-%Y"))
			ws.write( y + 4, 11, "")
			ws.write( y + 4, 12, "")
			ws.write( y + 4, 13, "" if k.tanggallahir == None else k.tanggallahir.strftime("%d-%m-%Y"))
			ws.write( y + 4, 14, k.fingerid)
			ws.write( y + 4, 15, "")
			ws.write( y + 4, 16, "")
			ws.write( y + 4, 17, k.alamat)
			ws.write( y + 4, 18, k.KPJ)
			ws.write( y + 4, 19, k.norek)
			ws.write( y + 4, 20, k.agama.name)
			ws.write( y + 4, 21, k.warganegara.name)
			ws.write( y + 4, 22, k.statusmenikah.name)
			ws.write( y + 4, 23, k.gender)
			ws.write( y + 4, 24, g.gajipokok)

		wb.save("laporan/datakaryawan/DATA KARYAWAN " + datetime.datetime.now().strftime("%d%m%Y-%H%M%S") + '.xls')

	return redirect("datakaryawan-index")





