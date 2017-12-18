from django.core.management.base import BaseCommand, CommandError
from pprint import pprint
from system.models import Karyawan, Perusahaan, Bank, Departemen, Bagian, GajiPokok, Jabatan
from openpyxl import load_workbook
import argparse
from datetime import datetime

class Command(BaseCommand):
  args = 'Arguments is not needed'
  help = 'Django admin custom command poc.'

  # def add_arguments(self, parser):
 	# parser.add_argument("pile", type=argparse.FileType(), required=True)

  def handle(self, *args, **options):
  	wb = load_workbook(filename ="payroll-template.xlsx")
  	ax = wb['Sheet1']

  	y = 3
  	for x in range(3,417):
  		banyakpegawai = Karyawan.objects.filter(tanggalmasuk__year=ax['K' + str(y)].value.strftime("%Y"), tanggalmasuk__month=ax['K' + str(y)].value.strftime("%m"))
	  	banyakpegawai = len(banyakpegawai)+1
	  	jarak = "000"
	  	if banyakpegawai > 9 :
	  		jarak = "00"
	  	elif banyakpegawai > 99 :
	  		jarak = "0"
	  	elif banyakpegawai > 999 :
	  		jarak = "" 

	  	NIK = "GC" + str(ax['AF' + str(y)].value) + ax['K' + str(y)].value.strftime("%Y")[2:] + ax['K' + str(y)].value.strftime("%m") + jarak + str(banyakpegawai)
	  	nama = str(ax['B' + str(y)].value)
	  	gender = str(ax['C' + str(y)].value)
	  	norek = str(ax['T' + str(y)].value)
	  	bank = Bank.objects.get(name="Bank " + str(ax['S' + str(y)].value))
	  	jumlahhari = ax['Z' + str(y)].value
	  	try:
	  		dp = Departemen.objects.get(name=str(ax['AD' + str(y)].value))
	  	except Departemen.DoesNotExist:
	  		dp = Departemen(name=str(ax['AD' + str(y)].value), desc=str(ax['AD' + str(y)].value))
			dp.save()

		try:
	  		bg = Bagian.objects.get(name=str(ax['AE' + str(y)].value))
	  	except Bagian.DoesNotExist:
	  		bg = Bagian(name=str(ax['AE' + str(y)].value), desc=str(ax['AE' + str(y)].value))
			bg.save()

		try:
	  		ps = Perusahaan.objects.get(name=str(ax['AC' + str(y)].value))
	  	except Perusahaan.DoesNotExist:
	  		ps = Perusahaan(name=str(ax['AC' + str(y)].value), desc=str(ax['AC' + str(y)].value))
			ps.save()

	  	try:
	  		jb = Jabatan.objects.get(name=str(ax['AG' + str(y)].value))
	  		jb = jb.id
	  	except Jabatan.DoesNotExist:
	  		jb = Jabatan(name=str(ax['AG' + str(y)].value), desc=str(ax['AG' + str(y)].value))
			jb.save()
			jb = jb.id

  		k = Karyawan(NIK = NIK, name = nama, gender = gender,
					tanggalmasuk = ax['K' + str(y)].value.strftime("%Y-%m-%d"),
					bank_id = bank.id,
					norek =norek, jumlahhari = jumlahhari,
					departemen_id = dp.id, bagian_id = bg.id,
					golongan_id = ax['AF' + str(y)].value,
					perusahaan_id= ps.id, jabatan_id = jb)
		k.save()

		g = GajiPokok(karyawan_id=k.id, name="Gaji Pokok " + k.name, gajipokok=ax['AA' + str(y)].value, 
					jumlahhari = jumlahhari, jabatan = ax['AB' + str(y)].value)
		g.save()

		y = y + 1
		print "["+ str(y) +"] Tambah karyawan " + nama + " Sukses"

  	#print(ax['K3'].value).strftime("%Y-%m-%d")
  	

  	# k = Perusahaan.objects.get(name="PT. Galuh Mas Citarum"))
  	# print(NIK)