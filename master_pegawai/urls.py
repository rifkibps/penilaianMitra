from django.urls import path
from . import views

app_name = 'master_pegawai'

urlpatterns = [
    path('master-pegawai', views.MasterPegawaiClassView.as_view(), name='index'),
    path('master-pegawai/update', views.MasterPegawaiUpdateClassView.as_view(), name='update'),
    path('master-pegawai/delete', views.MasterPegawaiDeleteClassView.as_view(), name='delete'),
    path('master-pegawai/detail', views.MasterPegawaiDetailClassView.as_view(), name='detail'),
    path('master-pegawai/json-response', views.MasterPegawaiJsonResponseClassView.as_view(), name='datatable-json'),

    path('jabatan', views.PositionsClassView.as_view(), name='jabatan'),
    path('jabatan/json-response', views.MasterPositionJsonResponseClassView.as_view(), name='position-datatable-json'),
    path('jabatan/detail', views.MasterPositionDetailClassView.as_view(), name='position-detail'),
    path('jabatan/update', views.MasterPositionUpdateClassView.as_view(), name='position-update'),
    path('jabatan/delete', views.MasterPositionDeleteClassView.as_view(), name='position-delete'),

    path('pangkat', views.PangkatClassView.as_view(), name='pangkat'),
    path('pangkat/json-response', views.MasterPangkatJsonResponseClassView.as_view(), name='pangkat-datatable-json'),
    path('pangkat/detail', views.MasterPangkatDetailClassView.as_view(), name='pangkat-detail'),
    path('pangkat/update', views.MasterPangkatUpdateClassView.as_view(), name='pangkat-update'),
    path('pangkat/delete', views.MasterPangkatDeleteClassView.as_view(), name='pangkat-delete'),

]