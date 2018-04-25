from django.core.management.base import BaseCommand, CommandError
from pprint import pprint
from system.models import Karyawan, Perusahaan, Bank, Departemen, Bagian, GajiPokok, Jabatan, TunjanganKaryawan, Bonusthr, Mesin, KaryawanMesin, Absensi, KaryawanShift
from openpyxl import load_workbook
import argparse, pyping, time
import datetime
from zk import ZK, const

class Command(BaseCommand):
	args = 'Arguments is not needed'
	help = 'Django admin custom command poc.'

	def handle(self, *args, **options):
		# status 0 = masuk
		# status 1 = keluar
		sampledata = {'status': 0, 'timestamp': datetime.datetime(2016, 8, 27, 12, 34, 3), 'user_id': '12'}, {'status': 0, 'timestamp': datetime.datetime(2016, 8, 28, 12, 38, 33),  'user_id': '12'}, {'status': 0, 'timestamp': datetime.datetime(2016, 8, 29, 12, 52, 25), 'user_id': '12'}, {'status': 0, 'timestamp': datetime.datetime(2016, 8, 30, 12, 52, 41), 'user_id': '12'}, {'status': 1, 'timestamp': datetime.datetime(2016, 8, 27, 17, 52, 41), 'user_id': '12'}

		for x in sampledata:
			status = x['status']
			userid = x['user_id']
			tanggal = x['timestamp'].strftime("%Y") + "-" + x['timestamp'].strftime("%m") + "-" + x['timestamp'].strftime("%d")
			hari = x['timestamp'].strftime("%a")
			waktu = x['timestamp'].strftime("%H") + ":" + x['timestamp'].strftime("%M") + ":" + x['timestamp'].strftime("%S")
			cariid = Karyawan.objects.filter(fingerid=x['user_id'])
			if len(cariid) > 0:
				if status == 0:
					ks = KaryawanShift.objects.filter(karyawan_id=cariid[0].id)
					for find in ks:
						tglaw = find.tglawal
						tglak = find.tglakhir
						now = tanggal
						if tglaw <= x['timestamp'].date() <= tglak:
							a = Absensi(karyawan_id=cariid[0].id, tanggal=tanggal, hari=hari, masuk=waktu, karyawanshift_id=find.id)					
							a.save()
							print "Data Added"					
				else:
					a = Absensi.objects.select_for_update().filter(karyawan_id=cariid[0].id).filter(tanggal=tanggal)
					a.update(keluar=waktu)
					print "Data Updated"
			else:
				print "Tidak ada data dengan user_id " + x['user_id']
		# msn = Mesin.objects.all()
		# for z in msn:
		#  	response = pyping.ping(z.ip, timeout=800, packet_size=10)
		#  	msn = Mesin.objects.select_for_update().filter(id=z.id)
		#  	if response.ret_code == 0:		    
		# 	    msn.update(status="UP", last_up = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), last_check = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') )
		#  	else:
		#  	    msn.update(status="DOWN", last_down = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), last_check = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') )

		#  	mesin = Mesin.objects.all()
		#  	conn = None
		#  	for m in mesin:
		#  		if m.status == "UP":
		#  			zk = ZK(m.ip, port=4370, timeout=5)
		#  			try:
		#  				conn = zk.connect()
		#  				#get the attendance
		#  				attendances = conn.get_attendance()
		#  			except Exception, e:
		#  			finally:
		#  				if conn:
		#  					conn.disconnect()