from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group
from django.db import models


# Create your models here.

class Profile(models.Model):
    name = models.CharField(max_length=500)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    college = models.CharField(max_length=500)


class Volunteer(models.Model):
    GROUP_NAME = "volunteer"
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='creator')

    @staticmethod
    def create(current_user, first_name, last_name, email, phone, password, group_name=None):
        user = User(first_name=first_name, last_name=last_name, email=email)
        user.password = make_password(password)
        user.save()
        user.groups.add(Group.objects.filter(name=group_name))
        v = Volunteer(user=user, phone=phone, created_by=current_user)
        v.save()
        return v


class EventVolunteer(Volunteer):
    GROUP_NAME = "event_volunteer"
    event = models.ForeignKey('Event', on_delete=models.CASCADE)

    @classmethod
    def create(cls, current_user, first_name, last_name, email, phone, password, event_id):
        user = User(first_name=first_name, last_name=last_name, email=email)
        user.password = make_password(password)
        user.save()
        user.groups.add(Group.objects.filter(name=EventVolunteer.GROUP_NAME))
        v = cls(user=user, phone=phone, created_by=current_user)
        v.event_id = event_id
        v.save()


class RituAdmin(Volunteer):
    GROUP_NAME = "admin_"

    class Meta:
        proxy = True

    @classmethod
    def create(cls, current_user, first_name, last_name, email, phone, password):
        r = Volunteer.create(current_user, first_name, last_name, email, phone, cls.GROUP_NAME)


class RegistrationDesk(Volunteer):
    GROUP_NAME = "registration_desk"

    class Meta:
        proxy = True

    @classmethod
    def create(cls, current_user, first_name, last_name, email, phone, password):
        r = Volunteer.create(current_user, first_name, last_name, email, phone, cls.GROUP_NAME)


class Head(Volunteer):
    GROUP_NAME = "dept_head"

    class Meta:
        proxy = True

    @classmethod
    def create(cls, current_user, first_name, last_name, email, phone, password):
        r = Volunteer.create(current_user, first_name, last_name, email, phone, cls.GROUP_NAME)


class Organizer(models.Model):
    name = models.CharField(max_length=255)
    head = models.OneToOneField(Head, on_delete=models.SET_NULL, null=True)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, unique=True)
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE)
    timing = models.DateTimeField(null=True)
    additional_data = models.TextField()
    amount = models.CharField(max_length=10, null=True)
    is_team_event = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Workshop(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10)
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE, null=True)
    timing = models.DateTimeField(null=True)
    amount = models.CharField(max_length=10, null=True)
    is_team_event = models.BooleanField(default=False)


class WorkshopRegistration(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)
    additional_data = models.TextField()
    registrar = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = (('profile', 'workshop'),)


class Registration(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    additional_data = models.TextField(null=True)
    registrar = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = (('profile', 'event'),)
