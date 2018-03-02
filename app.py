import os

from django_micro import configure, route, run, get_app_label
from django.conf.urls import include
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
INSTALLED_APPS = ['rest_framework',]
STATIC_ROOT = 'static/'
STATIC_URL = '/static/'

configure(locals(), django_admin=True)
from rest_framework import routers, serializers, viewsets, permissions
from rest_framework.response import Response


class Quote(models.Model):
    content = models.TextField()

    class Meta:
        app_label = get_app_label()


class QuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = ('content',)


class QuoteViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer

    def retrieve(self, request, pk=None):
        if pk == 'random':
            quote = Quote.objects.order_by('?').first()
            serializer = QuoteSerializer(quote)
            return Response(serializer.data)
        else:
            super(QuoteViewSet, self).retrieve(request, pk)

router = routers.DefaultRouter()
router.register(r'quotes', QuoteViewSet)


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    pass


@route('')
def homepage(request):
    quotes = Quote.objects.order_by('pk').reverse()
    return render(request, 'base.html', {'quotes': quotes})


@route('quotes/<int:quote>')
def get_quote(request, quote):
    quote = Quote.objects.get(pk=quote)
    return render(request, 'base.html', {'quotes': [quote]})


route(r'api/', include(router.urls))
route(os.environ.get('ADMIN_PATH', 'admin/'), admin.site.urls)
application = run()
