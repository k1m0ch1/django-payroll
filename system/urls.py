from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.loginpage,  name="loginpage"),
    url(r'^loginrequest$', views.loginrequest, name='loginrequest'),
]
