from django.contrib import admin
from django_mongoengine.mongo_admin import DocumentAdmin, site
from .models import TestModel, Character


class TestModelAdmin(DocumentAdmin):
    list_display = ('name',)
    search_fields = ('name',)


site.register(TestModel, TestModelAdmin)


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'archetype', 'gender', 'is_default')
    list_filter = ('is_default',)
