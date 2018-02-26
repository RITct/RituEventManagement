from django import forms

from EventManagement.models import Profile, Event, Workshop


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['id_code']


class AddEventVolunteerForm(forms.Form):
    def __init__(self, organizer, *args, **kwargs):
        super().__init__(args, kwargs)
        self.fields['event'].query_set = Event.objects.filter(organizer=organizer)

    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.CharField()
    password = forms.CharField()
    phone = forms.CharField()
    event = forms.ModelChoiceField(queryset=Event.objects.all())


class AddRegistrationDesk(forms.Form):
    first_name = forms.CharField()
    email = forms.CharField()
    password = forms.CharField()
    phone = forms.CharField()
