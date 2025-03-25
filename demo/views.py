from django import http
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404, render

from karate.models import Occurrence, EventType

try:
    import requests
except ImportError:
    requests = None


def event_type(request, abbr):
    event_type = get_object_or_404(EventType, abbr=abbr)
    now = datetime.now()
    occurrences = Occurrence.objects.filter(
        event__event_type=event_type,
        start_time__gte=now,
        start_time__lte=now + timedelta(days=+30),
    )
    return render(
        request,
        "karate/upcoming_by_event_type.html",
        {"occurrences": occurrences, "event_type": event_type},
    )


def smoketest(request):
    if not requests:
        return http.HttpResponse("<code>requests</code> not availabe: pip install requests")

    host = "{}{}".format("https://" if request.is_secure() else "http://", request.get_host())
    occ = Occurrence.objects.select_related("event", "event__event_type").first()
    dt = occ.start_time
    results = []
    errors = 0
    i = 0
    for url, expected in [
        (f"{host}/", 200),
        (f"{host}/karate/", 200),
        (f"{host}/karate/swingtime/events/type/{occ.event.event_type.abbr}/", 200),
        (f"{host}/karate/swingtime/", 200),
        (f"{host}/karate/swingtime/calendar/", 200),
        (f"{host}/karate/swingtime/calendar/{dt.year}/", 200),
        (f"{host}/karate/swingtime/calendar/{dt.year}/{dt.month}/", 200),
        (f"{host}/karate/swingtime/calendar/{dt.year}/{dt.month}/{dt.day}/", 200),
        (f"{host}/karate/swingtime/events/", 200),
        (f"{host}/karate/swingtime/events/create/", 200),
        (f"{host}/karate/swingtime/events/{occ.event.pk}/", 200),
        (f"{host}/karate/swingtime/events/{occ.event.pk}/{occ.pk}/", 200),
        (f"{host}/docs/", 200),
        (f"{host}/docs/index.html", 200),
    ]:
        i += 1
        error = ""
        emoji = "✅"
        try:
            r = requests.get(url)
        except Exception as e:
            error = str(e)
        else:
            if r.status_code != expected:
                error = f"Response code {r.response_code} did not match {expected}"

        if error:
            emoji = "⛔️"
            errors += 1
        
        results.append(f"{emoji} {url}")
        if error:
            results.append(error)

    results = "\n\n".join(results)
    return http.HttpResponse(f"<pre>{i - errors} of {i} smoketests passed\n\n{results}</pre>")