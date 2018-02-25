from django.contrib import admin

# Register your models here.
from EventManagement.models import *

admin.site.register(Organizer)
admin.site.register(Event)
admin.site.register(RituAdmin)
admin.site.register(Head)
admin.site.register(RegistrationDesk)
admin.site.register(EventVolunteer)
admin.site.register(Volunteer)