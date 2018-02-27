from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError

from EventManagement.models import *

from event_details import *


class Command(BaseCommand):
    help = 'Initialize Database with event details'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Creating Event Volunteer\n'))
        first_name = str(input('First Name'))
        last_name = str(input('Last Name'))
        email = str(input('Email'))
        username = str(input('username'))
        password = str(input('Password'))
        phone = str(input('Phone'))
        r = RegistrationDesk.create(username, first_name, last_name, email, phone,password)
