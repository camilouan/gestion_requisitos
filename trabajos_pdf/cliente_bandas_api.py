import requests
import json # Para imprimir JSON de forma legible

API_BASE_URL = "http://localhost:5000/bandas"

def mostrar_respuesta(response):
    """Helper para mostrar la respuesta de la API de forma legible."""
    print(f"Status Code: {response.status_code}")
    try:
        print("Respuesta JSON:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except requests.exceptions.JSONDecodeError:
        print("Respuesta (No JSON):")
        print(response.text)
    print("-" * 30)

def crear_nueva_banda(datos_banda):
    print("\n--- CREANDO NUEVA BANDA ---")
    try:
        response = requests.post(API_BASE_URL, json=datos_banda)
        mostrar_respuesta(response)
        return response.json() if response.ok else None
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión al crear banda: {e}")
        return None

def obtener_todas():
    print("\n--- OBTENIENDO TODAS LAS BANDAS ---")
    try:
        response = requests.get(API_BASE_URL)
        mostrar_respuesta(response)
        return response.json() if response.ok else None
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión al obtener bandas: {e}")
        return None

def obtener_por_id(banda_id):
    print(f"\n--- OBTENIENDO BANDA CON ID: {banda_id} ---")
    try:
        response = requests.get(f"{API_BASE_URL}/{banda_id}")
        mostrar_respuesta(response)
        return response.json() if response.ok else None
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión al obtener banda por ID: {e}")
        return None

def actualizar_banda_existente(banda_id, datos_actualizacion):
    print(f"\n--- ACTUALIZANDO BANDA CON ID: {banda_id} ---")
    try:
        response = requests.put(f"{API_BASE_URL}/{banda_id}", json=datos_actualizacion)
        mostrar_respuesta(response)
        return response.json() if response.ok else None
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión al actualizar banda: {e}")
        return None

def eliminar_banda_existente(banda_id):
    print(f"\n--- ELIMINANDO BANDA CON ID: {banda_id} ---")
    try:
        response = requests.delete(f"{API_BASE_URL}/{banda_id}")
        mostrar_respuesta(response)
        return response.json() if response.ok else None # O True si es 204 y no hay JSON
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión al eliminar banda: {e}")
        return None

if __name__ == '__main__':
    print("Cliente API de Bandas interactuando con el servidor...")
    print("Asegúrate de que 'servidor_bandas_api.py' esté ejecutándose en otra terminal.")
    input("Presiona Enter para comenzar las pruebas (después de iniciar el servidor)...")

    # 1. Obtener todas las bandas iniciales
    bandas_actuales = obtener_todas()
    if bandas_actuales:
        print(f"Número de bandas iniciales: {len(bandas_actuales)}")

    # 2. Crear una nueva banda
    nueva_banda_datos = {
        "nombre": "Metallica",
        "genero": "Thrash Metal",
        "pais_origen": "EE.UU.",
        "año_formacion": 1981,
        "integrantes": ["James Hetfield", "Lars Ulrich", "Kirk Hammett", "Robert Trujillo"]
    }
    banda_creada = crear_nueva_banda(nueva_banda_datos)
    id_nueva_banda = None
    if banda_creada and 'id' in banda_creada:
        id_nueva_banda = banda_creada['id']
        print(f"Banda creada con ID: {id_nueva_banda}")

    # 3. Obtener todas las bandas de nuevo
    obtener_todas()

    # 4. Obtener la banda recién creada por su ID
    if id_nueva_banda:
        obtener_por_id(id_nueva_banda)

    # 5. Intentar obtener una banda que no existe
    obtener_por_id(999)

    # 6. Actualizar la banda creada (si existe)
    if id_nueva_banda:
        datos_actualizacion = {
            "genero": "Heavy Metal / Thrash Metal",
            "integrantes": ["James Hetfield", "Lars Ulrich", "Kirk Hammett", "Robert Trujillo", "Cliff Burton (In Memoriam)"]
        }
        actualizar_banda_existente(id_nueva_banda, datos_actualizacion)
        # Verificar la actualización obteniéndola de nuevo
        obtener_por_id(id_nueva_banda)

    # 7. Eliminar la banda creada (si existe)
    if id_nueva_banda:
        eliminar_banda_existente(id_nueva_banda)
        # Intentar obtenerla de nuevo para verificar que fue eliminada
        obtener_por_id(id_nueva_banda)

    # 8. Obtener todas las bandas al final
    obtener_todas()

    print("\n--- Pruebas del cliente finalizadas ---")