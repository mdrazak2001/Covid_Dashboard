from django.conf.urls import include, url
from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('country/<str:country_index>',
         views.countryInsights, name="country_graph"),
    path('countries/<str:country_index1>/<str:country_index2>',
         views.versus, name='versus'),
]
