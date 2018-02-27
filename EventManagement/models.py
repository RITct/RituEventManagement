from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group
from django.db import models


# Create your models here.
from django.db.models import Max


class Profile(models.Model):
    name = models.CharField(max_length=500)
    email = models.EmailField()
    phone = models.CharField(max_length=15, unique=True)
    college = models.CharField(max_length=500)
    id_code = models.CharField(max_length=250)

    def save(self, *args,**kwargs):
        code = Profile.objects.all().aggregate(Max('id'))['id__max']
        self.id_code = "RITU" + str(code if code is not None else "00")
        return super(Profile,self).save()

    @property
    def serialize(self):
        return {
            'name':self.name,
            'email':self.email,
            'phone':self.phone,
            'college':self.college,
            'id_code':self.id_code
        }

    def __str__(self):
        return self.name


class Volunteer(models.Model):
    GROUP_NAME = "volunteer"
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username

    @staticmethod
    def create(username, first_name, last_name, email, phone, password, group_name=GROUP_NAME):
        user = User(username=username, first_name=first_name, last_name=last_name, email=email)
        user.password = make_password(password)
        user.save()
        user.groups.add(Group.objects.filter(name=group_name).first())
        v = Volunteer(user=user, phone=phone)
        v.save()
        return v


class EventVolunteer(Volunteer):
    GROUP_NAME = "event_volunteer"
    organizer = models.ForeignKey('Organizer', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    @classmethod
    def create(cls, username, first_name, last_name, email, phone, password, organizer):
        user = User(username=username, first_name=first_name, last_name=last_name, email=email)
        user.password = make_password(password)
        user.save()
        user.groups.add(Group.objects.filter(name=EventVolunteer.GROUP_NAME).first())
        v = cls(user=user, phone=phone)
        v.organizer = organizer
        v.save()


class RituAdmin(Volunteer):
    GROUP_NAME = "admin_"

    class Meta:
        proxy = True

    def __str__(self):
        return self.user.username

    @classmethod
    def create(cls, username, first_name, last_name, email, phone, password):
        r = Volunteer.create(username, first_name, last_name, email, phone, cls.GROUP_NAME)


class RegistrationDesk(Volunteer):
    GROUP_NAME = "registration_desk"

    class Meta:
        proxy = True

    def __str__(self):
        return self.user.username

    @classmethod
    def create(cls, username, first_name, last_name, email, phone, password):
        r = Volunteer.create(username, first_name, last_name, email, phone, password, cls.GROUP_NAME)


# class Head(Volunteer):
#     GROUP_NAME = "dept_head"
#
#     class Meta:
#         proxy = True
#
#     def __str__(self):
#         return self.user.username
#
#     @classmethod
#     def create(cls, username, first_name, last_name, email, phone, password):
#         r = Volunteer.create(username, first_name, last_name, email, phone, cls.GROUP_NAME)


class Organizer(models.Model):
    name = models.CharField(max_length=255)
    # head = models.OneToOneField(Head, on_delete=models.SET_NULL, null=True)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, unique=True)
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE)
    timing = models.CharField(max_length=250,null=True)
    additional_data = models.TextField()
    amount = models.CharField(max_length=10, null=True)
    is_team_event = models.BooleanField(default=False)
    venue = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class Workshop(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10)
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE, null=True)
    timing = models.DateTimeField(null=True)
    amount = models.CharField(max_length=10, null=True)
    is_team_event = models.BooleanField(default=False)
    venue = models.CharField(max_length=500)


    def __str__(self):
        return self.name


class WorkshopRegistration(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)
    additional_data = models.TextField()
    registrar = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = (('profile', 'workshop'),)

    def __str__(self):
        return self.profile.name + " | " + self.additional_data


class Registration(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    additional_data = models.TextField(null=True)
    registrar = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = (('profile', 'event'),)

    def __str__(self):
        return str(self.profile) + " | " + str(self.event) + ( " | " + self.additional_data if self.additional_data is not None else "")