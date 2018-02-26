from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.views import View
from django.views.decorators.http import require_http_methods

from EventManagement.celery import send_email
from EventManagement.forms import ProfileForm, EventForm
from EventManagement.utils import belongs_to_group, group_login_required
from EventManagement.models import *


def index(request):
    if request.user.is_authenticated:
        return redirect('admin_panel')
    return render(request, 'EventManagement/sign_in.html')


def logout_user(request):
    logout(request)
    return redirect('index')


@login_required
def admin_panel(request):
    context = {'event_list': Event.objects.all(), 'workshop_list': Workshop.objects.all(), 'user': request.user}
    if belongs_to_group(request.user, EventVolunteer.GROUP_NAME):
        event_volunteer = EventVolunteer.objects.get(user=request.user)
        context['event_volunteer'] = event_volunteer
        org_events = Event.objects.filter(organizer=event_volunteer.organizer)
        context['registrations'] = []
        for i, event in enumerate(org_events):
            context['registrations'].append({
                'code': event.code,
                'name': event.name,
                'list': []
            })
            registrations = Registration.objects.filter(event=event)
            for reg in registrations:
                context['registrations'][i]['list'].append({
                    'profile': reg.profile.serialize,
                    'additonal_data': reg.additional_data,
                })
        return render(request, 'EventManagement/event_volunteer_admin.html', context)
    elif belongs_to_group(request.user, RegistrationDesk.GROUP_NAME):
        event_volunteer = RegistrationDesk.objects.get(user=request.user)
        context['event_volunteer'] = event_volunteer
        context['p_form'] = ProfileForm()
        return render(request, 'EventManagement/event_volunteer_admin.html', context)
    elif belongs_to_group(request.user, RituAdmin.GROUP_NAME):
        context['admin'] = RituAdmin.objects.get(user=request.user)

        return render(request, "EventManagement/ritu_admin_admin.html", context)
    else:
        raise PermissionDenied("Not a authorized to view the page")


@require_http_methods(["POST"])
@group_login_required(group_name=RegistrationDesk.GROUP_NAME)
def add_profile(request):
    print('')
    form = ProfileForm(request.POST)
    context = {'event_list': [], 'workshop_list': []}
    if form.is_valid():
        profile = form.save()
        events = Event.objects.all()
        for event in events:
            if event.code in request.POST:
                r = Registration()
                r.event = event
                r.registrar = request.user
                r.profile = profile
                if event.is_team_event:
                    r.additional_data = request.POST[event.code + "_additional"]
                r.save()
                context['event_list'].append(event.name)
        workshops = Workshop.objects.all()
        for workshop in workshops:
            if workshop.code in request.POST:
                r = WorkshopRegistration()
                r.workshop = workshop
                r.registrar = request.user
                r.profile = profile
                if event.is_team_event:
                    r.additional_data = request.POST[event.code + "_additional"]
                r.save()
                context['workshop_list'].append(workshop.name)
        send_email.delay(profile.serialize, context)
        return redirect('admin_panel')
    print(form.errors)
    return render(request, "EventManagement/event_volunteer_admin.html", {'p_form': form,
                                                                          'event_list': Event.objects.all(),
                                                                          'workshop_list': Workshop.objects.all()})


class UpdateEvent(View):
    def get(self, request, event_code):
        if not belongs_to_group(request.user, EventVolunteer.GROUP_NAME):
            raise PermissionDenied()
        event = get_object_or_404(Event, code=event_code)
        form = EventForm(instance=event)
        return render(request, 'EventManagement/update_event.html', {'form': form, 'user': request.user})

    def post(self, request, event_code):
        if not belongs_to_group(request.user, EventVolunteer.GROUP_NAME):
            raise PermissionDenied()
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        return render(request, 'EventManagement/update_event.html', {'form': form, 'user': request.user})


#####################################################
def get_event_data(request):
    event_details = Event.objects.all()
    workshop_details = Workshop.objects.all()
    data = {
        'events': [],
        'workshops': []
    }
    for event in event_details:
        data['events'].append({
            "code": event.code,
            'name': event.name,
            'time': event.timing,
            'organiser': event.organizer.name,
            'amount': event.amount,
            'additional': event.additional_data,
            'is_team': event.is_team_event,
            'venue': event.venue,
        })
    for event in workshop_details:
        data['workshops'].append({
            "code": event.code,
            'name': event.name,
            'time': event.timing,
            'organiser': event.organizer.name if event.organizer is not None else "",
            'amount': event.amount,
            'is_team': event.is_team_event,
            "venue": event.venue
        })
    return JsonResponse(data=data)


def get_user_data(request):
    data = {
        'name': "test",
        'college': "RIT",
        'phone': '999999999',
        'email': 'test@test.com',
        'registrations': {
            'events': [
                {
                    'code': "CSE01",
                },
                {
                    'code': "CSE02"
                }
            ],
            'workshops': [
                {
                    'code': "CSEW01",
                },
                {
                    'code': "CSEW02"
                }
            ]
        }
    }
    return JsonResponse(data)
