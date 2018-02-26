from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.http import require_http_methods

from EventManagement.forms import AddEventVolunteerForm, ProfileForm
from EventManagement.utils import belongs_to_group, group_login_required
from EventManagement.models import *


def index(request):
    if request.user is not None:
        return redirect('admin')
    return render(request, 'EventManagement/sign_in.html')


@login_required
def admin_panel(request):
    context = {'event_list': Event.objects.all(), 'workshop_list': Workshop.objects.all()}
    if belongs_to_group(request.user, Volunteer.GROUP_NAME):
        render(request, 'EventManagement/volunteer_admin.html', context)
    elif belongs_to_group(request.user, EventVolunteer.GROUP_NAME):
        event_volunteer = EventVolunteer.objects.get(user=request.user)
        context['event_volunteer'] = event_volunteer
        render(request, 'EventManagement/event_volunteer_admin.html', context)
    elif belongs_to_group(request.user, Head.GROUP_NAME):
        context['head'] = Head.objects.get(user=request.user)
        render(request, "EventManagement/head_admin.html", context)
    elif belongs_to_group(request.user, RituAdmin.GROUP_NAME):
        context['admin'] = RituAdmin.objects.get(user=request.user)
        render(request, "EventManagement/ritu_admin_admin.html", context)
    else:
        raise PermissionDenied("Not a authorized to view the page")


#@require_http_methods(["POST"])
#@group_login_required(group_name=Head.GROUP_NAME)
def head_event_volunteer_add(request):
    form = AddEventVolunteerForm(request.POST)
    head = Head.objects.filter(user=request.user).select_related().first()
    if form.is_valid():
        event_volunteer = EventVolunteer.create(current_user=request.user,
                                                first_name=form.cleaned_data['first_name'],
                                                last_name=form.cleaned_data['last_name'],
                                                email=form.cleaned_data['email'],
                                                phone=form.cleaned_data['phone'],
                                                password=form.cleaned_data['password'],
                                                event_id=form.cleaned_data['event']
                                                )
        return redirect('admin')
    return render(request, "EventManagement/head_admin.html", {'form': form})


# @require_http_methods(["POST"])
# @group_login_required(group_name=Head.GROUP_NAME)
def add_profile(request):
    form = ProfileForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('admin')
    return render(request, "EventManagement/head_admin.html", {'form': form})


