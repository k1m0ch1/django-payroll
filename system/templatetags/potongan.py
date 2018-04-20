from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag
def sisa_cicil(pinjaman=None, banyak_cicil=None):
	hasil = pinjaman / banyak_cicil
	return hasil