from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.assignment_tag
def define(val=None):
  return val

@register.simple_tag
def dashboard(module=None, mode=None, idpk=None):
  if module == "Bagian/ Division":
  	return{
  		'indeks' : reverse('bagian-index'),
  		'tambah' : reverse('bagian-create'),
  		'ubah'	 : reverse('bagian-edit', kwargs={'bagian_id': idpk}),
  		'hapus'	 : reverse('bagian-delete', kwargs={'bagian_id': idpk})
  	}[mode]
    
  return "null"