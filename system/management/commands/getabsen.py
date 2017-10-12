from django.core.management.base import BaseCommand, CommandError
from zk import ZK, const
from pprint import pprint
from system.models import Perusahaan, Karyawan, KaryawanShift, Absensi
 
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

		self.stdout.write("Koneksi ke mesin " + line)
		self.stdout.write("Tolong jangan melakukan finger ataupun pencabutan kabel jaringan")
		conn = None
		dataip = line.strip()
		dataip = dataip.split(";")
		ipmesin = dataip[0]
		zk = ZK(ipmesin, port=int(dataip[2]), timeout=5)
		try:
			print 'Koneksi ke Mesin ' + dataip[1] + ' dengan alamat IP ' + ipmesin
			conn = zk.connect()
			print 'Koneksi ke Mesin ' + dataip[1] + ' dengan alamat IP ' + ipmesin + ' berhasil'
			print 'Menon-aktifkan Mesin'
			conn.enable_device()
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

			#pprint(vars(attendances[12632]))
			MASUK = 0
			KELUAR = 1

			users = conn.get_users()
			for at in attendances:

				tanggal = at.timestamp.strftime("%Y-%m-%d")
				waktu = at.timestamp.strftime("%H:%M:%S")
				hari = at.timestamp.strftime("%A")
				kid = 1
				kw = 1
				print "Absen tanggal = " + at.timestamp.strftime("%d-%m-%Y %H:%M:%S")
				print "Status = " + ( "MASUK" if at.status == 0 else "KELUAR" )

				k = Karyawan.objects.filter(fingerid=at.user_id)
				if at.status == MASUK :
					if len(k) > 0:
						kid = k.id
						kw = KaryawanShift.objects.filter(karyawan_id=kid).filter(tgl_awal__gte=tanggal).filter(tgl_akhir__lte=tanggal)
						if len(kw) > 0:
							kw = kw.id
						else:
							kw = 1
					else:
						kid = 1
				
					masuk = waktu
					if kid != 1:
						a = Absensi(karyawan_id=kid, karyawanshift_id=kw, tanggal=tanggal, hari=hari, masuk = masuk)
					else:
						for usersi in users:					
							if usersi.user_id == at.user_id:
								print " ID : " + usersi.user_id + " Name : " + usersi.name
								a = Absensi(name=usersi.name, desc=usersi.user_id, karyawan_id=kid, karyawanshift_id=kw, tanggal=tanggal, hari=hari, masuk = masuk)
					a.save()
				else:
					keluar = waktu
					a = Absensi.objects.select_for_update().filter(tanggal = tanggal)
					a.update(keluar=keluar)

				for usersi in users:					
					if usersi.user_id == at.user_id:
						print " ID : " + usersi.user_id + " Name : " + usersi.name
						

						

			# for a in attendances:
			# 	pprint(vars(a))
			print "==================================================="
			print "Total Data Absen yang ditarik : " + str(len(attendances))
			print "User pada Mesin Absensi : " + str(len(users))
			print "==================================================="
			print "Pengambilan Data Absensi pada mesin "+ dataip[1] + " dengan alamat IP " + ipmesin + " berhasil"
			conn.test_voice()
			print 'Mengaktifkan kembali Mesin'
			conn.enable_device()
		except Exception, e:
		    print "Process terminate : {}".format(e)
		finally:
		    if conn:
		        conn.disconnect()