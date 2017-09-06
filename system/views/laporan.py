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
from system.models import PostingGaji, MasaTenggangClosing
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from sys import getsizeof
from django.core import serializers
import json
from dateutil.parser import parse
import datetime
import xlwt
import re

modules = Modules.objects.all()
allmenu = Modules.objects.only('name')

@login_required()
def laporangaji(request):

	style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on',
    					 num_format_str='#,##0.00')
	style1 = xlwt.easyxf(num_format_str='D-MMM-YY')

	objs = [0]

	class postgaji(object):
			no = ""
			nik = ""
			nama = ""
			departemen = ""
			bagian = ""
			golongan = ""
			gajipokok = ""
			tmakan = ""
			transportnonexec = ""
			tovertime = ""
			pbpjs = ""
			ppinjam = ""
			pabsen = ""

			def __init__(self, no, nik, nama, departemen, bagian, golongan, gajipokok, tmakan, transportnonexec, tovertime, pbpjs, ppinjam, pabsen):
				self.no = no
				self.nik = nik
				self.nama = nama
				self.departemen = departemen
				self.bagian = bagian
				self.golongan = golongan
				self.gajipokok = gajipokok
				self.tmakan = tmakan
				self.transportnonexec = transportnonexec
				self.tovertime = tovertime
				self.pbpjs = pbpjs
				self.ppinjam = ppinjam
				self.pabsen = pabsen

	today = datetime.datetime.now()
	idkaryawan = request.POST['idkaryawan']
	masatenggangclosing = request.POST['masatenggangclosing']
	mas = MasaTenggangClosing.objects.get(pk=masatenggangclosing)
	if idkaryawan.find("&") != -1 :
		listid = [x.strip() for x in idkaryawan.split('&')]
		a= ""
		mantap = ""
	
		a = Karyawan.objects
		if listid[0] != "":
			a = a.filter(perusahaan=listid[0])

		if listid[1] != "":
			a = a.filter(departemen=listid[1])

		if listid[2] != "":
			a = a.filter(bagian=listid[2])

		if listid[3] != "":
			a = a.filter(golongan=listid[3])

		#a = a.filter(tanggal__year=today.year).filter(tanggal__month=4)

		y = 0

		objs = [range(len(a))]

		for b in a:
			y = y + 1
			#k = Karyawan.objects.get(pk=b.karyawan.id)
			g = GajiPokok.objects.get(karyawan_id=b.id)
			p = PotonganKaryawan.objects.get(karyawan_id=b.id)

			gajipokok = g.gajipokok 
			tunjanganmakan = g.tmakan
			makanlembur = g.makanlembur
			transportnonexec = g.transportnonexec
			cicil = 0
			tovertime = 0
			pabsen = 0

			if p.cicil_pinjkaryawan > 0 :
				cicil = (p.pinjkaryawan/p.cicil_pinjkaryawan)
				pe = PotonganKaryawan.objects.select_for_update().filter(id=p.id)
				pe.update(cicil_pinjkaryawan=p.cicil_pinjkaryawan-1)

			# for x in a:
			# 	mantap =  waktu(x.keluar, x.karyawanshift.shift.jamkeluar, True)

			ab = Absensi.objects.filter(karyawan_id=b.id).filter(tanggal__range = [mas.tanggal, mas.sd])

			for abi in ab:
				if abi.SPL == 1:
					tovertime = tovertime + (abi.SPL_banyak * 20000)

				if waktu(abi.masuk, abi.karyawanshift.shift.jammasuk, True) > 1:
					pabsen = pabsen + 1

			pabsen = pabsen * 10000

			objs.append(postgaji(y, b.NIK, b.name, b.departemen.name, b.bagian.name, b.golongan.name, g.gajipokok, tunjanganmakan, transportnonexec, tovertime, p.bpjs, cicil, pabsen))


	else:
		listid = [x.strip() for x in idkaryawan.split(',')]
		a = ""
		mantap = ""
		objs = [range(0, len(listid)-1)]

		for y in range(0, len(listid)-1):
			a = Absensi.objects.filter(karyawan=listid[y]).filter(tanggal__year=today.year).filter(tanggal__month=4)
			k = Karyawan.objects.get(pk=listid[y])
			g = GajiPokok.objects.get(karyawan_id=listid[y])
			p = PotonganKaryawan.objects.get(karyawan_id=listid[y])

			gajipokok = g.gajipokok 
			tunjanganmakan = g.tmakan
			makanlembur = g.makanlembur
			transportnonexec = g.transportnonexec

			cicil = 0
			tovertime = 0
			pabsen = 0

			if p.cicil_pinjkaryawan > 0 :
				cicil = (p.pinjkaryawan/p.cicil_pinjkaryawan)
				pe = PotonganKaryawan.objects.select_for_update().filter(id=p.id)
				pe.update(cicil_pinjkaryawan=p.cicil_pinjkaryawan-1)

			# for x in a:
			# 	mantap =  waktu(x.keluar, x.karyawanshift.shift.jamkeluar, True)

			ab = Absensi.objects.filter(karyawan_id=b.id).filter(tanggal__range[mas.tanggal, mas.sd])
			
			for abi in ab:
				if abi.SPL == 1:
					tovertime = tovertime + (abi.SPL_banyak * 20000)

				if waktu(abi.masuk, abi.karyawanshift.shift.jammasuk, True) > 1:
					pabsen = pabsen + 1

			pabsen = pabsen * 10000
			
			objs.append(postgaji(y+1, k.NIK, k.name, k.departemen.name, k.bagian.name, k.golongan.name, g.gajipokok, tunjanganmakan, transportnonexec,tovertime, p.bpjs, cicil, pabsen))
	
	wb = xlwt.Workbook()
	ws = wb.add_sheet('A Test Sheet')

	ws.write(0, 0, "No")
	ws.write(0, 1, "NIK")
	ws.write(0, 2, "Nama")
	ws.write(0, 3, "Departemen")
	ws.write(0, 4, "Bagian")
	ws.write(0, 5, "Golongan")
	ws.write(0, 6, "Gaji Pokok")
	ws.write(0, 7, "Tunjangan Makan")
	ws.write(0, 8, "Tunjangan Transportasi")
	ws.write(0, 9, "Tunjangan Overtime")
	ws.write(0, 10, "Potongan Pinjaman")
	ws.write(0, 11, "Potongan BPJS")
	ws.write(0, 12, "Potongan Absensi")

	x=1 

	ob = objs

	for x in range(1, len(objs)):
		ws.write(ob[x].no, 0, ob[x].no)
		ws.write(ob[x].no, 1, ob[x].nik)
		ws.write(ob[x].no, 2, ob[x].nama)
		ws.write(ob[x].no, 3, ob[x].departemen)
		ws.write(ob[x].no, 4, ob[x].bagian)
		ws.write(ob[x].no, 5, ob[x].golongan)
		ws.write(ob[x].no, 6, ob[x].gajipokok)
		ws.write(ob[x].no, 7, ob[x].tmakan)
		ws.write(ob[x].no, 8, ob[x].transportnonexec)
		ws.write(ob[x].no, 9, ob[x].tovertime)
		ws.write(ob[x].no, 10, ob[x].ppinjam)
		ws.write(ob[x].no, 11, ob[x].pbpjs)
		ws.write(ob[x].no, 12, ob[x].pabsen)

	wb.save("laporan/gaji/LAPORAN GAJI " + mas.name + ' ' + mas.tanggal.strftime("%d-%m-%Y") +' .s.d ' + mas.tanggal.strftime("%d-%m-%Y") +'-' + datetime.now().strftime("%d%m%Y-%H%M%S") + '.xls')

	return redirect("laporangaji-index")

def waktu(waktu=None, jadwal=None, masuk=None):
	hasil = 0
	akhir = 0

	wj, wm, wd = waktu.strftime("%H:%M:%S").split(':')
	waktu = (int(wj)*3600) + (int(wm)*60) + int(wd)

	jj, jm, jd = jadwal.strftime("%H:%M:%S").split(':')
	jadwal = (int(jj)*3600) + (int(jm)*60) + int(jd)

	nilai = waktu-jadwal

	return nilai