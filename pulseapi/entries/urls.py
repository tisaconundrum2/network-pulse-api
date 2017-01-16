from django.conf.urls import url

from pulseapi.entries.views import (
    EntriesListView,
    EntryView,
    toggle_favorite
)

urlpatterns = [
    url('^$', EntriesListView.as_view(), name='entries-list'),
    url(r'^(?P<entryid>[0-9]+)/favorite/?', toggle_favorite, name='favorite'),
    url(r'^(?P<pk>[0-9]+)/', EntryView.as_view(), name='entry'),
]
