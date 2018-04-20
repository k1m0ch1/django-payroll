from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag
def banyak_cicil(pinjaman=None, banyak_cicil=None):
	hasil = pinjaman / banyak_cicil
	money = str(int(hasil))
	i = 0
	hasil = "Rp. "
	y = len(str(money))
	for x in str(money):
		if y%3 == 0 and y != 1 and y != len(str(money)):
			hasil = hasil + "."
		hasil = hasil + x
		y = y - 1
	return hasil

@register.simple_tag
def sisa_cicil(pinjaman=None, banyak_cicil=None, sisa_cicil=None):
	hasil = (pinjaman / banyak_cicil) * sisa_cicil
	money = str(int(hasil))
	i = 0
	hasil = "Rp. "
	y = len(str(money))
	for x in str(money):
		if y%3 == 0 and y != 1 and y != len(str(money)):
			hasil = hasil + "."
		hasil = hasil + x
		y = y - 1
	return hasil