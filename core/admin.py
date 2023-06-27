from django.contrib import admin
from .models import Language


# Register your models here.


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ["code", "name", "native_name"]
    search_fields = ["name"]
