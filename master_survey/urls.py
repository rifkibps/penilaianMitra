from django.urls import path
from . import views

app_name = 'master_survei'

urlpatterns = [
    path('survei', views.MasterSurveiClassView.as_view(), name='index'),
    path('survei/json-response', views.SurveyJsonResponseClassView.as_view(), name='datatable-json'),
    path('survei/delete', views.MasterSurveyDeleteView.as_view(), name='delete-survey'),
    path('survei/detail', views.MasterSurveyDetailView.as_view(), name='detail-survey'),
    path('survei/update', views.MasterSurveyUpdateView.as_view(), name='update-survey'),
    path('survei/export', views.MasterSurveyExportView.as_view(), name='export-survey'),
    path('survei/upload', views.MasterSurveyUploadClassView.as_view(), name='upload-survey'),
    path('survei/template', views.MasterSurveyTemplateClassView.as_view(), name='template-survey'),

    path('kegiatan-survei', views.MasterKegiatanSurveiClassView.as_view(), name='kegiatan-survey'),
    path('kegiatan-survei/detail', views.MasterKegiatanSurveiDetailClassView.as_view(), name='detail-kegiatan'),
    path('kegiatan-survei/update', views.MasterKegiatanSurveiUpdateClassView.as_view(), name='update-kegiatan'),
    path('kegiatan-survei/delete', views.MasterKegiatanSurveiDeleteClassView.as_view(), name='delete-kegiatan'),
    path('kegiatan-survei/json-response', views.MasterKegiatanSurveiJsonClassView.as_view(), name='kegiatan-survey-json'),

]