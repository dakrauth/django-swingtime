from django.utils import timezone


def current_datetime(request):
    return {"current_datetime": timezone.now()}
