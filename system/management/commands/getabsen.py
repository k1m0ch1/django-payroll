from django.core.management.base import BaseCommand, CommandError
from zk import ZK, const
from pprint import pprint
from system.models import Perusahaan, Karyawan
 
class Command(BaseCommand):
  args = 'Arguments is not needed'
  help = 'Django admin custom command poc.'
 
  def handle(self, *args, **options):
    self.stdout.write("Hello World")
    file = open("listip.txt", "r")
    for line in file:
		# p = Perusahaan.objects.filter(pk=1)
		# for pa in p:
		# 	print pa.name

		#print len(Karyawan.objects.all())

		self.stdout.write("Koneksi ke mesin " + line)
		self.stdout.write("Tolong jangan melakukan finger ataupun pencabutan kabel jaringan")
		conn = None
		dataip = line.strip()
		dataip = dataip.split(";")
		ipmesin = dataip[0]
		zk = ZK(ipmesin, port=4370, timeout=5)
		try:
			print 'Koneksi ke Mesin ' + dataip[1] + ' dengan alamat IP ' + ipmesin
			conn = zk.connect()
			print 'Koneksi ke Mesin ' + dataip[1] + ' dengan alamat IP ' + ipmesin + ' berhasil'
			print 'Menon-aktifkan Mesin'
			conn.disable_device()
			print 'Firmware Version: : {}'.format(conn.get_firmware_version())
			# print '--- Get User ---'
			print "================================================================================================"
			print "Sedang mengambil data absensi pada mesin "+ dataip[1] + " dengan alamat IP " + ipmesin
			print ""
			print "!!!Tolong jangan melakukan finger ataupun pencabutan kabel jaringan!!!"
			print "================================================================================================"
			attendances = conn.get_attendance()

			# Create user
			#conn.set_user(uid=99, name='Yahya F. Al Fatih', privilege=const.USER_DEFAULT, password='12345678', group_id='', user_id='112233')
			# Get all users (will return list of User object)
			#users = conn.get_users()

			pprint(vars(attendances[0]))
			# for a in attendances:
			# 	pprint(vars(a))

			print "Pengambilan Data Absensi pada mesin "+ dataip[1] + " dengan alamat IP " + ipmesin + " berhasil"
			conn.test_voice()
			print 'Mengaktifkan kembali Mesin'
			conn.enable_device()
		except Exception, e:
		    print "Process terminate : {}".format(e)
		finally:
		    if conn:
		        conn.disconnect()