#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'KandaBackend.settings')
django.setup()

from django.contrib.auth.models import User

def make_user_admin():
    """Hacer que el usuario sea administrador"""
    email = "luisfelipebolanosdixon@gmail.com"
    
    try:
        # Buscar el usuario por email
        user = User.objects.get(email=email)
        print(f"дЃр Usuario encontrado: {user.username} ({user.email})")
        
        # Hacerlo staff y superuser
        user.is_staff = True
        user.is_superuser = True
        user.save()
        
        print(f"дЃр Usuario {user.username} ahora es administrador")
        return user
        
    except User.DoesNotExist:
        print(f"дию Usuario con email {email} no encontrado")
        print("Creando usuario administrador...")
        
        # Crear el usuario como admin
        user = User.objects.create_user(
            username='luisfelipe',
            email=email,
            password='pipe7070',
            is_staff=True,
            is_superuser=True
        )
        print(f"дЃр Usuario administrador creado: {user.username}")
        return user

if __name__ == "__main__":
    make_user_admin()
