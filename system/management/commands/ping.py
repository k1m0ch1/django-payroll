from django.core.management.base import BaseCommand, CommandError
from zk import ZK, const
from pprint import pprint
from system.models import Perusahaan, Karyawan
 
class Command(BaseCommand):
  args = 'Arguments is not needed'
  help = 'Django admin custom command poc.'
 
  def handle(self, *args, **options):

  	class mesin(object):
  		no = 0
  		ipmesin = ""
  		namamesin = ""
  		status = ""
  		portmesin = 0

  		def __init__(self, no, ipmesin, namamesin, status, portmesin):

  			self.no = no
  			self.ipmesin = ipmesin
  			self.namamesin = namamesin
  			self.status = status
  			self.portmesin = portmesin

	files = open("listip.txt", "r")
	objs = [range(sum(1 for xx in open("listip.txt")))]
	y=0
	for line in files:
		# p = Perusahaan.objects.filter(pk=1)
		# for pa in p:
		# 	print pa.name

		#print len(Karyawan.objects.all())
		conn = None
		dataip = line.strip()
		dataip = dataip.split(";")
		ipmesin = dataip[0]
		zk = ZK(ipmesin, port=int(dataip[2]), timeout=5)
		try:
			y = y +1
			print '[*]  Koneksi ke Mesin ' + dataip[1] + ' dengan alamat IP ' + ipmesin
			self.stdout.write("[!]  Tolong jangan melakukan finger ataupun pencabutan kabel jaringan")
			conn = zk.connect()
			print '[*]  Koneksi ke Mesin ' + dataip[1] + ' dengan alamat IP ' + ipmesin + ' BERHASIL'
			conn.test_voice()
			objs.append(mesin(y, ipmesin, dataip[1], "UP", dataip[2]))
		except Exception, e:
			print "===ERROR LOG==="
			print "[!!] " + dataip[1] + " dengan alamat IP " + ipmesin + " dengan error = " + format(e)
			print "==============="
			print '[*]  Koneksi ke Mesin ' + dataip[1] + ' dengan alamat IP ' + ipmesin + ' GAGAL'
			objs.append(mesin(y, ipmesin, dataip[1], "DOWN", dataip[2]))
		finally:
		    if conn:
		        conn.disconnect()

	objs.pop(0)

	print " "
	print "=== LISTING MESIN ==="

	for ob in objs:
		print " [+] " + ob.namamesin + " dengan IP " + ob.ipmesin + ":" +  ob.portmesin + " " + ob.status

	print "====================="
