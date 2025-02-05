import numpy as np
import locale
from django.db.models.functions import Length

# Helpers
def get_rows_table(rows):
    n_row = np.quantile(np.arange(1, rows), [.25, .5, .75, ])
    return np.append(np.unique(np.rint(n_row).astype(int)).astype(str), ['All'])

def currency_formatting(nominal,with_prefix=False, decimal=2):
    locale.setlocale(locale.LC_NUMERIC, 'IND')
    rp = locale.format_string("%.*f", (decimal, nominal), True)
    if with_prefix:
         return "Rp{}".format(rp)
    return rp

def restrict_datatable_actions(request):
    if ((request.user.is_superuser) and (request.user.is_staff) and ('Administrator' in request.user.groups.all().values_list('name', flat=True))) is False:  # If the user is a standard user,
        return True
    
def get_adm_levels(model_adm):
        adm = model_adm.objects.annotate(text_len=Length('code'))
        adm = {
                'prov' : adm.filter(text_len=2).order_by('region'),
                'kabkot' : adm.filter(text_len=4).order_by('region'),
                'kec' : adm.filter(text_len=7).order_by('region'),
                'desa' : adm.filter(text_len=10).order_by('region'),
            }
        return adm