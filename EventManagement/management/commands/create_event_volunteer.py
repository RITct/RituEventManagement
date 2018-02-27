from django.core.management import BaseCommand

from EventManagement.models import RegistrationDesk, EventVolunteer, Organizer


class Command(BaseCommand):
    help = 'Initialize Database with event details'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Creating Registration Desk\n'))
        first_name = str(input('First Name'))
        last_name = str(input('Last Name'))
        email = str(input('Email'))
        username = str(input('username'))
        password = str(input('Password'))
        phone = str(input('Phone'))
        org = str(input('Dept'))
        r = EventVolunteer.create(username, first_name, last_name, email, phone,password, Organizer.objects.get(code=org))