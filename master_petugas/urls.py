from django.urls import path
from . import views

app_name = 'master_petugas'

urlpatterns = [
    path('master-petugas', views.MasterPetugasClassView.as_view(), name='index'),
    path('master-petugas/json-response', views.MasterPetugasJsonResponseClassView.as_view(), name='datatable-json'),
    path('master-petugas/delete', views.MasterPetugasDeleteView.as_view(), name='delete-petugas'),
    path('master-petugas/detail', views.MasterPetugasDetailView.as_view(), name='detail'),
    path('master-petugas/update', views.MasterPetugasUpdateView.as_view(), name='update'),
    path('master-petugas/upload', views.MasterPetugasUploadClassView.as_view(), name="upload-petugas"),
    path('master-petugas/export', views.MasterPetugasExportClassView.as_view(), name="mitra-export"),
    path('master-petugas/template/<int:rows>', views.MasterPetugasTemplateClassView.as_view(), name="mitra-template"),
    path('master-petugas/view-petugas/<int:mitra_id>', views.MasterPetugasDetailViewClassView.as_view(), name="mitra-view-detail"),
    path('master-petugas/search', views.MasterPetugasSearchClassView.as_view(), name="mitra-search"),

    path('alokasi-petugas', views.AlokasiPetugasClassView.as_view(), name='alokasi'),
    path('alokasi-petugas/json-response', views.MasterAlokasiJsonResponseClassView.as_view(), name='datatable-json-alok'),
    path('alokasi-petugas/delete', views.AlokasiPetugasDeleteView.as_view(), name='delete-alokasi'),
    path('alokasi-petugas/detail', views.MasterAlokasiDetailView.as_view(), name='detail-alokasi'),
    path('alokasi-petugas/update', views.MasterAlokasiUpdateView.as_view(), name='update-alokasi'),
    path('alokasi-petugas/export', views.MasterAlokasiExportClassView.as_view(), name='export-alokasi'),
    path('alokasi-petugas/upload', views.MasterAlokasiUploadClassView.as_view(), name="upload-alokasi"),
    path('alokasi-petugas/template', views.MasterAlokasiTemplateClassView.as_view(), name="template-alokasi"),
    path('alokasi-penugasan', views.AlokasiPenugasanClassView.as_view(), name='penugasan'),
    
    path('role-petugas', views.RolePetugasClassView.as_view(), name='role'),
    path('role-petugas/json-response', views.MasterRoleJsonResponseClassView.as_view(), name='datatable-json-role'),
    path('role-petugas/delete', views.RolePetugasDeleteView.as_view(), name='delete-role'),
    path('role-petugas/detail', views.MasterRoleDetailView.as_view(), name='detail-role'),
    path('role-petugas/update', views.MasterRoleUpdateView.as_view(), name='update-role'),
    path('role-petugas/export', views.MasterRoleExportClassView.as_view(), name='export-role'),

    path('petugas', views.PetugasClassView.as_view(), name='petugas'),
    path('petugas/preview/<int:mitra_id>', views.DetailPetugasPreviewClassView.as_view(), name='detail-petugas'),
    path('petugas/json-response', views.ListPetugasClassView.as_view(), name='list-petugas-json'),
]