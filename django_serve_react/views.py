from django.http import HttpResponse
from django.conf import settings
import os

# Serve React build index.html
def index(request):
    try:
        with open(os.path.join(settings.STATIC_ROOT, 'index.html')) as file:
            return HttpResponse(file.read())
    except FileNotFoundError:
        return HttpResponse(
            "index.html not found. Ensure you've run 'collectstatic'.",
            status=501,
        )