#!/usr/bin/env python3
"""
Script para crear universos de ejemplo en el sistema de storytelling
"""

import requests
import json

# Configuraci+¦n
BASE_URL = "http://127.0.0.1:8000/api"
LOGIN_URL = f"{BASE_URL}/auth/login/"
UNIVERSES_URL = f"{BASE_URL}/universes/"

# Datos de ejemplo para crear universos
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

def get_auth_token():
    """Funci+¦n para obtener token de autenticaci+¦n (requiere usuario admin)"""
    # Por ahora retornamos None, ya que necesitar+¡amos credenciales reales
    print("ÔÜá´©Å  Para crear universos necesitas estar autenticado como administrador")
    print("   Puedes usar la interfaz web en http://localhost:5175/universes")
    return None

def create_universe(universe_data, token=None):
    """Crear un universo usando la API"""
    headers = {
        'Content-Type': 'application/json',
    }
    
    if token:
        headers['Authorization'] = f'Bearer {token}'
    
    try:
        response = requests.post(UNIVERSES_URL, 
                               data=json.dumps(universe_data), 
                               headers=headers)
        
        if response.status_code == 201:
            print(f"Ô£à Universo '{universe_data['name']}' creado exitosamente")
            return response.json()
        else:
            print(f"ÔØî Error creando '{universe_data['name']}': {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("ÔØî Error: No se pudo conectar al servidor. -+Est+í corriendo Django en el puerto 8000?")
        return None
    except Exception as e:
        print(f"ÔØî Error inesperado: {e}")
        return None

def main():
    """Funci+¦n principal"""
    print("­ƒîƒ Script para crear universos de ejemplo")
    print("=" * 50)
    
    # Verificar conexi+¦n con la API
    try:
        response = requests.get(f"{BASE_URL}/")
        print("Ô£à Servidor Django est+í corriendo")
    except:
        print("ÔØî Error: Servidor Django no est+í disponible")
        print("   Aseg+¦rate de que est+® corriendo en http://127.0.0.1:8000")
        return
    
    # Obtener token (por ahora manual)
    token = get_auth_token()
    
    print("\n­ƒôû Universos disponibles para crear:")
    print("-" * 40)
    
    for i, universe in enumerate(universes_data, 1):
        print(f"{i}. {universe['name']}")
        print(f"   {universe['description'][:100]}...")
        print()
    
    print("­ƒÆí Informaci+¦n de los universos:")
    print("-" * 40)
    
    for universe in universes_data:
        print(f"\n­ƒÅ¦ {universe['name']}")
        print(f"­ƒôØ Descripci+¦n: {universe['description']}")
        print(f"­ƒîì Ambientaci+¦n: {universe['setting'][:200]}...")
        print(f"ÔÜû´©Å  Reglas: {universe['rules'][:200]}...")
        print(f"­ƒÄ¡ Tono: {universe['tone']}")
        print(f"­ƒÄ» Temas: {universe['themes']}")
        print("-" * 60)
    
    print("\n­ƒöº Para crear estos universos:")
    print("1. Ve a http://localhost:5175/login")
    print("2. Inicia sesi+¦n como administrador")
    print("3. Ve a http://localhost:5175/universes")
    print("4. Usa los datos de arriba para crear cada universo")
    
    print("\n­ƒÆ¥ Los datos tambi+®n est+ín disponibles en este script para copiar y pegar")

if __name__ == "__main__":
    main()
