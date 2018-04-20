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
from system.models import PostingGaji, MasaTenggangClosing, IzinCuti, TunjanganKaryawan, Pinjaman
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


def mon(money=None):
	i = 0
	hasil = "Rp. "
	y = len(str(money))
	for x in str(money):
		if y%3 == 0 and y != 1 and y != len(str(money)):
			hasil = hasil + "."
		hasil = hasil + x
		y = y - 1
	return hasil

@login_required()
def laporanbpjs(request):

	style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on',
    					 num_format_str='#,##0.00')
	style1 = xlwt.easyxf(num_format_str='D-MMM-YY')

	objs = [0]

	class bpjs(object):
			no = 0
			kpj = 0
			nik = ""
			nama = ""
			sex = ""
			kpjkk = 0
			kpjht = 0
			kpjkm = 0
			kpjp = 0
			totala = 0
			kpkes = 0
			totalb = 0
			kkjht = 0
			kkjp = 0
			totalc = 0	
			kkkes = 0 
			totald = 0		

			def __init__(self, no, kpj, nik, nama, sex, kpjkk, kpjht, kpjkm, kpjp, totala,
						 kpkes, totalb, kkjht, kkjp, totalc, kkkes, totald):
				self.no = no
				self.kpj = kpj
				self.nik = nik
				self.nama = nama
				self.sex = sex
				self.kpjkk = kpjkk
				self.kpjht = kpjht
				self.kpjkm = kpjkm
				self.kpjp = kpjp
				self.totala = totala
				self.kpkes = kpkes
				self.totalb = totalb
				self.kkjht = kkjht
				self.kkjp = kkjp
				self.totalc = totalc
				self.kkkes = kkkes
				self.totald = totald
				

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
			k = Karyawan.objects.get(pk=b.id)
			g = GajiPokok.objects.get(karyawan_id=b.id)
			p = PotonganKaryawan.objects.get(karyawan_id=b.id)
			tt = TunjanganKaryawan.objects.get(karyawan_id=b.id)

			gajipokok = g.gajipokok 
			tunjanganmakan = tt.tmakan
			makanlembur = g.makanlembur
			transportnonexec = tt.transportnonexec
			cicil = 0
			tovertime = 0
			pabsen = 0

			if p.cicil_pinjkaryawan > 0 :
				cicil = (p.pinjkaryawan/p.cicil_pinjkaryawan)
				pe = PotonganKaryawan.objects.select_for_update().filter(id=p.id)
				pe.update(cicil_pinjkaryawan=p.sisa_cicil_pinjkaryawan-1)

			if p.cicil_koperasi > 0 :
				cicil = (p.koperasi/p.cicil_koperasi)
				pe = PotonganKaryawan.objects.select_for_update().filter(id=p.id)
				pe.update(cicil_koperasi=p.sisa_cicil_koperasi-1)

			# for x in a:
			# 	mantap =  waktu(x.keluar, x.karyawanshift.shift.jamkeluar, True)

			ab = Absensi.objects.filter(karyawan_id=b.id).filter(tanggal__range = [mas.tanggal, mas.sd])

			date_format = "%Y-%m-%d"
			hari = mas.sd - mas.tanggal
			hari = hari.days

			banyak = len(ab)

			if k.jumlahhari == 5 :
				hari = 21
				bjam = 8
			elif k.jumlahhari == 6 :
				hari = 25
				bjam = 7	

			for abi in ab:
				if abi.SPL == 1:
					hari = abi.created_at.strftime("%A")
					FMT = '%H:%M:%S'
					penjumlahan = datetime.datetime.strptime(abi.keluar.strftime("%H:%M:%S"), FMT) - datetime.datetime.strptime(abi.masuk.strftime("%H:%M:%S"), FMT)
					penjumlahan = (penjumlahan.seconds / 3600)
					istirahat = ( penjumlahan / 5 )
					banyakwaktu = penjumlahan - bjam - istirahat
					if hari == "Minggu" or hari == "Sunday" :
						hitungot = abi.SPL_banyak
						if abi.karyawan.golongan.id == 7 or abi.karyawan.golongan.id == 8 :
							if banyakwaktu <= 7 :
								tovertime = tovertime + int(float((banyakwaktu * 2) * 10000))
							elif banyakwaktu > 7 :
								tovertime = tovertime + int(float((7 * 2) * 10000))
								tovertime = tovertime + ( ( ( banyakwaktu - 7 ) * 3 ) * 10000 )
						elif abi.karyawan.golongan.id < 7 :
							if banyakwaktu <= 7 :
								tovertime = tovertime + int(float((banyakwaktu * 2) * 20000))
							elif banyakwaktu > 7 :
								tovertime = tovertime + int(float((7 * 2) * 10000))
								tovertime = tovertime + ( ( ( banyakwaktu - 7 ) * 3 ) * 20000 )
					else:
						if abi.karyawan.golongan.id == 7 or abi.karyawan.golongan.id == 8 :
							if banyakwaktu <= 1 :
								tovertime = tovertime + int(float(1.5 * 10000))
							elif banyakwaktu > 1 :
								tovertime = tovertime + int(float(1.5 * 10000))
								tovertime = tovertime + ( ( ( banyakwaktu - 1 ) * 2 ) * 10000 )
						elif abi.karyawan.golongan.id < 7 :
							if banyakwaktu >= 1 :
								tovertime = tovertime + int(float(1.5 * 20000))
							elif banyakwaktu > 1 :
								tovertime = tovertime + int(float(1.5 * 20000))
								tovertime = tovertime + ( ( ( banyakwaktu - 1 ) * 2 ) * 20000 )

				if waktu(abi.masuk, abi.karyawanshift.shift.jammasuk, True) > 300:
					pabsen = pabsen + 1

			if k.jumlahhari == 5 :
				hari = 21
			elif k.jumlahhari == 6 :
				hari = 25

			# hari = mas.sd - mas.tanggal
			# hari = hari.days

			if k.golongan.id == 7 or k.golongan.id == 8 :
				pabsen = pabsen * 20000
				tunjanganmakan = int( 20000 * hari )
				transportnonexec = int( 20000 * hari )			
			elif k.golongan.id == 6 or k.golongan.id == 5 :
				pabsen = pabsen * 40000
				tunjanganmakan = int( 40000 * hari ) * banyak
				transportnonexec = int( 40000 * hari )			
			elif k.golongan_id < 5:
				pabsen = pabsen * 60000
				tunjanganmakan = int( 60000 * hari )
				transportnonexec = int( 60000 * hari )

			UMUT = 	(tunjanganmakan + transportnonexec)	
			pabsen = UMUT - pabsen

			wp = 0

			gapok = g.gajipokok
			ga_pok = gapok + UMUT + g.jabatan
			gatu = ga_pok - UMUT
			ga_pokii = gatu * (75/100)
			tunjangan_ii = gatu * (25/100)

			if k.golongan.id == 7 or k.golongan.id == 8 :
				mangkir = (gatu / hari) + 20000	
				mangkir = (hari - banyak) * mangkir
			elif k.golongan.id == 6 or k.golongan.id == 5 :
				mangkir = (gatu / hari) + 40000		
				mangkir = (hari - banyak) * mangkir
			elif k.golongan_id < 5:
				mangkir = (gatu / hari) + 60000
				mangkir = (hari - banyak) * mangkir

			ga_pok = ga_pok - mangkir

			status = b.statusmenikah.desc
			tunjangan = g.jabatan + tt.kemahalan + UMUT
			pph = 0
			bpjs_ks = p.bpjs_ks
			bpjs_kt = p.bpjs_kt

			if ga_pok <= 50000000 :
			  wp = float(float(5)/100) 
			elif ga_pok > 50000000 or ga_pok <= 250000000 :
			  wp = float(float(15)/100) 
			elif ga_pok > 250000000 or ga_pok <= 500000000 :
			  wp = float(float(25)/100)
			elif ga_pok > 500000000 :
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

			bpjs_ktg_per_jkk = int(float(float(0.54)/100) * int( bpjs_kt)) # BPJS Ketenagakerjaan Perusahaan Kecelakaan Kerja 0.54% 
			bpjs_ktg_per_jkm = int(float(float(0.3)/100) * int( bpjs_kt)) # BPJS Ketenagakerjaan Perusaaan Jaminan Kematian 0.3%
			bpjs_kes_per = int(float(float(4)/100) * int(bpjs_ks)) # BPJS Kesehatan Perusahaan 4%
			bruto = ga_pok + tunjangan + bpjs_ktg_per_jkk + bpjs_ktg_per_jkm + bpjs_kes_per

			bpjs_ktg_kar_jht = int(float(float(2)/100) * int( bpjs_kt)) # BPJS Ketenagakerjaan Karyawan Jaminan Hari Tua 2%	
			bpjs_ktg_per_jpn = int(float(float(2)/100) * int( bpjs_kt)) # BPJS Ketenagakerjaan Perusahaan Jaminan Kematian 2%

			kpjkk = bpjs_ktg_per_jkk
			kpjht = int(float(float(3.70)/100) * int( bpjs_kt))
			kpjkm = bpjs_ktg_per_jkm
			kpjp = int(float(float(2)/100) * int( bpjs_kt))
			totala = kpjkk + kpjht + kpjkm + kpjp
			kpkes = bpjs_kes_per
			totalb = totala + kpkes
			kkjht = int(float(float(2)/100) * int( bpjs_kt))
			kkjp = int(float(float(1)/100) * int( bpjs_kt))
			totalc = kkjht + kkjp
			kkkes = int(float(float(1)/100) * int( bpjs_ks))
			totald = totalc + kkkes

			ph_netto_sebulan = bruto - ( (int(float(float(5)/100) * int(bruto))) + bpjs_ktg_kar_jht + bpjs_ktg_per_jpn )

			ph_netto_setahun = ph_netto_sebulan * 12

			ph_kena_pajak = ph_netto_setahun - ptkp

			pph_terhutang = int(wp * int(ph_kena_pajak))

			pph = pph_terhutang / 12
			pph = 0 if pph < 0 else pph

			if b.NPWP == 0 or b.NPWP == None :
				pph = int(float(float(120)/100) * int(pph))
			
			objs.append(bpjs(y, k.KPJ, k.NIK, k.name, 
									k.gender, kpjkk, kpjht, kpjkm, kpjp, 
									totala, kpkes, totalb, kkjht, kkjp, totalc, kkkes, totald))

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
			tunjanganmakan = tt.tmakan
			makanlembur = g.makanlembur
			transportnonexec = tt.transportnonexec

			cicil = 0
			tovertime = 0
			pabsen = 0

			if p.cicil_pinjkaryawan > 0 :
				cicil = (p.pinjkaryawan/p.cicil_pinjkaryawan)
				pe = PotonganKaryawan.objects.select_for_update().filter(id=p.id)
				pe.update(cicil_pinjkaryawan=p.sisa_cicil_pinjkaryawan-1)

			if p.cicil_koperasi > 0 :
				cicil = (p.koperasi/p.cicil_koperasi)
				pe = PotonganKaryawan.objects.select_for_update().filter(id=p.id)
				pe.update(cicil_koperasi=p.sisa_cicil_koperasi-1)

			# for x in a:
			# 	mantap =  waktu(x.keluar, x.karyawanshift.shift.jamkeluar, True)

			ab = Absensi.objects.filter(karyawan_id=b.id).filter(tanggal__range = [mas.tanggal, mas.sd])

			date_format = "%Y-%m-%d"
			hari = mas.sd - mas.tanggal
			hari = hari.days

			banyak = len(ab)

			if k.jumlahhari == 5 :
				hari = 21
				bjam = 8
			elif k.jumlahhari == 6 :
				hari = 25
				bjam = 7	
			
			for abi in ab:
				if abi.SPL == 1:
					hari = abi.created_at.strftime("%A")
					FMT = '%H:%M:%S'
					penjumlahan = datetime.datetime.strptime(abi.keluar.strftime("%H:%M:%S"), FMT) - datetime.datetime.strptime(abi.masuk.strftime("%H:%M:%S"), FMT)
					penjumlahan = (penjumlahan.seconds / 3600)
					istirahat = ( penjumlahan / 5 )
					banyakwaktu = penjumlahan - bjam - istirahat
					if hari == "Minggu" or hari == "Sunday" :
						hitungot = abi.SPL_banyak
						if abi.karyawan.golongan.id == 7 or abi.karyawan.golongan.id == 8 :
							if banyakwaktu <= 7 :
								tovertime = tovertime + int(float((banyakwaktu * 2) * 10000))
							elif banyakwaktu > 7 :
								tovertime = tovertime + int(float((7 * 2) * 10000))
								tovertime = tovertime + ( ( ( banyakwaktu - 7 ) * 3 ) * 10000 )
						elif abi.karyawan.golongan.id < 7 :
							if banyakwaktu <= 7 :
								tovertime = tovertime + int(float((banyakwaktu * 2) * 20000))
							elif banyakwaktu > 7 :
								tovertime = tovertime + int(float((7 * 2) * 10000))
								tovertime = tovertime + ( ( ( banyakwaktu - 7 ) * 3 ) * 20000 )
					else:
						if abi.karyawan.golongan.id == 7 or abi.karyawan.golongan.id == 8 :
							if banyakwaktu <= 1 :
								tovertime = tovertime + int(float(1.5 * 10000))
							elif banyakwaktu > 1 :
								tovertime = tovertime + int(float(1.5 * 10000))
								tovertime = tovertime + ( ( ( banyakwaktu - 1 ) * 2 ) * 10000 )
						elif abi.karyawan.golongan.id < 7 :
							if banyakwaktu >= 1 :
								tovertime = tovertime + int(float(1.5 * 20000))
							elif banyakwaktu > 1 :
								tovertime = tovertime + int(float(1.5 * 20000))
								tovertime = tovertime + ( ( ( banyakwaktu - 1 ) * 2 ) * 20000 )

				if waktu(abi.masuk, abi.karyawanshift.shift.jammasuk, True) > 300:
					pabsen = pabsen + 1

			if k.jumlahhari == 5 :
				hari = 21
			elif k.jumlahhari == 6 :
				hari = 25

			if k.golongan.id == 7 or k.golongan.id == 8 :
				pabsen = pabsen * 20000
				tunjanganmakan = int( 20000 * hari )
				transportnonexec = int( 20000 * hari )			
			elif k.golongan.id == 6 or k.golongan.id == 5 :
				pabsen = pabsen * 40000
				tunjanganmakan = int( 40000 * hari ) * banyak
				transportnonexec = int( 40000 * hari )			
			elif k.golongan_id < 5:
				pabsen = pabsen * 60000
				tunjanganmakan = int( 60000 * hari )
				transportnonexec = int( 60000 * hari )

			UMUT = 	(tunjanganmakan + transportnonexec)	
			pabsen = UMUT - pabsen

			if k.golongan.id == 7 or k.golongan.id == 8 :
				mangkir = (gatu / hari) + 20000	
				mangkir = (hari - banyak) * mangkir
			elif k.golongan.id == 6 or k.golongan.id == 5 :
				mangkir = (gatu / hari) + 40000		
				mangkir = (hari - banyak) * mangkir
			elif k.golongan_id < 5:
				mangkir = (gatu / hari) + 60000
				mangkir = (hari - banyak) * mangkir

			ga_pok = ga_pok - mangkir
			
			gapok = g.gajipokok
			ga_pok = gapok + UMUT + g.jabatan
			gatu = ga_pok - UMUT
			ga_pokii = gatu * (75/100)
			tunjangan_ii = gatu * (25/100)

			status = k.statusmenikah.desc
			tunjangan = g.jabatan + tt.kemahalan + UMUT
			pph = 0
			bpjs_ks = p.bpjs_ks
			bpjs_kt = p.bpjs_kt

			if ga_pok <= 50000000 :
			  wp = float(float(5)/100) 
			elif ga_pok > 50000000 or ga_pok <= 250000000 :
			  wp = float(float(15)/100) 
			elif ga_pok > 250000000 or ga_pok <= 500000000 :
			  wp = float(float(25)/100)
			elif ga_pok > 500000000 :
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

			bpjs_ktg_per_jkk = int(float(float(0.54)/100) * int( bpjs_kt)) # BPJS Ketenagakerjaan Perusahaan Kecelakaan Kerja 0.54% 
			bpjs_ktg_per_jkm = int(float(float(0.3)/100) * int( bpjs_kt)) # BPJS Ketenagakerjaan Perusaaan Jaminan Kematian 0.3%
			bpjs_kes_per = int(float(float(4)/100) * int(bpjs_ks)) # BPJS Kesehatan Perusahaan 4%
			bruto = ga_pok + tunjangan + bpjs_ktg_per_jkk + bpjs_ktg_per_jkm + bpjs_kes_per

			bpjs_ktg_kar_jht = int(float(float(2)/100) * int( bpjs_kt)) # BPJS Ketenagakerjaan Karyawan Jaminan Hari Tua 2%
			bpjs_ktg_per_jpn = int(float(float(2)/100) * int( bpjs_kt)) # BPJS Ketenagakerjaan Perusahaan Jaminan Kematian 2%

			kpjkk = bpjs_ktg_per_jkk
			kpjht = int(float(float(3.70)/100) * int( bpjs_kt))
			kpjkm = bpjs_ktg_per_jkm
			kpjp = int(float(float(2)/100) * int( bpjs_kt))
			totala = kpjkk + kpjht + kpjkm + kpjp
			kpkes = bpjs_kes_per
			totalb = totala + kpkes
			kkjht = int(float(float(2)/100) * int( bpjs_kt))
			kkjp = int(float(float(1)/100) * int( bpjs_kt))
			totalc = kkjht + kkjp
			kkkes = int(float(float(1)/100) * int( bpjs_ks))
			totald = totalc + kkkes

			ph_netto_sebulan = bruto - ( (int(float(float(5)/100) * int(bruto))) + bpjs_ktg_kar_jht + bpjs_ktg_per_jpn )

			ph_netto_setahun = ph_netto_sebulan * 12

			ph_kena_pajak = ph_netto_setahun - ptkp

			pph_terhutang = int(wp * int(ph_kena_pajak))

			pph = pph_terhutang / 12
			pph = 0 if pph < 0 else pph

			if k.NPWP == 0 or k.NPWP == None :
				pph = int(float(float(120)/100) * int(pph))
			
			objs.append(bpjs(y, k.KPJ, k.NIK, k.name, 
									k.gender, kpjkk, kpjht, kpjkm, kpjp, 
									totala, kpkes, totalb, kkjht, kkjp, totalc, kkkes, totald))
	objs.pop(0)
	wb = xlwt.Workbook()
	ws = wb.add_sheet('Laporan Gaji',cell_overwrite_ok=True)

	ws.write(1, 6, "Laporan BPJS")
	ws.write(2, 6, "Periode " + mas.name + " " + mas.tanggal.strftime("%d-%m-%Y") + " s/d " + mas.sd.strftime("%d-%m-%Y"))
	ws.write(4, 1, "No")
	ws.write(4, 2, "KPJ")
	ws.write(4, 3, "NIK")
	ws.write(4, 4, "Nama")
	ws.write(4, 5, "Sex")
	ws.write(4, 6, "KP JKK")
	ws.write(4, 7, "KP JHT")
	ws.write(4, 8, "KP JKM")
	ws.write(4, 9, "KP JP")
	ws.write(4, 10, "Total")
	ws.write(4, 11, "KP Kesehatan")
	ws.write(4, 12, "Total KP")
	ws.write(4, 13, "KK JHT")
	ws.write(4, 14, "KK JP")
	ws.write(4, 15, "Total")
	ws.write(4, 16, "KK Kesehatan")
	ws.write(4, 17, "Total KK")

	y=4

	ob = objs

	for x in range(1, len(objs)):
		ws.write(ob[x].no+y, 1, ob[x].no)
		ws.write(ob[x].no+y, 2, ob[x].kpj)
		ws.write(ob[x].no+y, 3, ob[x].nik)
		ws.write(ob[x].no+y, 4, ob[x].nama)
		ws.write(ob[x].no+y, 5, ob[x].sex)
		ws.write(ob[x].no+y, 6, ob[x].kpjkk)
		ws.write(ob[x].no+y, 7, ob[x].kpjht)
		ws.write(ob[x].no+y, 8, ob[x].kpjkm)
		ws.write(ob[x].no+y, 9, ob[x].kpjp)
		ws.write(ob[x].no+y, 10, ob[x].totala)
		ws.write(ob[x].no+y, 11, ob[x].kpkes)
		ws.write(ob[x].no+y, 12, ob[x].totalb)
		ws.write(ob[x].no+y, 13, ob[x].kkjht)
		ws.write(ob[x].no+y, 14, ob[x].kkjp)
		ws.write(ob[x].no+y, 15, ob[x].totalc)
		ws.write(ob[x].no+y, 16, ob[x].kkkes)
		ws.write(ob[x].no+y, 17, ob[x].totald)

	wb.save("laporan/bpjs/LAPORAN BPJS " + mas.name + ' ' + mas.tanggal.strftime("%d-%m-%Y") +' .s.d ' + mas.tanggal.strftime("%d-%m-%Y") +'-' + datetime.datetime.now().strftime("%d%m%Y-%H%M%S") + '.xls')

	return redirect("laporanbpjs-index")

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
			pbpjs_ks = 0
			pbpjs_kt = 0
			ppinjam = 0
			pkoperasi = 0
			pabsen = 0
			pph = 0
			umut = 0
			kemahalan = 0
			telepon = 0

			def __init__(self, no, nik, nama, departemen, bagian, 
								golongan, norek, gajipokok, statusmenikah, tmakan, 
								transportnonexec, tovertime, tunjangan, pbpjs_ks, pbpjs_kt, 
								ppinjam, pkoperasi, pabsen, pph, umut, kemahalan, telepon):
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
				self.pbpjs_ks = pbpjs_ks
				self.pbpjs_kt = pbpjs_kt
				self.ppinjam = ppinjam
				self.pkoperasi = pkoperasi
				self.pabsen = pabsen
				self.pph = pph
				self.umut = umut
				self.kemahalan = kemahalan
				self.telepon = telepon

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
			k = Karyawan.objects.get(pk=b.id)
			g = GajiPokok.objects.get(karyawan_id=b.id)
			p = PotonganKaryawan.objects.get(karyawan_id=b.id)
			tt = TunjanganKaryawan.objects.get(karyawan_id=b.id)

			gajipokok = g.gajipokok 
			tunjanganmakan = tt.tmakan
			makanlembur = g.makanlembur
			transportnonexec = tt.transportnonexec
			kemahalan = tt.kemahalan
			ttelepon = tt.ttelepon
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

			date_format = "%Y-%m-%d"
			hari = mas.sd - mas.tanggal
			hari = hari.days

			banyak = len(ab)

			if k.jumlahhari == 5 :
				hari = 21
				bjam = 8
			elif k.jumlahhari == 6 :
				hari = 25
				bjam = 7	

			for abi in ab:
				if abi.SPL == 1:
					hari = abi.created_at.strftime("%A")
					FMT = '%H:%M:%S'
					penjumlahan = datetime.datetime.strptime(abi.keluar.strftime("%H:%M:%S"), FMT) - datetime.datetime.strptime(abi.masuk.strftime("%H:%M:%S"), FMT)
					penjumlahan = (penjumlahan.seconds / 3600)
					istirahat = ( penjumlahan / 5 )
					banyakwaktu = penjumlahan - bjam - istirahat
					if hari == "Minggu" or hari == "Sunday" :
						hitungot = abi.SPL_banyak
						if abi.karyawan.golongan.id == 7 or abi.karyawan.golongan.id == 8 :
							if banyakwaktu <= 7 :
								tovertime = tovertime + int(float((banyakwaktu * 2) * 10000))
							elif banyakwaktu > 7 :
								tovertime = tovertime + int(float((7 * 2) * 10000))
								tovertime = tovertime + ( ( ( banyakwaktu - 7 ) * 3 ) * 10000 )
						elif abi.karyawan.golongan.id < 7 :
							if banyakwaktu <= 7 :
								tovertime = tovertime + int(float((banyakwaktu * 2) * 20000))
							elif banyakwaktu > 7 :
								tovertime = tovertime + int(float((7 * 2) * 10000))
								tovertime = tovertime + ( ( ( banyakwaktu - 7 ) * 3 ) * 20000 )
					else:
						if abi.karyawan.golongan.id == 7 or abi.karyawan.golongan.id == 8 :
							if banyakwaktu <= 1 :
								tovertime = tovertime + int(float(1.5 * 10000))
							elif banyakwaktu > 1 :
								tovertime = tovertime + int(float(1.5 * 10000))
								tovertime = tovertime + ( ( ( banyakwaktu - 1 ) * 2 ) * 10000 )
						elif abi.karyawan.golongan.id < 7 :
							if banyakwaktu >= 1 :
								tovertime = tovertime + int(float(1.5 * 20000))
							elif banyakwaktu > 1 :
								tovertime = tovertime + int(float(1.5 * 20000))
								tovertime = tovertime + ( ( ( banyakwaktu - 1 ) * 2 ) * 20000 )

				if waktu(abi.masuk, abi.karyawanshift.shift.jammasuk, True) > 300:
					pabsen = pabsen + 1

			if k.jumlahhari == 5 :
				hari = 21
			elif k.jumlahhari == 6 :
				hari = 25

			# hari = mas.sd - mas.tanggal
			# hari = hari.days

			if k.golongan.id == 7 or k.golongan.id == 8 :
				pabsen = pabsen * 20000
				tunjanganmakan = int( 20000 * hari )
				transportnonexec = int( 20000 * hari )			
			elif k.golongan.id == 6 or k.golongan.id == 5 :
				pabsen = pabsen * 40000
				tunjanganmakan = int( 40000 * hari ) * banyak
				transportnonexec = int( 40000 * hari )			
			elif k.golongan_id < 5:
				pabsen = pabsen * 60000
				tunjanganmakan = int( 60000 * hari )
				transportnonexec = int( 60000 * hari )

			UMUT = 	(tunjanganmakan + transportnonexec)	
			pabsen = UMUT - pabsen

			wp = 0

			gapok = g.gajipokok
			ga_pok = gapok + UMUT + g.jabatan
			gatu = ga_pok - UMUT
			ga_pokii = gatu * (75/100)
			tunjangan_ii = gatu * (25/100)

			if k.golongan.id == 7 or k.golongan.id == 8 :
				mangkir = (gatu / hari) + 20000	
				mangkir = (hari - banyak) * mangkir
			elif k.golongan.id == 6 or k.golongan.id == 5 :
				mangkir = (gatu / hari) + 40000		
				mangkir = (hari - banyak) * mangkir
			elif k.golongan_id < 5:
				mangkir = (gatu / hari) + 60000
				mangkir = (hari - banyak) * mangkir

			ga_pok = ga_pok - mangkir

			status = b.statusmenikah.desc
			tunjangan = g.jabatan + tt.kemahalan + UMUT
			pph = 0
			bpjs_ks = p.bpjs_ks
			bpjs_kt = p.bpjs_kt

			if ga_pok <= 50000000 :
			  wp = float(float(5)/100) 
			elif ga_pok > 50000000 or ga_pok <= 250000000 :
			  wp = float(float(15)/100) 
			elif ga_pok > 250000000 or ga_pok <= 500000000 :
			  wp = float(float(25)/100)
			elif ga_pok > 500000000 :
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

			bpjs_ktg_per_jkk = int(float(float(0.54)/100) * int( bpjs_kt)) # BPJS Ketenagakerjaan Perusahaan Kecelakaan Kerja 0.54% 
			bpjs_ktg_per_jkm = int(float(float(0.3)/100) * int( bpjs_kt)) # BPJS Ketenagakerjaan Perusaaan Jaminan Kematian 0.3%
			bpjs_kes_per = int(float(float(4)/100) * int(bpjs_ks)) # BPJS Kesehatan Perusahaan 4%
			bruto = ga_pok + tunjangan + bpjs_ktg_per_jkk + bpjs_ktg_per_jkm + bpjs_kes_per

			bpjs_ktg_kar_jht = int(float(float(2)/100) * int( bpjs_kt)) # BPJS Ketenagakerjaan Karyawan Jaminan Hari Tua 2%
			bpjs_ktg_per_jpn = int(float(float(2)/100) * int( bpjs_kt)) # BPJS Ketenagakerjaan Perusahaan Jaminan Kematian 2%

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
									g.jabatan, p.bpjs_ks, p.bpjs_kt, cicil, p.koperasi, pabsen, pph, g.umut, kemahalan, ttelepon))

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
			tunjanganmakan = tt.tmakan
			makanlembur = g.makanlembur
			transportnonexec = tt.transportnonexec
			kemahalan = tt.kemahalan
			ttelepon = tt.ttelepon

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

			date_format = "%Y-%m-%d"
			hari = mas.sd - mas.tanggal
			hari = hari.days

			banyak = len(ab)

			if k.jumlahhari == 5 :
				hari = 21
				bjam = 8
			elif k.jumlahhari == 6 :
				hari = 25
				bjam = 7	
			
			for abi in ab:
				if abi.SPL == 1:
					hari = abi.created_at.strftime("%A")
					FMT = '%H:%M:%S'
					penjumlahan = datetime.datetime.strptime(abi.keluar.strftime("%H:%M:%S"), FMT) - datetime.datetime.strptime(abi.masuk.strftime("%H:%M:%S"), FMT)
					penjumlahan = (penjumlahan.seconds / 3600)
					istirahat = ( penjumlahan / 5 )
					banyakwaktu = penjumlahan - bjam - istirahat
					if hari == "Minggu" or hari == "Sunday" :
						hitungot = abi.SPL_banyak
						if abi.karyawan.golongan.id == 7 or abi.karyawan.golongan.id == 8 :
							if banyakwaktu <= 7 :
								tovertime = tovertime + int(float((banyakwaktu * 2) * 10000))
							elif banyakwaktu > 7 :
								tovertime = tovertime + int(float((7 * 2) * 10000))
								tovertime = tovertime + ( ( ( banyakwaktu - 7 ) * 3 ) * 10000 )
						elif abi.karyawan.golongan.id < 7 :
							if banyakwaktu <= 7 :
								tovertime = tovertime + int(float((banyakwaktu * 2) * 20000))
							elif banyakwaktu > 7 :
								tovertime = tovertime + int(float((7 * 2) * 10000))
								tovertime = tovertime + ( ( ( banyakwaktu - 7 ) * 3 ) * 20000 )
					else:
						if abi.karyawan.golongan.id == 7 or abi.karyawan.golongan.id == 8 :
							if banyakwaktu <= 1 :
								tovertime = tovertime + int(float(1.5 * 10000))
							elif banyakwaktu > 1 :
								tovertime = tovertime + int(float(1.5 * 10000))
								tovertime = tovertime + ( ( ( banyakwaktu - 1 ) * 2 ) * 10000 )
						elif abi.karyawan.golongan.id < 7 :
							if banyakwaktu >= 1 :
								tovertime = tovertime + int(float(1.5 * 20000))
							elif banyakwaktu > 1 :
								tovertime = tovertime + int(float(1.5 * 20000))
								tovertime = tovertime + ( ( ( banyakwaktu - 1 ) * 2 ) * 20000 )

				if waktu(abi.masuk, abi.karyawanshift.shift.jammasuk, True) > 300:
					pabsen = pabsen + 1

			if k.jumlahhari == 5 :
				hari = 21
			elif k.jumlahhari == 6 :
				hari = 25

			if k.golongan.id == 7 or k.golongan.id == 8 :
				pabsen = pabsen * 20000
				tunjanganmakan = int( 20000 * hari )
				transportnonexec = int( 20000 * hari )			
			elif k.golongan.id == 6 or k.golongan.id == 5 :
				pabsen = pabsen * 40000
				tunjanganmakan = int( 40000 * hari ) * banyak
				transportnonexec = int( 40000 * hari )			
			elif k.golongan_id < 5:
				pabsen = pabsen * 60000
				tunjanganmakan = int( 60000 * hari )
				transportnonexec = int( 60000 * hari )

			UMUT = 	(tunjanganmakan + transportnonexec)	
			pabsen = UMUT - pabsen

			if k.golongan.id == 7 or k.golongan.id == 8 :
				mangkir = (gatu / hari) + 20000	
				mangkir = (hari - banyak) * mangkir
			elif k.golongan.id == 6 or k.golongan.id == 5 :
				mangkir = (gatu / hari) + 40000		
				mangkir = (hari - banyak) * mangkir
			elif k.golongan_id < 5:
				mangkir = (gatu / hari) + 60000
				mangkir = (hari - banyak) * mangkir

			ga_pok = ga_pok - mangkir
			
			gapok = g.gajipokok
			ga_pok = gapok + UMUT + g.jabatan
			gatu = ga_pok - UMUT
			ga_pokii = gatu * (75/100)
			tunjangan_ii = gatu * (25/100)

			status = k.statusmenikah.desc
			tunjangan = g.jabatan + tt.kemahalan + UMUT
			pph = 0
			bpjs_ks = p.bpjs_ks
			bpjs_kt = p.bpjs_kt

			if ga_pok <= 50000000 :
			  wp = float(float(5)/100) 
			elif ga_pok > 50000000 or ga_pok <= 250000000 :
			  wp = float(float(15)/100) 
			elif ga_pok > 250000000 or ga_pok <= 500000000 :
			  wp = float(float(25)/100)
			elif ga_pok > 500000000 :
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

			bpjs_ktg_per_jkk = int(float(float(0.54)/100) * int( bpjs_kt)) # BPJS Ketenagakerjaan Perusahaan Kecelakaan Kerja 0.54% 
			bpjs_ktg_per_jkm = int(float(float(0.3)/100) * int( bpjs_kt)) # BPJS Ketenagakerjaan Perusaaan Jaminan Kematian 0.3%
			bpjs_kes_per = int(float(float(4)/100) * int(bpjs_ks)) # BPJS Kesehatan Perusahaan 4%
			bruto = ga_pok + tunjangan + bpjs_ktg_per_jkk + bpjs_ktg_per_jkm + bpjs_kes_per

			bpjs_ktg_kar_jht = int(float(float(2)/100) * int( bpjs_kt)) # BPJS Ketenagakerjaan Karyawan Jaminan Hari Tua 2%
			bpjs_ktg_per_jpn = int(float(float(2)/100) * int( bpjs_kt)) # BPJS Ketenagakerjaan Perusahaan Jaminan Kematian 2%

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
									g.jabatan, p.bpjs_ks, p.bpjs_kt, cicil, p.koperasi, pabsen, pph, g.umut, kemahalan, ttelepon))
	objs.pop(0)
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
	ws.write(4, 8, "Jabatan")
	ws.write(4, 9, "UMUT Lumpsum")
	ws.write(4, 10, "Makan")
	ws.write(4, 11, "Transportasi")
	ws.write(4, 12, "Kemahalan")
	ws.write(4, 13, "Telepon")
	ws.write(4, 14, "JKK+JKM+JKES")
	ws.write(4, 15, "PPh 21")
	ws.write(4, 16, "Gaji Kotor")
	ws.write(4, 17, "Overtime")
	ws.write(4, 18, "Potongan Pinjaman")
	ws.write(4, 19, "Potongan Koperasi")
	ws.write(4, 20, "BPJS")	
	ws.write(4, 21, "Potongan BPJS Kesehatan")
	ws.write(4, 22, "Potongan BPJS Kesehatan")
	ws.write(4, 23, "Total Potongan BPJS")
	ws.write(4, 24, "Potongan Absensi")

	y=4

	ob = objs

	for x in range(1, len(objs)):
		bpjs_kes_kar = int(float(float(1)/100) * int(ob[x].pbpjs_ks)) # BPJS Kesehatan Karyawan 1%
		bpjs_kes_per = int(float(float(4)/100) * int(ob[x].pbpjs_ks)) # BPJS Kesehatan Perusahaan 4%
		bpjs_ktg_kar_jpn = int(float(float(1)/100) * int(ob[x].pbpjs_kt)) # BPJS Ketenagakerjaan Karyawan Jaminan Pensiunan 1%
		bpjs_ktg_kar_jht = int(float(float(2)/100) * int(ob[x].pbpjs_kt)) # BPJS Ketenagakerjaan Karyawan Jaminan Hari Tua 2%
		bpjs_ktg_per_jpn = int(float(float(2)/100) * int(ob[x].pbpjs_kt)) # BPJS Ketenagakerjaan Perusahaan Jaminan Kematian 2%
		bpjs_ktg_per_jkk = int(float(float(0.54)/100) * int(ob[x].pbpjs_kt)) # BPJS Ketenagakerjaan Perusahaan Kecelakaan Kerja 0.54% 
		bpjs_ktg_per_jht = int(float(float(3.7)/100) * int(ob[x].pbpjs_kt)) # BPJS Ketenagakerjaan Perusahaan Jaminan Hari Tua 3.7%
		bpjs_ktg_per_jkn = int(float(float(0.3)/100) * int(ob[x].pbpjs_kt)) # BPJS Ketenagakerjaan Perusaaan Jaminan Kematian 0.3%
		bpjs_kes = bpjs_kes_kar #+ bpjs_kes_per
		bpjs_ktg = bpjs_ktg_kar_jpn + bpjs_ktg_kar_jht #+ bpjs_ktg_per_jpn + bpjs_ktg_per_jkk + bpjs_ktg_per_jht
		bpjs_total = bpjs_kes + bpjs_ktg

		ws.write(ob[x].no+y, 1, ob[x].no)
		ws.write(ob[x].no+y, 2, ob[x].nik)
		ws.write(ob[x].no+y, 3, ob[x].nama)
		ws.write(ob[x].no+y, 4, ob[x].departemen)
		ws.write(ob[x].no+y, 5, ob[x].bagian)
		ws.write(ob[x].no+y, 6, ob[x].golongan)
		ws.write(ob[x].no+y, 7, ob[x].gajipokok)
		ws.write(ob[x].no+y, 8, ob[x].tunjangan)
		ws.write(ob[x].no+y, 9, ob[x].umut)
		ws.write(ob[x].no+y, 10, ob[x].tmakan)
		ws.write(ob[x].no+y, 11, ob[x].transportnonexec)
		ws.write(ob[x].no+y, 12, ob[x].kemahalan)
		ws.write(ob[x].no+y, 13, ob[x].telepon)
		ws.write(ob[x].no+y, 14, bpjs_ktg_per_jkk+bpjs_ktg_per_jkn+bpjs_kes_per)
		ws.write(ob[x].no+y, 15, ob[x].pph)
		gajikotor = ob[x].pph + ob[x].gajipokok + ob[x].tunjangan + ob[x].umut + ob[x].tmakan + ob[x].transportnonexec + ob[x].kemahalan + ob[x].telepon + bpjs_ktg_per_jkk+bpjs_ktg_per_jkn+bpjs_kes_per
		ws.write(ob[x].no+y, 16, gajikotor)
		ws.write(ob[x].no+y, 17, ob[x].tovertime)
		ws.write(ob[x].no+y, 18, ob[x].ppinjam)
		ws.write(ob[x].no+y, 19, ob[x].pkoperasi)		
		ws.write(ob[x].no+y, 20, bpjs_kes)
		ws.write(ob[x].no+y, 21, bpjs_ktg)
		ws.write(ob[x].no+y, 22, bpjs_total)
		ws.write(ob[x].no+y, 23, ob[x].pabsen)

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

@login_required()
def laporanpinjaman(request):

	style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on',
    					 num_format_str='#,##0.00')
	style1 = xlwt.easyxf(num_format_str='D-MMM-YY')

	objs = [0]

	class postpinjaman(object):
			no = ""
			nik = ""
			nama = ""
			departemen = ""
			bagian = ""
			golongan = ""
			pinjaman = 0
			cicil = 0
			koperasi = 0
			cicil_koperasi = 0
			pinjlain = 0
			cicil_pinjlain = 0
			inventory_pinjaman = ""
			tanggal_pinjam = ""
			tanggal_kembali = ""

			def __init__(self, no, nik, nama, departemen, bagian, golongan, 
						 pinjaman, cicil, koperasi, cicil_koperasi,
						 pinjlain, cicil_pinjlain, inventory_pinjaman, tanggal_pinjam, tanggal_kembali):
				self.no = no
				self.nik = nik
				self.nama = nama
				self.departemen = departemen
				self.bagian = bagian
				self.golongan = golongan
				self.pinjaman = pinjaman
				self.cicil = cicil
				self.koperasi = koperasi
				self.cicil_koperasi = cicil_koperasi
				self.pinjlain = pinjlain
				self.cicil_pinjlain = cicil_pinjlain
				self.inventory_pinjaman = inventory_pinjaman
				self.tanggal_pinjam = tanggal_pinjam
				self.tanggal_kembali = tanggal_kembali


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
			try:
				print b.id
				p = Pinjaman.objects.get(karyawan_id=b.id)
				try:
					potongan = PotonganKaryawan.objects.filter(karyawan=b.id).filter(masatenggangclosing=masatenggangclosing).get()

					tglpinjam = ""
					tglkembali = ""

					if isinstance(p.tglpinjam, datetime.date) :
						tglpinjam = p.tglpinjam.strftime("%d-%m-%Y")
					if isinstance(p.tglkembali, datetime.date) :
						tglkembali = p.tglkembali.strftime("%d-%m-%Y")


					objs.append(postpinjaman(y+1, b.NIK, b.name, b.departemen.name, b.bagian.name, b.golongan.name,
											potongan.pinjkaryawan, potongan.cicil_pinjkaryawan, potongan.koperasi, potongan.cicil_koperasi,
											potongan.pinjlain, potongan.cicil_pinjlain, p.inventory.name, tglpinjam , tglkembali))
				except PotonganKaryawan.DoesNotExist:		
					objs.append(postpinjaman(y+1, b.NIK, b.name, b.departemen.name, b.bagian.name, b.golongan.name,
											0, 0, 0, 0,
											0, 0, p.inventory.name, p.tglpinjam, p.tglkembali))	
			except Pinjaman.DoesNotExist:
				try:
					potongan = PotonganKaryawan.objects.filter(karyawan=b.id).filter(masatenggangclosing=masatenggangclosing).get()
					objs.append(postpinjaman(y+1, b.NIK, b.name, b.departemen.name, b.bagian.name, b.golongan.name,
											potongan.pinjkaryawan, potongan.cicil_pinjkaryawan, potongan.koperasi, potongan.cicil_koperasi,
											potongan.pinjlain, potongan.cicil_pinjlain, "Tidak ada", "", ""))
				except PotonganKaryawan.DoesNotExist:		
					objs.append(postpinjaman(y+1, b.NIK, b.name, b.departemen.name, b.bagian.name, b.golongan.name,
											0, 0, 0, 0,
											0, 0, "Tidak ada", "", ""))	
			y=y+1
				


	else:
		listid = [x.strip() for x in idkaryawan.split(',')]
		a = ""
		mantap = ""
		objs = [range(0, len(listid)-1)]

		for y in range(0, len(listid)-1):

			try:
				p = Pinjaman.objects.get(karyawan_id=listid[y])
				try:
					potongan = PotonganKaryawan.objects.filter(karyawan=listid[y]).filter(masatenggangclosing=masatenggangclosing).get()

					tglpinjam = ""
					tglkembali = ""

					if isinstance(p.tglpinjam, datetime.datetime) :
						tglpinjam = p.tglpinjam.strftime("%d-%m-%Y")
					if isinstance(p.tglkembali, datetime.datetime) :
						tglkembali = p.tglkembali.strftime("%d-%m-%Y")

					objs.append(postpinjaman(y, b.NIK, b.name, b.departemen.name, b.bagian.name, b.golongan.name,
											potongan.pinjkaryawan, potongan.cicil_pinjkaryawan, potongan.koperasi, potongan.cicil_koperasi,
											potongan.pinjlain, potongan.cicil_pinjlain, p.inventory.name, tglpinjam, tglkembali))
				except PotonganKaryawan.DoesNotExist:		
					objs.append(postpinjaman(y, b.NIK, b.name, b.departemen.name, b.bagian.name, b.golongan.name,
											0, 0, 0, 0,
											0, 0, p.inventory.name, p.tglpinjam, p.tglkembali))	
			except Pinjaman.DoesNotExist:
				try:
					potongan = PotonganKaryawan.objects.filter(karyawan=listid[y]).filter(masatenggangclosing=masatenggangclosing).get()
					objs.append(postpinjaman(y, b.NIK, b.name, b.departemen.name, b.bagian.name, b.golongan.name,
											potongan.pinjkaryawan, potongan.cicil_pinjkaryawan, potongan.koperasi, potongan.cicil_koperasi,
											potongan.pinjlain, potongan.cicil_pinjlain, "Tidak ada", "", ""))
				except PotonganKaryawan.DoesNotExist:		
					objs.append(postpinjaman(y, b.NIK, b.name, b.departemen.name, b.bagian.name, b.golongan.name,
											0, 0, 0, 0,
											0, 0, "Tidak ada", "", ""))	
	
	wb = xlwt.Workbook()
	ws = wb.add_sheet('Laporan Pinjaman Karyawan' ,cell_overwrite_ok=True )

	print len(objs)

	ws.write(1, 6, "Laporan Pinjaman Karyawan")
	ws.write(2, 6, "Masa Tenggang Closing " + mas.name)
	ws.write(4, 1, "No")
	ws.write(4, 2, "NIK")
	ws.write(4, 3, "Nama")
	ws.write(4, 4, "Departemen")
	ws.write(4, 5, "Bagian")
	ws.write(4, 6, "Golongan")
	ws.write(4, 7, "Pinjaman Karyawan")
	ws.write(4, 8, "Sisa cicilan")
	ws.write(4, 9, "Koperasi")
	ws.write(4, 10, "Sisa cicilan")
	ws.write(4, 11, "Pinjaman Lain")
	ws.write(4, 12, "Sisa cicilan")
	ws.write(4, 13, "Pinjaman Inventory")
	ws.write(4, 14, "Tanggal Pinjam")
	ws.write(4, 15, "Tanggal Kembali")

	y=4

	ob = objs

	for x in range(1, len(objs)):
		ws.write(ob[x].no+y, 1, ob[x].no)
		ws.write(ob[x].no+y, 2, ob[x].nik)
		ws.write(ob[x].no+y, 3, ob[x].nama)
		ws.write(ob[x].no+y, 4, ob[x].departemen)
		ws.write(ob[x].no+y, 5, ob[x].bagian)
		ws.write(ob[x].no+y, 6, ob[x].golongan)
		ws.write(ob[x].no+y, 7, ob[x].pinjaman)
		ws.write(ob[x].no+y, 8, ob[x].cicil)
		ws.write(ob[x].no+y, 9, ob[x].koperasi)
		ws.write(ob[x].no+y, 10, ob[x].cicil_koperasi)
		ws.write(ob[x].no+y, 11, ob[x].pinjlain)
		ws.write(ob[x].no+y, 12, ob[x].cicil_pinjlain)
		ws.write(ob[x].no+y, 13, ob[x].inventory_pinjaman )
		ws.write(ob[x].no+y, 14, ob[x].tanggal_pinjam )
		ws.write(ob[x].no+y, 15, ob[x].tanggal_kembali )

	wb.save("laporan/pinjaman/LAPORAN PINJAMAN " + mas.name + ' ' + 
		     mas.tanggal.strftime("%d-%m-%Y") +' .s.d ' + mas.tanggal.strftime("%d-%m-%Y") +'-' + 
		     datetime.datetime.now().strftime("%d%m%Y-%H%M%S") + '.xls')

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