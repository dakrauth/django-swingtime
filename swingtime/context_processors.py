from datetime import datetime

#-------------------------------------------------------------------------------
def current_datetime(request):
    return dict(current_datetime=datetime.now())