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

	def handle(self, *args, **options):
		msn = Mesin.objects.all()
		for z in msn:
		 	response = pyping.ping(z.ip, timeout=800, packet_size=10)
		 	msn = Mesin.objects.select_for_update().filter(id=z.id)
		 	if response.ret_code == 0:		    
			    msn.update(status="UP", last_up = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), last_check = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') )
		 	else:
		 	    msn.update(status="DOWN", last_down = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), last_check = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') )

		 	mesin = Mesin.objects.all()
		 	conn = None
		 	for m in mesin:
		 		if m.status == "UP":
		 			zk = ZK(m.ip, port=4370, timeout=5)
		 			try:
		 				conn = zk.connect()
		 				#get the attendance
		 				attendances = conn.get_attendance()
		 			except Exception, e:
		 			finally:
		 				if conn:
		 					conn.disconnect()