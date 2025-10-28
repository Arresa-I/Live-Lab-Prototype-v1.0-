from Información import *
from Búsqueda import *
import copy

# -------------------VARIABLES-------------------
# Diccionarios para almacenar listas de coincidencias y originales de cada categoría
Coincidencias = {cat: [] for cat in Listas_Coincidentes.keys()}
Originales = {cat: [] for cat in Listas_Coincidentes.keys()}

# -------------------FUNCIONES-------------------
# Función para limpiar listas
def limpiar_listas(*listas):
    for lista in listas:
        lista.clear()


# Función para gestionar coincidencias entre listas originales y de coincidencia de una categoría
def coincidencias_listas(lista1, lista2, Coincidencias):
    """
    Compara dos listas de listas, detecta los elementos coincidentes y crea una lista de listas con los resultados.
    
    - Si hay coincidencias, las agrega a la lista resultante.
    - Si no hay coincidencias, agrega todos los elementos de ambas listas, separados por "------------".
    - Para claves específicas, combina directamente las listas sin comparación.

    Args:
        lista1 (dict of lists): Primera lista de listas a comparar.
        lista2 (dict of lists): Segunda lista de listas a comparar.
        Coincidencias (dict of lists): Diccionario donde se almacenarán los resultados.

    Returns:
        dict of lists: Diccionario con los resultados de las comparaciones.
    """

    claves_combinadas = {"Calentamiento", "Fundamentos", "Desarrollo"}

    # Iterar sobre ambas listas en paralelo
    for clave, sublista1, sublista2 in zip(lista1.keys(), lista1.values(), lista2.values()):
        if isinstance(sublista1, str):
            sublista1 = globals().get(sublista1, [])
        if isinstance(sublista2, str):
            sublista2 = globals().get(sublista2, [])

        if clave in claves_combinadas:
            # Para estas claves, simplemente combinamos ambas listas sin comparación
            Coincidencias[clave] = list(set(sublista1) | set(sublista2))
        else:
            # Encontrar elementos coincidentes
            Coincidencias[clave] = list(set(sublista1) & set(sublista2))
            
            if not Coincidencias[clave] and sublista1 and sublista2:
                # Si no hay coincidencias, añadir todos los elementos con "------------" como separador
                Coincidencias[clave] = sublista1 + ["------------"] + sublista2
            
            elif not Coincidencias[clave] and (sublista1 or sublista2):
                # Si una de las listas está vacía, simplemente unir ambas
                Coincidencias[clave] = sublista1 + sublista2
          
    return Coincidencias
