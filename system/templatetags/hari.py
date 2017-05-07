from django import template
from django.core.urlresolvers import reverse
import time

register = template.Library()

@register.simple_tag
def hari(day=None):
	if day=="Sun":
		return "Minggu"
	elif day=="Mon":
		return "Senin"
	elif day=="Tue":
		return "Selasa"
	elif day=="Wed":
		return "Rabu"
	elif day=="Thu":
		return "Kamis"
	elif day=="Fri":
		return "Jumat"
	elif day=="Sat":
		return "Sabtu"

@register.simple_tag
def waktu(waktu=None):
	return waktu

@register.simple_tag
def getSenin(date=None):
	return date