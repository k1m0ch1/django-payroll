from django.core.management.base import BaseCommand, CommandError
from pprint import pprint
from system.models import Karyawan, Perusahaan, Bank, Departemen, Bagian, GajiPokok, Jabatan, TunjanganKaryawan, Bonusthr, Mesin, KaryawanMesin
from openpyxl import load_workbook
import argparse, pyping, time
from datetime import datetime
from zk import ZK, const

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
	  	try:
	  		bank = Bank.objects.get(name="Bank " + str(ax['S' + str(y)].value))
	  	except Bank.DoesNotExist:
	  		bank = Bank(name=str("Bank" + str(ax['S' + str(y)].value)), desc=str(ax['S' + str(y)].value))
			bank.save()

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
					jumlahhari = jumlahhari, jabatan = ax['AB' + str(y)].value, umut = ax['AH' + str(y)].value)
		g.save()

		t = TunjanganKaryawan(kemahalan=ax['AI' + str(y)].value, karyawan_id=k.id,
								transportnonexec=ax['AJ' + str(y)].value, ttelepon = ax['AK' + str(y)].value)
		t.save()

		pollutebonus = Bonusthr(karyawan_id=k.id)
		pollutebonus.save()

		y = y + 1

		msn = Mesin.objects.all()
		for z in msn:
			response = pyping.ping(z.ip, timeout=800, packet_size=10)
			msn = Mesin.objects.select_for_update().filter(id=z.id)
			if response.ret_code == 0:		    
			    msn.update(status="UP", last_up = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), last_check = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') )
			else:
			    msn.update(status="DOWN", last_down = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), last_check = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') )


		# Fungsi menambahkan karyawan ke dalam mesin absensi
		mesin = Mesin.objects.all()
		conn = None
		for m in mesin:
			if m.status == "UP":
				zk = ZK(m.ip, port=4370, timeout=5)
				try:
					conn = zk.connect()
					datausers = conn.get_users()
					userid = 1
					for user in datausers:
						userid = userid + 1
					conn.set_user(uid=userid, name=nama, privilege=const.USER_DEFAULT, password="", group_id="", user_id=str(userid))
					km = KaryawanMesin(mesin_id=m.id, karyawan_id=k.id, userid=userid)
					km.save()
					#conn.test_voice()
				except Exception, e:
					print "Process terminate : {}" . format(e)
				finally:
					if conn:
						conn.disconnect()

		print "["+ str(y) +"] Tambah karyawan " + nama + " Tersimpan di mesin absensi"

  	#print(ax['K3'].value).strftime("%Y-%m-%d")
  	

  	# k = Perusahaan.objects.get(name="PT. Galuh Mas Citarum"))
  	# print(NIK)