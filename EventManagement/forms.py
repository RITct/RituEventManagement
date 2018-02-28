from django import forms

from EventManagement.models import Profile, Event, Workshop


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['id_code']


class EventForm(forms.ModelForm):
    additional_data = forms.CharField(required=False)

    class Meta:
        model = Event
        fields = ['additional_data', 'timing', 'venue']

class WorkshopForm(forms.ModelForm):
    additional_data = forms.CharField(required=False)

    class Meta:
        model = Workshop
        fields = ['additional_data', 'timing', 'venue']