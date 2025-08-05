from django_mongoengine.mongo_admin import DocumentAdmin, site
from .models import TestModel

class TestModelAdmin(DocumentAdmin):
    list_display = ('name',)
    search_fields = ('name',)

site.register(TestModel, TestModelAdmin)