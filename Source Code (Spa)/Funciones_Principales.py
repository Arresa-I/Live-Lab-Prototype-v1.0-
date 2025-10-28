from Información import *
from Búsqueda import *
from Combinación import *

# -------------VARIABLES-------------

indice = []

# ---------FUNCIÓN AUXILIARES---------
### Borrado de listas

def Borrado_Listas(lst):
    """Limpia todas las listas proporcionadas."""
    if lst is not None and isinstance(lst, list):  # Verifica que lst sea una lista no vacía
        lst.clear()
    else:
        print("Error: La variable no es una lista válida.")


# -------------FUNCIÓN 1: Búsqueda Musical-------------
### Buscar resultados a partir del "Elemento Central" del botón "Mostrar Resultados"

def Mostrar_Resultados_Musical(Parametro):
    indice.clear()

    # Buscar el índice de Elemento_Central en Categorías (1 a 4)
    for clave, subcategorias in Categorias.items():
        try:    
            if Parametro in subcategorias:
                indice.append(clave)  # Almacenar el nombre de la categoría
                indice.append(subcategorias.index(Parametro))  # Almacenar el índice dentro de la lista
                break  # Salir del bucle cuando se encuentra el elemento
        except ValueError:
            continue  # Si el Parametro no está, continuar sin hacer nada

    # Llamar a la función de opciones de categorías
    Muestra_Opciones_Cat(indice)

    # LLamar a la función para la búsqueda de lecciones y objetivos
    Llamada_Lecciones_Objetivos(Parametro, True)

    # Acceder directamente a las claves del diccionario
    resultados_coincidentes = {clave: lista for clave, lista in Listas_Coincidentes.items()}
    
    return resultados_coincidentes

# -------------FUNCIÓN 2: Búsqueda Lección-------------
### Buscar resultados a partir de la "Lección Central" del botón "Mostrar Resultados"
##### 1º Busca las lecciones y objetivos con el parámetro seleccionado
##### 2º Se hace un repaso por cada lección para ver que elementos contienen las lecciones

def Mostrar_Resultados_Leccion(Parametro):

    [Borrado_Listas(Listas_Coincidentes[clave]) for clave in ["Habilidades", "Dimensiones Musicales", "SubDimensiones Musicales", "Técnicas", "Modos"]]

    # LLamar a la función para la búsqueda de lecciones y objetivos
    Llamada_Lecciones_Objetivos(Parametro, True)

    # Analizar las características de las lecciones para recopilar la lista de elementos
    for clave in ["Calentamiento", "Fundamentos", "Desarrollo", "Improvisación"]:
        for file in Listas_Coincidentes[clave]:
            analisis_lecciones(file)


# -------------FUNCIÓN 3: Combinación (Musical y Lectivo)-------------
# Función principal de combinación y procesamiento
def combinacion(Seleccion):
    # Limpiar listas
    limpiar_listas(*Coincidencias.values(), *Originales.values())

    # Trasladar a "Originales" la lista de resultados anterior a la selección
    for clave, nueva_lista in zip(Originales.keys(), Listas_Coincidentes.values()):
        Originales[clave].extend(nueva_lista)   

    # Identificar categoría y procesar -> Aquí se determina un cambio si el ítem seleccionado es musical o no musical
    for cat, list1 in zip(Categorias.keys(), Categorias.values()):
        if Seleccion in list1:
            Categoria1, Categoria2 = cat, list1.index(Seleccion)
            Muestra_Opciones_Cat([Categoria1, Categoria2])
            break
    else:
        limpiar_listas(*Listas_Coincidentes.values())
        if Seleccion.startswith("  - "):
            Seleccion = Seleccion.removeprefix("  - ")

        analisis_lecciones(Seleccion)

        # Procesar cada elemento de las listas correspondientes
        claves_interes = {"Habilidades", "Elementos", "SubDimensiones Musicales", "Técnicas", "Modos"}

        #for clave in claves_interes:
         #   if clave in Listas_Coincidentes:
          #      for item in Listas_Coincidentes[clave]:
           #         # Llamar a la función y acumular los resultados
            #        Llamada_Lecciones_Objetivos(item, False)

    # LLamar a la función para la búsqueda de lecciones y objetivos
    Llamada_Lecciones_Objetivos(Seleccion, False)

    # Borrado de items repetidos dentro de cada lista.
    for clave, valores in Listas_Coincidentes.items():
        # Convertimos la lista en un conjunto y luego de vuelta a una lista para eliminar duplicados
        Listas_Coincidentes[clave] = list(set(valores))

    
    # Comparar las listas originales con las coincidencias del parámetro seleccionado todas las categorías
    coincidencias_listas(Originales, Listas_Coincidentes, Coincidencias)
    
    # Limpiar Lista_Coincidentes para incluir las coincidencias
    limpiar_listas(*Listas_Coincidentes.values())
                   
    # Pasar las coincidencias a la lista de listas principal
    for nueva_clave, lista_coincidentes in zip(Listas_Coincidentes.keys(), Coincidencias.values()):
        Listas_Coincidentes[nueva_clave].extend(lista_coincidentes)

    return Listas_Coincidentes

            