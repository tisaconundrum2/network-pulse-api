from django.contrib import admin

from .models import Entry


class EntryAdmin(admin.ModelAdmin):
    """
    Show a list of entries a user has submitted in the EmailUser Admin app
    """

    fields = (
        'title',
        'description',
        'content_url',
        'thumbnail_url',
        'tags',
        'get_involved',
        'get_involved_url',
        'interest',
        'featured',
        'internal_notes',
        'issues',
        'creators',
        'published_by',
        'favorite_count'
    )

    readonly_fields = ('favorite_count',)

    def favorite_count(self, instance):
        """
        Show the total number of favorites for this Entry
        """
        return instance.favorited_by.count()


admin.site.register(Entry, EntryAdmin)
