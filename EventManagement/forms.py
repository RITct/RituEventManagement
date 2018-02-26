from django import forms

from EventManagement.models import Profile, Event, Workshop


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['id_code']


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['code']