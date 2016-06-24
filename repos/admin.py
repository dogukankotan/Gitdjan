from django.contrib import admin

# Register your models here.

from .models import Repository
class RepoAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'timestamp']
    class Meta:
        model = Repository


admin.site.register(Repository, RepoAdmin)

