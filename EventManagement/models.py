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
    event = models.ForeignKey('Event', on_delete=models.CASCADE)


class Head(User):
    GROUP_NAME = "head"

    class Meta:
        proxy = True


class Organizer(models.Model):
    name = models.CharField(max_length=255)
    head = models.OneToOneField(Head, on_delete=models.SET_NULL, null=True)


class Event(models.Model):
    name = models.CharField(max_length=255)
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE)
    timing = models.DateTimeField()
    team_size = models.IntegerField(default=1)


class Registration(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('profile', 'event'))
