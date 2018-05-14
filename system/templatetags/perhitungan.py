from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag
def banyak_cicil():
	return "aw"
