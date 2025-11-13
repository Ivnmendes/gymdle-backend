from django.contrib import admin

from .models import APIKey

@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ('service', 'key', 'is_active', 'created_at')
    search_fields = ('service', 'key')
    list_filter = ('is_active', 'created_at')
    readonly_fields = ('key', 'created_at')
    ordering = ('-created_at',)
    