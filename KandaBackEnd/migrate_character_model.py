#!/usr/bin/env python
"""
Script para migrar el modelo Character a+¶adiendo los nuevos campos.
Este script agrega los campos special_abilities y goals a documentos existentes.
"""

import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'KandaBackend.settings')
django.setup()

from api.models.documents import Character

def migrate_characters():
    """Migra los personajes existentes para incluir los nuevos campos."""
    print("Iniciando migraci+¶n de modelo Character...")
    
    try:
        # Obtener todos los personajes existentes
        characters = Character.objects.all()
        print(f"Encontrados {characters.count()} personajes para migrar.")
        
        updated_count = 0
        for character in characters:
            # Verificar si necesita migraci+¶n
            needs_update = False
            
            # Agregar special_abilities si no existe
            if not hasattr(character, 'special_abilities') or character.special_abilities is None:
                character.special_abilities = ""
                needs_update = True
            
            # Agregar goals si no existe
            if not hasattr(character, 'goals') or character.goals is None:
                character.goals = ""
                needs_update = True
                
            # Agregar age si no existe
            if not hasattr(character, 'age') or character.age is None:
                character.age = 0
                needs_update = True
            
            # Guardar si hay cambios
            if needs_update:
                character.save()
                updated_count += 1
                print(f"Migrado personaje: {character.name}")
        
        print(f"Migraci+¶n completada. {updated_count} personajes actualizados.")
        
    except Exception as e:
        print(f"Error durante la migraci+¶n: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    success = migrate_characters()
    if success:
        print("‘£‡ Migraci+¶n exitosa!")
        sys.exit(0)
    else:
        print("‘ÿÓ Migraci+¶n fall+¶!")
        sys.exit(1)
