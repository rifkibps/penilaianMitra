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