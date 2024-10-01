from django.urls import path
from . import views

app_name = 'master_honor'

urlpatterns = [
    path('manajemen-honor', views.MasterHonorClassView.as_view(), name='index'),

    path('manajemen-honor/constrain-salary', views.MasterConstSalarytGetClassView.as_view(), name='get-const-salary'),
    path('manajemen-honor/settings', views.MasterHonorSettingClassView.as_view(), name='honor-settings'),
    path('manajemen-honor/update', views.MasterConstHonorSettingUpdateView.as_view(), name='update-const'),
    path('manajemen-honor/delete', views.MasterConstSalaryDeleteView.as_view(), name='delete-const'),
    
    path('manajemen-honor/json-response', views.MasterHonorJsonResponseClassView.as_view(), name='json-response'),
]