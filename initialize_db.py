from EventManagement.models import Organizer, Event
from event_details import EVENT_DETAILS

for i in EVENT_DETAILS:
    k = Organizer()
    k.code = i
    k.name = EVENT_DETAILS[i]['name']
    k.save()

for i in EVENT_DETAILS:
    for k in EVENT_DETAILS[i]['events']:
        e = Event()
        e.code = EVENT_DETAILS[i]['events'][k]['code']
        e.name = EVENT_DETAILS[i]['events'][k]['name']
        e.organizer = Organizer.objects.get(code=i)
        e.save()