#!/usr/bin/env python3
"""
Django management command para crear universos de ejemplo
"""

import os
import sys
import django
from datetime import datetime

# Configurar Django
sys.path.append('/c/Users/36705/Desktop/Nueva carpeta (4)/KandaProyect/KandaBackEnd')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'KandaBackend.settings')
django.setup()

from api.models.documents import Universe
from django.contrib.auth.models import User

def get_or_create_admin_user():
    """Obtener el usuario administrador existente"""
    try:
        # Buscar el usuario por email
        admin_user = User.objects.get(email='luisfelipebolanosdixon@gmail.com')
        print(f"Ô£à Usuario administrador encontrado: {admin_user.username}")
        return admin_user
    except User.DoesNotExist:
        try:
            # Buscar por username alternativo
            admin_user = User.objects.get(username='luisfelipe')
            print(f"Ô£à Usuario administrador encontrado: {admin_user.username}")
            return admin_user
        except User.DoesNotExist:
            print("ÔØî Usuario administrador no encontrado")
            print("Por favor ejecuta primero: python make_admin.py")
            return None

# Datos de universos
universes_data = [
    {
        "name": "Reino de Eldoria",
        "description": "Un mundo fant+ístico medieval lleno de magia, dragones y aventuras +®picas donde la luz y la oscuridad luchan por el control del reino.",
        "setting": "Eldoria es un vasto reino medieval dividido en cinco territorios: las Monta+¦as Cristalinas del Norte donde habitan los enanos, los Bosques Encantados del Este hogar de los elfos, las Llanuras Doradas del Sur con pr+¦speras ciudades humanas, el Pantano Sombrio del Oeste lleno de criaturas misteriosas, y la Torre Central donde reside el Rey Mago. La magia fluye a trav+®s de cristales antiguos y cada territorio tiene su propia escuela de hechicer+¡a.",
        "rules": "La magia requiere cristales como catalizadores y consume energ+¡a vital del usuario. Los dragones son seres inteligentes que pueden ser aliados o enemigos. Existen cinco escuelas de magia: Elemental, Curaci+¦n, Ilusi+¦n, Nigromancia y Transmutaci+¦n. Los muertos no pueden ser revividos completamente. El hierro fr+¡o anula la magia +®lfica.",
        "tone": "+®pico",
        "themes": "Honor, amistad, el poder corrompe, sacrificio por el bien mayor, la uni+¦n hace la fuerza"
    },
    {
        "name": "Nueva Tokio 2087",
        "description": "Una metr+¦polis cyberpunk donde la tecnolog+¡a y la humanidad chocan en las calles neon-iluminadas de una sociedad dist+¦pica controlada por megacorporaciones.",
        "setting": "Nueva Tokio en 2087 es una ciudad vertical de 200 niveles. Los ricos viven en los niveles superiores con aire puro y tecnolog+¡a avanzada, mientras que los pobres sobreviven en los niveles inferiores entre la contaminaci+¦n y la criminalidad. Las megacorporaciones controlan todo: Yamamoto Corp (biotecnolog+¡a), Nexus Industries (cibern+®tica), y DataFlow (informaci+¦n). Los hackers operan desde cibercaf+®s clandestinos y la polic+¡a usa androides para patrullar.",
        "rules": "Los implantes cibern+®ticos mejoran habilidades pero pueden causar cyberpsicosis si se usan en exceso. La IA tiene tres niveles: b+ísica, avanzada y autoconsciente (ilegal). El hacking requiere hardware especializado y puede ser rastreado. Las armas son principalmente energ+®ticas. Los androides no pueden da+¦ar directamente a humanos debido a sus protocolos.",
        "tone": "misterioso",
        "themes": "-+Qu+® significa ser humano?, la tecnolog+¡a como liberaci+¦n y prisi+¦n, corrupci+¦n corporativa, supervivencia en la adversidad"
    },
    {
        "name": "Academia Arcanum",
        "description": "Una prestigiosa escuela de magia flotante donde j+¦venes magos aprenden a dominar sus poderes mientras enfrentan misterios, rivalidades y amenazas ancestrales.",
        "setting": "La Academia Arcanum flota sobre las nubes, sostenida por cristales m+ígicos antiguos. Tiene cuatro casas: Ignis (fuego/valor), Aqua (agua/sabidur+¡a), Terra (tierra/lealtad) y Ventus (aire/creatividad). Los estudiantes viven en dormitorios seg+¦n su casa, asisten a clases de hechizos, pociones, criaturas m+ígicas e historia arcana. La academia tiene una biblioteca infinita, laboratorios de alquimia, y jardines con plantas m+ígicas.",
        "rules": "Los estudiantes usan varitas que se sincronizan con su aura m+ígica. La magia requiere palabras de poder, gestos precisos y concentraci+¦n mental. Est+í prohibido usar magia fuera del campus sin supervisi+¦n. Los duelos m+ígicos son legales solo en el coliseo bajo reglas estrictas. Existen criaturas guardianas que protegen la academia de intrusos.",
        "tone": "aventura",
        "themes": "Amistad, crecimiento personal, responsabilidad del poder, superar los prejuicios, el conocimiento como poder"
    },
    {
        "name": "Oeste Salvaje Sobrenatural",
        "description": "El viejo oeste americano pero con un toque paranormal: vampiros, hombres lobo, brujas y cazadores de demonios en pueblos fronterizos llenos de peligro.",
        "setting": "A+¦o 1885 en los territorios de Arizona y Nuevo M+®xico. Los pueblos mineros atraen todo tipo de criaturas sobrenaturales. Deadwood Gulch es controlado por un vampiro sheriff, Silver Creek tiene una manada de hombres lobo, y Perdition est+í plagado de demonios que emergen de una mina maldita. Los trenes transportan mercanc+¡as normales y artefactos m+ígicos. Los nativos americanos conocen rituales antiguos para combatir lo sobrenatural.",
        "rules": "La plata da+¦a a la mayor+¡a de criaturas sobrenaturales. Los vampiros no pueden cruzar agua corriente ni entrar a hogares sin invitaci+¦n. Los hombres lobo son vulnerables durante la luna nueva. Los demonios necesitan ser invocados o encontrar portales para manifestarse. Las balas bendecidas son efectivas contra no-muertos. Los rituales nativos pueden crear protecciones temporales.",
        "tone": "dram+ítico",
        "themes": "Justicia vs venganza, redenci+¦n, el precio de la supervivencia, fe vs escepticismo, civilizaci+¦n vs naturaleza salvaje"
    },
    {
        "name": "Estaci+¦n Esperanza",
        "description": "Una estaci+¦n espacial en los confines de la galaxia donde diplom+íticos, comerciantes, exploradores y refugiados de diferentes especies coexisten mientras enfrentan amenazas c+¦smicas.",
        "setting": "La Estaci+¦n Esperanza orbita una estrella binaria en el sector neutral de la galaxia. Es un puerto franco donde cinco especies principales comercian: Humanos (adaptables), Kristalinos (telep+íticos), Void'hai (energia pura), Zephyrians (tecnol+¦gicos) y Terraxi (guerreros). La estaci+¦n tiene sectores ambientales para cada especie, un gran bazar comercial, laboratorios de investigaci+¦n, y bah+¡as de naves. Amenazas incluyen piratas espaciales, anomal+¡as dimensionales y una raza antigua dormida.",
        "rules": "Cada especie tiene habilidades +¦nicas: humanos son adaptables, kristalinos leen mentes, void'hai manipulan energ+¡a, zephyrians controlan tecnolog+¡a, terraxi tienen fuerza superior. La comunicaci+¦n universal se logra con implantes traductores. Las armas energ+®ticas pueden da+¦ar el casco de la estaci+¦n. Algunas tecnolog+¡as son incompatibles entre especies. Los viajes FTL requieren navegantes especializados.",
        "tone": "aventura",
        "themes": "Cooperaci+¦n interespecies, exploraci+¦n de lo desconocido, diplomacia vs conflicto, supervivencia en el espacio, unidad en la diversidad"
    }
]

def create_universes():
    """Crear universos directamente en la base de datos"""
    print("­ƒîƒ Creando universos en la base de datos...")
    print("=" * 50)
    
    # Obtener o crear usuario admin
    admin_user = get_or_create_admin_user()
    
    created_count = 0
    skipped_count = 0
    
    for universe_data in universes_data:
        # Verificar si ya existe
        existing = Universe.objects.filter(name=universe_data['name']).first()
        
        if existing:
            print(f"ÔÜá´©Å  '{universe_data['name']}' ya existe, saltando...")
            skipped_count += 1
            continue
        
        try:
            # Crear nuevo universo usando los campos del modelo actual
            universe = Universe(
                name=universe_data['name'],
                description=universe_data['description'],
                context=universe_data['setting'],  # Mapear setting a context
                rules=universe_data['rules'],
                # Agregar campos del modelo actual
                time_period="Indefinido",
                location="M+¦ltiples ubicaciones", 
                technology_level=universe_data['tone'],  # Usar tone como technology_level temporalmente
                magic_allowed=True if 'magia' in universe_data['description'].lower() else False,
                supernatural_elements=True if any(word in universe_data['description'].lower() for word in ['sobrenatural', 'fantas+¡a', 'magia', 'vampiros', 'hombres lobo']) else False,
                is_public=True
                # No incluir created_by por ahora para evitar errores de referencia
            )
            universe.save()
            
            print(f"Ô£à '{universe_data['name']}' creado exitosamente")
            created_count += 1
            
        except Exception as e:
            print(f"ÔØî Error creando '{universe_data['name']}': {e}")
    
    print("\n" + "=" * 50)
    print(f"­ƒôè Resumen:")
    print(f"   Ô£à Universos creados: {created_count}")
    print(f"   ÔÜá´©Å  Universos saltados: {skipped_count}")
    print(f"   ­ƒôÜ Total en base de datos: {Universe.objects.count()}")
    
    if created_count > 0:
        print(f"\n­ƒÄë -íLos universos est+ín listos para usar!")
        print(f"   Ve a http://localhost:5175/universes para verlos")

def list_existing_universes():
    """Listar universos existentes"""
    print("\n­ƒôÜ Universos existentes en la base de datos:")
    print("-" * 50)
    
    universes = Universe.objects.all()
    
    if not universes:
        print("   No hay universos creados a+¦n.")
        return
    
    for i, universe in enumerate(universes, 1):
        print(f"{i}. {universe.name}")
        print(f"   Descripci+¦n: {universe.description[:100]}...")
        print(f"   Contexto: {universe.context}")
        print(f"   Magia permitida: {'S+¡' if universe.magic_allowed else 'No'}")
        print(f"   Creado: {universe.created_at.strftime('%Y-%m-%d %H:%M')}")
        print()

if __name__ == "__main__":
    try:
        print("­ƒîƒ Script de creaci+¦n de universos para Kanda Project")
        print("=" * 60)
        
        # Listar universos existentes
        list_existing_universes()
        
        # Crear nuevos universos
        create_universes()
        
        # Listar universos despu+®s de la creaci+¦n
        list_existing_universes()
        
    except Exception as e:
        print(f"ÔØî Error ejecutando el script: {e}")
        import traceback
        traceback.print_exc()
