from django.conf.urls import url

import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.loginpage,  name="loginpage"),
    url(r'^loginrequest$', views.loginrequest, name='loginrequest'),
    url(r'^logout$', views.logout_view,  name="logout"),
    url(r'^perusahaan$', views.dashboard.perusahaan_index,  name="perusahaan-index"),
    url(r'^department$', views.dashboard.department_index,  name="department-index"),
    url(r'^perusahaan/(?P<perusahaan_id>[0-9]+)/delete/$', views.perusahaan_delete, name="perusahaan-delete"),
    url(r'^perusahaan/(?P<perusahaan_id>[0-9]+)/edit/$', views.perusahaan_edit, name="perusahaan-edit"),
    url(r'^department/(?P<department_id>[0-9]+)/delete/$', views.department_delete, name="department-delete"),
    url(r'^department/(?P<department_id>[0-9]+)/edit/$', views.department_edit, name="department-edit"),
]