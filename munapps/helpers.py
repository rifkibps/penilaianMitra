import numpy as np
import locale

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