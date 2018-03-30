from datetime import datetime


def current_datetime(request):
    return {'current_datetime': datetime.now()}
