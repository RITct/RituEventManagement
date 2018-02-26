from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render

from EventManagement.models import *


def belongs_to_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


def group_login_required(group_name):
    def real_decorator(function):
        @login_required
        def wrapper(request):
            if not belongs_to_group(request.user, group_name):
                raise PermissionDenied()
            return function(request)

        return wrapper
    return real_decorator

