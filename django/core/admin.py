from django.contrib import admin

from .models import Movie, Person, Role


admin.site.register(Person)
admin.site.register(Role)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'released', 'runtime',
                    'rating', 'director')
    list_filter = ('released', 'rating')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'released'
    ordering = ('released', 'rating')
