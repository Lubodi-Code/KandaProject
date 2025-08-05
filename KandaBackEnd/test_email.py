#!/usr/bin/env python
"""
Script para probar el envío de correos electrónicos en Django.
Este script configura el entorno de Django y envía un correo de prueba.

Uso:
    python test_email.py destinatario@example.com
"""

import os
import sys
import django
from django.core.mail import send_mail
from django.conf import settings

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'KandaBackend.settings')
django.setup()

def test_email(recipient_email):
    """
    Envía un correo electrónico de prueba al destinatario especificado.
    
    Args:
        recipient_email (str): La dirección de correo electrónico del destinatario.
    
    Returns:
        bool: True si el correo se envió correctamente, False en caso contrario.
    """
    subject = 'Prueba de correo desde KandaBackend'
    message = 'Este es un correo de prueba para verificar la configuración de correo en KandaBackend.'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [recipient_email]
    
    try:
        # Intentar enviar el correo
        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=False,
        )
        print(f"\n✅ Correo enviado correctamente a {recipient_email}")
        print(f"   Desde: {from_email}")
        print(f"   Asunto: {subject}")
        print("\nVerifica la bandeja de entrada (y la carpeta de spam) para confirmar la recepción.")
        return True
    except Exception as e:
        print(f"\n❌ Error al enviar el correo: {str(e)}")
        print("\nVerifica la configuración de correo en settings.py y el archivo .env:")
        print(f"   EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
        print(f"   EMAIL_HOST: {settings.EMAIL_HOST}")
        print(f"   EMAIL_PORT: {settings.EMAIL_PORT}")
        print(f"   EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
        print(f"   EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
        print(f"   DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
        print("\nSi estás usando Gmail, asegúrate de:")
        print("1. Haber generado una 'contraseña de aplicación' en la configuración de seguridad de Google")
        print("2. Haber habilitado el acceso de aplicaciones menos seguras (si es una cuenta personal)")
        return False

def main():
    """
    Función principal que procesa los argumentos de la línea de comandos
    y ejecuta la prueba de correo.
    """
    if len(sys.argv) != 2:
        print("Uso: python test_email.py destinatario@example.com")
        sys.exit(1)
    
    recipient_email = sys.argv[1]
    print(f"\nEnviando correo de prueba a {recipient_email}...")
    
    success = test_email(recipient_email)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()