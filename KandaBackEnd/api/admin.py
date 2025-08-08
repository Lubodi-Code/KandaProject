# Admin configuration disabled
# Since we're using MongoEngine instead of Django ORM, 
# Django's admin interface is not compatible with our models.
# If you need an admin interface, consider using:
# 1. Django-MongoEngine admin (django-mongoengine package)
# 2. Custom admin views with MongoEngine
# 3. External tools like MongoDB Compass

# Uncomment the lines below if you install django-mongoengine and want to use its admin:
# from django_mongoengine.mongo_admin import DocumentAdmin, site
# from .models import TestModel, Character, User
# 
# class CharacterAdmin(DocumentAdmin):
#     list_display = ('name', 'archetype', 'user', 'created_at')
#     search_fields = ('name', 'archetype')
#     list_filter = ('archetype', 'created_at')
# 
# site.register(Character, CharacterAdmin)