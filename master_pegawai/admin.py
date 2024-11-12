from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

# Register your models here.
from . import models

admin.site.register(models.JabatanPegawaiModel)
admin.site.register(models.PangkatPegawaiModel)
admin.site.register(models.MasterPegawaiModel)