import os

from django_micro import configure, route, run, get_app_label
from django.shortcuts import render
from django.db import models

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
}
configure(locals())


class Quote(models.Model):
    content = models.TextField()

    class Meta:
        app_label = get_app_label()


@route('')
def homepage(request):
    quotes = Quote.objects.all()
    return render(request, 'base.html', {'quotes': quotes})


application = run()
