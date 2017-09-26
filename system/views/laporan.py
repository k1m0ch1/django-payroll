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
def laporangaji(request):

	style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on',
    					 num_format_str='#,##0.00')
	style1 = xlwt.easyxf(num_format_str='D-MMM-YY')

	objs = [0]

	class postgaji(object):
			no = 0
			nik = 0
			nama = ""
			departemen = 0
			bagian = 0
			golongan = ""
			norek = 0
			gajipokok = 0
			statusmenikah = ""
			tmakan = 0
			transportnonexec = 0
			tovertime = 0
			tunjangan = 0
			pbpjs = 0
			ppinjam = 0
			pkoperasi = 0
			pcicil = 0
			pabsen = 0
			pph = 0

			def __init__(self, no, nik, nama, departemen, bagian, 
								golongan, norek, gajipokok, statusmenikah, tmakan, 
								transportnonexec, tovertime, tunjangan, pbpjs, 
								ppinjam, pkoperasi, pabsen, pph):
				self.no = no
				self.nik = nik
				self.nama = nama
				self.departemen = departemen
				self.bagian = bagian
				self.golongan = golongan
				self.norek = norek
				self.gajipokok = gajipokok
				self.statusmenikah = statusmenikah
				self.tmakan = tmakan
				self.transportnonexec = transportnonexec
				self.tovertime = tovertime
				self.tunjangan = tunjangan
				self.pbpjs = pbpjs
				self.ppinjam = ppinjam
				self.pkoperasi = pkoperasi
				self.pabsen = pabsen
				self.pph = pph

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
			tt = TunjanganKaryawan.objects.get(karyawan_id=b.id)

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

			wp = 0

			gapok = g.gajipokok
			status = b.statusmenikah.name
			tunjangan = tt.jabatan
			pph = 0
			bpjs = p.bpjs

			if gapok <= 50000000 :
			  wp = float(float(5)/100) 
			elif gapok > 50000000 or gapok <= 250000000 :
			  wp = float(float(15)/100) 
			elif gapok > 250000000 or gapok <= 500000000 :
			  wp = float(float(25)/100)
			elif gapok > 500000000 :
			  wp = float(float(30)/100)

			ptkp = 0

			if status == "Lajang Tanpa Tanggungan" :
			  ptkp = 54000000
			elif status == "Lajang 1 Tanggungan" or status == "Menikah Tanpa Tanggungan" :
			  ptkp = 58500000
			elif status ==  "Lajang 2 Tanggungan" or status == "Menikah 1 Tanggungan" :
			  ptkp = 63000000
			elif status == "Menikah 2 Tanggungan" :
			  ptkp = 67500000
			elif status == "Menikah 3 Tanggungan" :
			  ptkp = 72000000

			bpjs_ktg_per_jkk = int(float(float(0.54)/100) * int( bpjs)) # BPJS Ketenagakerjaan Perusahaan Kecelakaan Kerja 0.54% 
			bpjs_ktg_per_jkm = int(float(float(0.3)/100) * int( bpjs)) # BPJS Ketenagakerjaan Perusaaan Jaminan Kematian 0.3%
			bpjs_kes_per = int(float(float(4)/100) * int(bpjs)) # BPJS Kesehatan Perusahaan 4%
			bruto = gapok + tunjangan + bpjs_ktg_per_jkk + bpjs_ktg_per_jkm + bpjs_kes_per

			bpjs_ktg_kar_jht = int(float(float(2)/100) * int( bpjs)) # BPJS Ketenagakerjaan Karyawan Jaminan Hari Tua 2%
			bpjs_ktg_per_jpn = int(float(float(2)/100) * int( bpjs)) # BPJS Ketenagakerjaan Perusahaan Jaminan Kematian 2%

			ph_netto_sebulan = bruto - ( (int(float(float(5)/100) * int(bruto))) + bpjs_ktg_kar_jht + bpjs_ktg_per_jpn )

			ph_netto_setahun = ph_netto_sebulan * 12

			ph_kena_pajak = ph_netto_setahun - ptkp

			pph_terhutang = int(wp * int(ph_kena_pajak))

			pph = pph_terhutang / 12
			pph = 0 if pph < 0 else pph

			if b.NPWP == 0 or b.NPWP == None :
				pph = int(float(float(120)/100) * int(pph))
			
			objs.append(postgaji(y, b.NIK, b.name, b.departemen.name, b.bagian.name, 
									b.golongan.name, b.norek + " a.n." + b.atasnama + " " + b.bank.name , 
									g.gajipokok, b.statusmenikah.name, tunjanganmakan, transportnonexec, tovertime, 
									tt.jabatan, p.bpjs, cicil, p.koperasi, pabsen, pph))

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
			tt = TunjanganKaryawan.objects.get(karyawan_id=listid[y])

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
			
			gapok = g.gajipokok
			status = k.statusmenikah.name
			tunjangan = tt.jabatan
			pph = 0
			bpjs = p.bpjs

			if gapok <= 50000000 :
			  wp = float(float(5)/100) 
			elif gapok > 50000000 or gapok <= 250000000 :
			  wp = float(float(15)/100) 
			elif gapok > 250000000 or gapok <= 500000000 :
			  wp = float(float(25)/100)
			elif gapok > 500000000 :
			  wp = float(float(30)/100)

			ptkp = 0

			if status == "Lajang Tanpa Tanggungan" :
			  ptkp = 54000000
			elif status == "Lajang 1 Tanggungan" or status == "Menikah Tanpa Tanggungan" :
			  ptkp = 58500000
			elif status ==  "Lajang 2 Tanggungan" or status == "Menikah 1 Tanggungan" :
			  ptkp = 63000000
			elif status == "Menikah 2 Tanggungan" :
			  ptkp = 67500000
			elif status == "Menikah 3 Tanggungan" :
			  ptkp = 72000000

			bpjs_ktg_per_jkk = int(float(float(0.54)/100) * int(bpjs)) # BPJS Ketenagakerjaan Perusahaan Kecelakaan Kerja 0.54% 
			bpjs_ktg_per_jkm = int(float(float(0.3)/100) * int(bpjs)) # BPJS Ketenagakerjaan Perusaaan Jaminan Kematian 0.3%
			bpjs_kes_per = int(float(float(4)/100) * int(bpjs)) # BPJS Kesehatan Perusahaan 4%

			bruto = gapok + tunjangan + bpjs_ktg_per_jkk + bpjs_ktg_per_jkm + bpjs_kes_per

			bpjs_ktg_kar_jht = int(float(float(2)/100) * int(bpjs)) # BPJS Ketenagakerjaan Karyawan Jaminan Hari Tua 2%
			bpjs_ktg_per_jpn = int(float(float(2)/100) * int(bpjs)) # BPJS Ketenagakerjaan Perusahaan Jaminan Kematian 2%

			ph_netto_sebulan = bruto - ( (int(float(float(5)/100) * int(bruto))) + bpjs_ktg_kar_jht + bpjs_ktg_per_jpn )

			ph_netto_setahun = ph_netto_sebulan * 12

			ph_kena_pajak = ph_netto_setahun - ptkp

			pph_terhutang = int(wp * int(ph_kena_pajak))

			pph = pph_terhutang / 12
			pph = 0 if pph < 0 else pph

			if k.NPWP == 0 or k.NPWP == None :
				pph = int(float(float(120)/100) * int(pph))
			
			objs.append(postgaji(y+1, k.NIK, k.name, k.departemen.name, k.bagian.name, 
									k.golongan.name, k.norek + " a.n." + k.atasnama + " " + k.bank.name ,
									g.gajipokok, k.statusmenikah.name, tunjanganmakan, transportnonexec,tovertime, 
									tt.jabatan, p.bpjs, cicil, p.koperasi, pabsen, pph))
	wb = xlwt.Workbook()
	ws = wb.add_sheet('Laporan Gaji',cell_overwrite_ok=True)

	ws.write(1, 6, "Laporan Gaji")
	ws.write(2, 6, "Masa Tenggang Closing " + mas.name)
	ws.write(4, 1, "No")
	ws.write(4, 2, "NIK")
	ws.write(4, 3, "Nama")
	ws.write(4, 4, "Departemen")
	ws.write(4, 5, "Bagian")
	ws.write(4, 6, "Golongan")
	ws.write(4, 7, "Gaji Pokok")
	ws.write(4, 8, "Tunjangan Makan")
	ws.write(4, 9, "Tunjangan Transportasi")
	ws.write(4, 10, "Tunjangan Overtime")
	ws.write(4, 11, "Potongan Pinjaman")
	ws.write(4, 12, "Potongan Koperasi")
	ws.write(4, 13, "BPJS")
	ws.write(4, 14, "PPh 21")
	ws.write(4, 15, "Potongan BPJS Kesehatan")
	ws.write(4, 16, "Potongan BPJS Kesehatan")
	ws.write(4, 17, "Total Potongan BPJS")
	ws.write(4, 18, "Potongan Absensi")

	y=4

	ob = objs

	for x in range(1, len(objs)):
		ws.write(ob[x].no+y, 1, ob[x].no)
		ws.write(ob[x].no+y, 2, ob[x].nik)
		ws.write(ob[x].no+y, 3, ob[x].nama)
		ws.write(ob[x].no+y, 4, ob[x].departemen)
		ws.write(ob[x].no+y, 5, ob[x].bagian)
		ws.write(ob[x].no+y, 6, ob[x].golongan)
		ws.write(ob[x].no+y, 7, ob[x].gajipokok)
		ws.write(ob[x].no+y, 8, ob[x].tmakan)
		ws.write(ob[x].no+y, 9, ob[x].transportnonexec)
		ws.write(ob[x].no+y, 10, ob[x].tovertime)
		ws.write(ob[x].no+y, 11, ob[x].ppinjam)
		ws.write(ob[x].no+y, 12, ob[x].pkoperasi)

		bpjs_kes_kar = int(float(float(1)/100) * int(ob[x].pbpjs)) # BPJS Kesehatan Karyawan 1%
		bpjs_kes_per = int(float(float(4)/100) * int(ob[x].pbpjs)) # BPJS Kesehatan Perusahaan 4%
		bpjs_ktg_kar_jpn = int(float(float(1)/100) * int(ob[x].pbpjs)) # BPJS Ketenagakerjaan Karyawan Jaminan Pensiunan 1%
		bpjs_ktg_kar_jht = int(float(float(2)/100) * int(ob[x].pbpjs)) # BPJS Ketenagakerjaan Karyawan Jaminan Hari Tua 2%
		bpjs_ktg_per_jpn = int(float(float(2)/100) * int(ob[x].pbpjs)) # BPJS Ketenagakerjaan Perusahaan Jaminan Kematian 2%
		bpjs_ktg_per_jkk = int(float(float(0.54)/100) * int(ob[x].pbpjs)) # BPJS Ketenagakerjaan Perusahaan Kecelakaan Kerja 0.54% 
		bpjs_ktg_per_jht = int(float(float(3.7)/100) * int(ob[x].pbpjs)) # BPJS Ketenagakerjaan Perusahaan Jaminan Hari Tua 3.7%
		bpjs_ktg_per_jkn = int(float(float(0.3)/100) * int(ob[x].pbpjs)) # BPJS Ketenagakerjaan Perusaaan Jaminan Kematian 0.3%
		bpjs_kes = bpjs_kes_kar + bpjs_kes_per
		bpjs_ktg = bpjs_ktg_kar_jpn + bpjs_ktg_kar_jht + bpjs_ktg_per_jpn + bpjs_ktg_per_jkk + bpjs_ktg_per_jht
		bpjs_total = bpjs_kes + bpjs_ktg

		ws.write(ob[x].no+y, 13, ob[x].pbpjs)
		ws.write(ob[x].no+y, 14, ob[x].pph)
		ws.write(ob[x].no+y, 15, bpjs_kes)
		ws.write(ob[x].no+y, 16, bpjs_ktg)
		ws.write(ob[x].no+y, 17, bpjs_total)
		ws.write(ob[x].no+y, 18, ob[x].pabsen)

	wb.save("laporan/gaji/LAPORAN GAJI " + mas.name + ' ' + mas.tanggal.strftime("%d-%m-%Y") +' .s.d ' + mas.tanggal.strftime("%d-%m-%Y") +'-' + datetime.datetime.now().strftime("%d%m%Y-%H%M%S") + '.xls')

	return redirect("laporangaji-index")

@login_required()
def laporanabsensi(request):

	style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on',
    					 num_format_str='#,##0.00')
	style1 = xlwt.easyxf(num_format_str='D-MMM-YY')

	objs = [0]

	class postabsensi(object):
			no = ""
			nik = ""
			nama = ""
			departemen = ""
			bagian = ""
			golongan = ""
			masuk = ""
			telat = ""
			overtime = ""
			izin = ""
			cuti = ""
			dinas = ""
			sakit = ""

			def __init__(self, no, nik, nama, departemen, bagian, golongan, masuk, telat, overtime, izin, cuti, dinas, sakit):
				self.no = no
				self.nik = nik
				self.nama = nama
				self.departemen = departemen
				self.bagian = bagian
				self.golongan = golongan
				self.masuk = masuk
				self.telat = telat
				self.overtime = overtime
				self.izin = izin
				self.cuti = cuti
				self.dinas = dinas
				self.sakit = sakit

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
			telat = 0
			overtime = 0
			izin = 0
			cuti = 0
			dinas = 0
			sakit = 0 
			#k = Karyawan.objects.get(pk=b.karyawan.id)

			# for x in a:
			# 	mantap =  waktu(x.keluar, x.karyawanshift.shift.jamkeluar, True)

			ab = Absensi.objects.filter(karyawan_id=b.id).filter(tanggal__range = [mas.tanggal, mas.sd])

			for abi in ab:
				if waktu(abi.masuk, abi.karyawanshift.shift.jammasuk, True) > 1 and abi.koreksi == 0:
					telat = telat + 1

				if abi.SPL == 1:
					overtime = overtime + 1

			ic = IzinCuti.objects.filter(karyawan_id=b.id).filter(tglmulai__range = [mas.tanggal, mas.sd])
			for ici in ic:
				izin = izin + 1 if ici.jenis == "IZIN" else izin
				cuti = cuti + 1 if ici.jenis == "CUTI" else cuti
				dinas = dinas + 1 if ici.jenis == "DINAS" else dinas
				sakit = sakit + 1 if ici.jenis == "SAKIT" else sakit

			objs.append(postabsensi(y, b.NIK, b.name, b.departemen.name, b.bagian.name, b.golongan.name, len(ab), telat, overtime, izin, cuti, dinas, sakit))


	else:
		listid = [x.strip() for x in idkaryawan.split(',')]
		a = ""
		mantap = ""
		objs = [range(0, len(listid)-1)]

		for y in range(0, len(listid)-1):
			izin = 0
			cuti = 0
			dinas = 0
			sakit = 0 
			a = Absensi.objects.filter(karyawan=listid[y]).filter(tanggal__year=today.year).filter(tanggal__month=4)
			k = Karyawan.objects.get(pk=listid[y])

			ab = Absensi.objects.filter(karyawan_id=b.id).filter(tanggal__range = [mas.tanggal, mas.sd])

			for abi in ab:
				if waktu(abi.masuk, abi.karyawanshift.shift.jammasuk, True) > 1 and abi.koreksi == 0:
					telat = telat + 1

				if abi.SPL == 1:
					overtime = overtime + 1

			ic = IzinCuti.objects.filter(karyawan_id=b.id).filter(tglmulai__range = [mas.tanggal, mas.sd])
			for ici in ic:
				izin = izin + 1 if ici.jenis == "IZIN" else izin
				cuti = cuti + 1 if ici.jenis == "CUTI" else cuti
				dinas = dinas + 1 if ici.jenis == "DINAS" else dinas
				sakit = sakit + 1 if ici.jenis == "SAKIT" else sakit

			objs.append(postabsensi(y, b.NIK, b.name, b.departemen.name, b.bagian.name, b.golongan.name, len(ab), telat, overtime, izin, cuti, dinas, sakit))
	
	wb = xlwt.Workbook()
	ws = wb.add_sheet('Laporan Absensi' ,cell_overwrite_ok=True )

	ws.write(1, 6, "Laporan Absensi")
	ws.write(2, 6, "Masa Tenggang Closing " + mas.name)
	ws.write(4, 1, "No")
	ws.write(4, 2, "NIK")
	ws.write(4, 3, "Nama")
	ws.write(4, 4, "Departemen")
	ws.write(4, 5, "Bagian")
	ws.write(4, 6, "Golongan")
	ws.write(4, 7, "Jumlah Masuk")
	ws.write(4, 8, "Jumlah Telat")
	ws.write(4, 9, "Jumlah Overtime")
	ws.write(4, 10, "Jumlah Izin")
	ws.write(4, 11, "Jumlah Cuti")
	ws.write(4, 12, "Jumlah Dinas")
	ws.write(4, 13, "Jumlah Sakit")

	y=4

	ob = objs

	for x in range(1, len(objs)):
		ws.write(ob[x].no+y, 1, ob[x].no)
		ws.write(ob[x].no+y, 2, ob[x].nik)
		ws.write(ob[x].no+y, 3, ob[x].nama)
		ws.write(ob[x].no+y, 4, ob[x].departemen)
		ws.write(ob[x].no+y, 5, ob[x].bagian)
		ws.write(ob[x].no+y, 6, ob[x].golongan)
		ws.write(ob[x].no+y, 7, ob[x].masuk)
		ws.write(ob[x].no+y, 8, ob[x].telat)
		ws.write(ob[x].no+y, 9, ob[x].overtime)
		ws.write(ob[x].no+y, 10, ob[x].izin)
		ws.write(ob[x].no+y, 11, ob[x].cuti)
		ws.write(ob[x].no+y, 12, ob[x].dinas)
		ws.write(ob[x].no+y, 13, ob[x].sakit)

	wb.save("laporan/absensi/LAPORAN ABSENSI " + mas.name + ' ' + mas.tanggal.strftime("%d-%m-%Y") +' .s.d ' + mas.tanggal.strftime("%d-%m-%Y") +'-' + datetime.datetime.now().strftime("%d%m%Y-%H%M%S") + '.xls')

	return HttpResponse("Success")

def waktu(waktu=None, jadwal=None, masuk=None):
	hasil = 0
	akhir = 0

	wj, wm, wd = waktu.strftime("%H:%M:%S").split(':')
	waktu = (int(wj)*3600) + (int(wm)*60) + int(wd)

	jj, jm, jd = jadwal.strftime("%H:%M:%S").split(':')
	jadwal = (int(jj)*3600) + (int(jm)*60) + int(jd)

	nilai = waktu-jadwal

	return nilai