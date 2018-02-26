from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError

from EventManagement.models import *

from event_details import *


class Command(BaseCommand):
    help = 'Initialize Database with event details'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Adding Events\n'))
        for i in EVENT_DETAILS:
            print(i)
            k = Organizer()
            k.code = i
            k.name = EVENT_DETAILS[i]['name']
            try:
                k.save()
            except:pass

        for i in EVENT_DETAILS:
            for k in EVENT_DETAILS[i]['events']:
                print(EVENT_DETAILS[i]['events'][k]['code'])
                e = Event()
                e.code = EVENT_DETAILS[i]['events'][k]['code']
                e.name = EVENT_DETAILS[i]['events'][k]['name']
                e.organizer = Organizer.objects.get(code=i)
                try:
                    e.save()
                except IntegrityError as er:
                    pass
        self.stdout.write(self.style.SUCCESS('Added all Events\n'))
        for i in WORKSHOP_EVENTS:
            e = Workshop()
            e.code = WORKSHOP_EVENTS[i]['code']
            e.name = WORKSHOP_EVENTS[i]['name']
            e.save()
        self.stdout.write(self.style.SUCCESS('Added all Workshops\n'))

        self.stdout.write(self.style.NOTICE('Creating groups'))

        Group(name=Volunteer.GROUP_NAME).save()
        Group(name=EventVolunteer.GROUP_NAME).save()
        Group(name=RegistrationDesk.GROUP_NAME).save()
        Group(name=RituAdmin.GROUP_NAME).save()
