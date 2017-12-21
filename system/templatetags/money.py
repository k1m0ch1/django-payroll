from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag
def mon(money=None):
	i = 0
	hasil = "Rp. "
	for x in str(money):
		if i%3 == 1 and i != 0:
			hasil =  hasil + "."
		hasil = hasil + x
		i = i + 1
	return hasil