from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Comments


class CommnetsMPTTModelAdmin(MPTTModelAdmin):
    mptt_level_indent = 20


admin.site.register(Comments, CommnetsMPTTModelAdmin)
