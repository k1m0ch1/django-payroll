from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag
def mon(money=None):
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
def ez(angka=None):
	i = 0
	hasil = ""
	for x in str(angka):
		if i%4 == 0 and i != 0:
			hasil =  hasil + " "
		hasil = hasil + x
		i = i + 1
	return hasil

@register.simple_tag
def gajipokok(angka=None):
	money=int(float(angka) * float(0.75))
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
def tunjangan(angka=None):
	money=int(float(angka) * float(0.25))
	i = 0
	hasil = "Rp. "
	y = len(str(money))
	for x in str(money):
		if y%3 == 0 and y != 1 and y != len(str(money)):
			hasil = hasil + "."
		hasil = hasil + x
		y = y - 1
	return hasil