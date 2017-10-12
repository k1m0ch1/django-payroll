from django.core.management.base import BaseCommand, CommandError
from zk import ZK, const
from pprint import pprint
from system.models import Perusahaan, Karyawan, KaryawanShift
 
class Command(BaseCommand):

  help = 'Django admin custom command poc.'

  def add_arguments(self, parser):
  	parser.add_argument('fingerid', type=int)
  	parser.add_argument('nama', type=str)
 
  def handle(self, *args, **options):
    print options['nama']