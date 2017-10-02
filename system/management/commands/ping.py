from django.core.management.base import BaseCommand, CommandError
from zk import ZK, const
from pprint import pprint
from system.models import Perusahaan, Karyawan
 
class Command(BaseCommand):
  args = 'Arguments is not needed'
  help = 'Django admin custom command poc.'
 
  def handle(self, *args, **options):
    file = open("listip.txt", "r")
    for line in file:
		# p = Perusahaan.objects.filter(pk=1)
		# for pa in p:
		# 	print pa.name

		#print len(Karyawan.objects.all())
		conn = None
		dataip = line.strip()
		dataip = dataip.split(";")
		ipmesin = dataip[0]
		zk = ZK(ipmesin, port=4370, timeout=5)
		try:
			print '[*]  Koneksi ke Mesin ' + dataip[1] + ' dengan alamat IP ' + ipmesin
			self.stdout.write("[!]  Tolong jangan melakukan finger ataupun pencabutan kabel jaringan")
			conn = zk.connect()
			print '[*]  Koneksi ke Mesin ' + dataip[1] + ' dengan alamat IP ' + ipmesin + ' BERHASIL'
			conn.test_voice()
		except Exception, e:
			print "===ERROR LOG==="
			print "[!!] " + dataip[1] + " dengan alamat IP " + ipmesin + " dengan error = " + format(e)
			print "==============="
			print '[*]  Koneksi ke Mesin ' + dataip[1] + ' dengan alamat IP ' + ipmesin + ' GAGAL'
		finally:
		    if conn:
		        conn.disconnect()