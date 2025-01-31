from django.urls import reverse
from django.shortcuts import redirect
from django.http import HttpResponseForbidden

class RestrictionsAccess(object):
    """
    Mixin allows you to require a user with `is_superuser` || `is_staff` || `is_administrations groups` set to True.
    """
    def dispatch(self, request, *args, **kwargs):
        if ((request.user.is_superuser) and (request.user.is_staff) and ('Administrator' in request.user.groups.all().values_list('name', flat=True))) is False:  # If the user is a standard user,
            # return HttpResponseForbidden("You do not have permission to access this resource.")
            return redirect(reverse('dashboard:index'))

        return super(RestrictionsAccess, self).dispatch(request, *args, **kwargs)

class RestrictionsHttpRequestAccess(object):
    """
    Mixin allows you to require a user with `is_superuser` || `is_staff` || `is_administrations groups` set to True.
    """
    def dispatch(self, request, *args, **kwargs):
        if ((request.user.is_superuser) and (request.user.is_staff) and ('Administrator' in request.user.groups.all().values_list('name', flat=True))) is False:  # If the user is a standard user,
            return HttpResponseForbidden("You do not have permission to access this resource.")

        return super(RestrictionsHttpRequestAccess, self).dispatch(request, *args, **kwargs)
