import os

from django_micro import configure, route, run, get_app_label
from django.contrib import admin
from django.shortcuts import render
from django.db import models

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEBUG = False if os.environ.get('DEBUG') == 'False' else True
if not DEBUG:
    ALLOWED_HOSTS = [os.environ.get('ALLOWED_HOST', 'quotes.hotkosc.ru')]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.environ.get(
            'DATABASE_PATH',
            os.path.join(BASE_DIR, 'db.sqlite3'),
        )
    },
}
STATIC_ROOT = 'static/'
STATIC_URL = '/static/'

configure(locals(), django_admin=True)

class Quote(models.Model):
    content = models.TextField()

    class Meta:
        app_label = get_app_label()


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    pass

@route('')
def homepage(request):
    quotes = Quote.objects.all()
    return render(request, 'base.html', {'quotes': quotes})


route(os.environ.get('ADMIN_PATH', 'admin/'), admin.site.urls)
application = run()
