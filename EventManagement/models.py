from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    college = models.CharField(max_length=500)
    qr_id = models.CharField(max_length=10)


class Volunteer(models.Model):
    GROUP_NAME = "volunteer"
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class EventVolunteer(Volunteer):
    GROUP_NAME = "event_volunteer"
    event = models.ForeignKey('Event', on_delete=models.CASCADE)


class RegistrationDesk(Volunteer):
    GROUP_NAME = "registration_desk"

    class Meta:
        proxy = True


class Head(User):
    GROUP_NAME = "dept_head"

    class Meta:
        proxy = True


class Organizer(models.Model):
    name = models.CharField(max_length=255)
    head = models.OneToOneField(Head, on_delete=models.SET_NULL, null=True)
    code = models.CharField(max_length=10)


class Event(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10)
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE)
    timing = models.DateTimeField()
    is_team_event = models.BooleanField(default=False)
    additional_data = models.TextField()


class TeamRegistration(models.Model):
    team_name = models.CharField(max_length=250)


class Registration(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    team = models.ForeignKey(TeamRegistration, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = (('profile', 'event'),('profile','team'))
