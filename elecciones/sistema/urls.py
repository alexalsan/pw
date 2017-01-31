from django.conf.urls import include, url
from django.contrib import admin

from sistema.views import (
	sistema_list,
	CircList,
	CircDetail,
	CircCreate,
	CircUpdate,
	CircDelete,
	mesa_list,
	mesa_create,
	mesa_detail,
	mesa_update,
)

urlpatterns = [
	url(r'^$', sistema_list, name='home'),

	url(r'^circ/$', CircList.as_view(), name='circ_list'),
	url(r'^circ/(?P<pk>\d+)/$', CircDetail.as_view(), name='circ_detail'),
	url(r'^circ/create/$', CircCreate.as_view(), name='circ_create'),
	url(r'^circ/(?P<pk>\d+)/update/$', CircUpdate.as_view(), name='circ_update'),
	url(r'^circ/(?P<pk>\d+)/delete/$', CircDelete.as_view(), name='circ_delete'),

	url(r'^circ/(?P<id>\d+)/mesas/$', mesa_list, name='mesa_list'),
	url(r'^circ/(?P<id>\d+)/mesas/create/$', mesa_create, name='mesa_create'),
	url(r'^mesas/(?P<id>\d+)/$', mesa_detail, name='mesa_detail'),
	url(r'^mesas/(?P<id>\d+)/update/$', mesa_update, name='mesa_update'),
]