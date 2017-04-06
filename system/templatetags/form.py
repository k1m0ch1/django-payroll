from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag
def form(module=None, mode=None, idpk=None):
	if module == "Bagian/ Division":
		return{
			'Tambah' : reverse('bagian-create-save'),
			'Ubah'   : reverse('bagian-edit-save', kwargs={'bagian_id': idpk})
		}[mode]
		
	return "null"