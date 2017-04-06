from django.conf.urls import url

import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.loginpage,  name="loginpage"),
    url(r'^loginrequest$', views.loginrequest, name='loginrequest'),
    url(r'^logout$', views.logout_view,  name="logout"),

    url(r'^perusahaan$', views.dashboard.perusahaan_index,  name="perusahaan-index"),
    url(r'^department$', views.dashboard.department_index,  name="department-index"),
    #url(r'^unit$', views.dashboard.unit_index, name="unit-index"),
  	url(r'^bagian$', views.dashboard.bagian_index, name="bagian-index"),
  	url(r'^golongan$', views.dashboard.golongan_index, name="golongan-index"),
  	url(r'^jabatan$', views.dashboard.jabatan_index, name="jabatan-index"),
  	url(r'^bank$', views.dashboard.bank_index, name="bank-index"),
  	url(r'^agama$', views.dashboard.agama_index, name="agama-index"),
  	url(r'^warganegara$', views.dashboard.warganegara_index, name="warganegara-index"),
  	url(r'^statusmenikah$', views.dashboard.statusmenikah_index, name="statusmenikah-index"),
  	#url(r'^notif-system$', views.dashboard.notif_system, name="notif-system-index"),
  	#url(r'^notif-login$', views.dashboard.notif_login, name="notif-login-index"),
  	#url(r'^notif-aplikasi$', views.dashboard.notif_aplikasi, name="notif-aplikasi-index"),
  	#url(r'^notif-karyawan$', views.dashboard.notif_karyawan, name="notif-karyawans-index"),
  	#url(r'^notif-system$', views.dashboard.notif_system, name="notif-system-index"),

  	#url(r'^perusahaan$', views.dashboard.perusahaan_index,  name="perusahaan-index"),
    url(r'^department/create$', views.create.department,  name="department-create"),
    url(r'^department/create/save$', views.create.department_save,  name="department-create-save"),
    url(r'^bagian/create$', views.create.bagian,  name="bagian-create"),
    url(r'^bagian/create/save$', views.create.bagian_save,  name="bagian-create-save"),
  	#url(r'^golongan/create$', views.dashboard.golongan, name="golongan-create"),
  	#url(r'^jabatan/create$', views.dashboard.jabatan, name="jabatan-create"),
  	#url(r'^bank/create$', views.dashboard.bank, name="bank-create"),
  	#url(r'^agama/create$', views.dashboard.agama, name="agama-create"),
  	#url(r'^warganegara/create$', views.dashboard.warganegara, name="warganegara-create"),
  	#url(r'^statusmenikah/create$', views.dashboard.statusmenikah, name="statusmenikah-create"),

  	url(r'^department/(?P<department_id>[0-9]+)/edit/$', views.edit.department, name="department-edit"),
  	url(r'^department/(?P<department_id>[0-9]+)/edit/save$', views.edit.department_save, name="department-edit-save"),
  	url(r'^bagian/(?P<bagian_id>[0-9]+)/edit/$', views.edit.bagian, name="bagian-edit"),
  	url(r'^bagian/(?P<bagian_id>[0-9]+)/edit/save$', views.edit.bagian_save, name="bagian-edit-save"),

    url(r'^perusahaan/(?P<perusahaan_id>[0-9]+)/delete/$', views.perusahaan_delete, name="perusahaan-delete"),
    url(r'^department/(?P<department_id>[0-9]+)/delete/$', views.delete.department, name="department-delete"),
    url(r'^bagian/(?P<bagian_id>[0-9]+)/delete/$', views.delete.bagian, name="bagian-delete")
]