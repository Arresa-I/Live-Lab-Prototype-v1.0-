import os
from Información import *

# -------------------DEFINICIÓN DE VARIABLES-------------------
full_file = ""
filedata_lines = []
lista_categorias = []

# -------------------FUNCIONES AUXILIARES-------------------

def Borrado_Listas(Lista):
    """Limpia todas las listas proporcionadas."""
    for lst in Lista:
        lst.clear()

def Llamada_Lecciones_Objetivos(Parametro, Borrado):
    # LLamar a la función para la búsqueda de lecciones

    # Carpeta base donde esta nota se encuentra
    carpeta = os.path.dirname(os.path.abspath(__file__))

    # Path a la carpeta "Lecciones"
    Path = os.path.join(carpeta, 'Lecciones')

    Muestra_Opciones_Ar2(
        Path, 
        Parametro,
        [Listas_Coincidentes["Calentamiento"], 
        Listas_Coincidentes["Fundamentos"], 
        Listas_Coincidentes["Desarrollo"]],
        ["Calentamiento", "Fundamentos", "Desarrollo"],
        Borrado
    )

    # Llamar a la función para la búsqueda de objetivos

    # Path a la carpeta "Objetivos"
    Path = os.path.join(carpeta, 'Objetivos')
    Muestra_Opciones_Ar(Path, Parametro, [Listas_Coincidentes["Objetivos"]], ["Objetivos"], Borrado)
    
# -------------------FUNCIÓN CATEGORÍAS-------------------
def Muestra_Opciones_Cat(indice):
    # Limpiar las listas de coincidencias
    Borrado_Listas(Listas_Coincidentes.values())  
    
    Relaciones = {
        "Habilidades": {"Habilidades": 1, "Dimensiones Musicales": 1, "SubDimensiones Musicales": 1, "Técnicas": 1, "Modos": 1},
        "Dimensiones Musicales": {"Habilidades": -1, "Dimensiones Musicales": 0, "SubDimensiones Musicales": 1, "Técnicas": 1, "Modos": 1},
        "SubDimensiones Musicales": {"Habilidades": -1, "Dimensiones Musicales": -1, "SubDimensiones Musicales": 0, "Técnicas": 1, "Modos": 1},
        "Técnicas": {"Habilidades": -1, "Dimensiones Musicales": -1, "SubDimensiones Musicales": -1, "Técnicas": 0, "Modos": 0},
        "Modos": {"Habilidades": -1, "Dimensiones Musicales": -1, "SubDimensiones Musicales": -1, "Técnicas": 0, "Modos": 0}
    }
    
    # Recorrer las relaciones según la categoría central
    for categoria_destino, relacion in Relaciones.get(indice[0], {}).items():
        for n in range(len(Categorias[categoria_destino])):  # Iterar sobre las categorías destino
            if (
                relacion == 1 
                and Matrices_de_Relaciones[indice[0]][categoria_destino][indice[1]][n]
            ):
                Listas_Coincidentes[categoria_destino].append(Categorias[categoria_destino][n])
            elif (
                relacion == -1 
                and Matrices_de_Relaciones[indice[0]][categoria_destino][n][indice[1]]
            ):
                Listas_Coincidentes[categoria_destino].append(Categorias[categoria_destino][n])

    # Agregar la categoría central si no es "Habilidades" (la primera)
    if indice[0] != "Habilidades":
        Listas_Coincidentes[indice[0]].append(Categorias[indice[0]][indice[1]])

    return Listas_Coincidentes


# -------------------FUNCIÓN BUSCAR EN ARCHIVOS-------------------
def Muestra_Opciones_Ar(Path, Elemento_Central, Listas_Incluidas, Terminos, Borrado=True):
    if Borrado:
        Borrado_Listas(Listas_Incluidas)

    for root, _, files in os.walk(Path):
        for file_name in files:
            if file_name.endswith(".md"):  # Check if it's a markdown file
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r', encoding='utf-8') as file:
                    filedata_lines = file.readlines()
                    count, Incluir, Lista = 0, False, []

                    for linea in filedata_lines:
                        if "---" in linea:
                            count += 1
                            if count == 2:
                                break

                        if Elemento_Central in linea:
                            Incluir = True
                        
                        for item in Terminos:               
                            if Terminos.index(item) not in Lista:
                                Lista.append(Terminos.index(item))
                    
                    if Incluir:
                        for lista in Lista:
                            Listas_Incluidas[lista].append(file_name.split('.')[0])

                        if file_name.split('.')[0] not in Lecciones:
                            Lecciones[file_name.split('.')[0]] = set()
                        Lecciones[file_name.split('.')[0]].add(Elemento_Central)

    return Listas_Incluidas, Lecciones

def Muestra_Opciones_Ar2(Path, Elemento_Central, Listas_Incluidas, Terminos, Borrado=True):
    if Borrado:
        Borrado_Listas(Listas_Incluidas)

    for root, _, files in os.walk(Path):
        for file_name in files:
            if file_name.endswith(".json"):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    if "data" not in data or not isinstance(data["data"], dict):
                        return

                    tags = data["data"].get("tags", [])
                    grade = data["data"].get("grade", [])
                    genres = data["data"].get("genres", [])

                    # Normalizar valores no lista a lista
                    if not isinstance(tags, list):
                        tags = [tags]
                    if not isinstance(grade, list):
                        grade = [grade]
                    if not isinstance(genres, list):
                        genres = [genres]

                    # Concatenar
                    tags = tags + grade + genres
                    
                    Incluir = Elemento_Central in json.dumps(tags)

                    Lista = []
                    
                    if Incluir:
                        for item in Terminos:
                            if item in tags:
                                Lista.append(Terminos.index(item))

                        for lista in Lista:
                            Listas_Incluidas[lista].append(file_name.split('.')[0])

                        if file_name.split('.')[0] not in Lecciones:
                            Lecciones[file_name.split('.')[0]] = set()
                        Lecciones[file_name.split('.')[0]].add(Elemento_Central)

    return Listas_Incluidas, Lecciones

# -------------------FUNCIÓN ANÁLISIS FICHAS-------------------
def analisis_lecciones(file):

    full_file = ""

    # Carpeta donde está el código
    carpeta_nota = os.path.dirname(os.path.abspath(__file__))

    # Path a la carpeta de Lecciones
    path = os.path.join(carpeta_nota, 'Lecciones')

    # Construimos la ruta completa y verificamos su existencia

    for root, _, files in os.walk(path):
        if f"{file}.json" in files:
            full_file = os.path.join(root, f"{file}.json")
            break  # Opcional: detener al encontrar el primero
    
    if full_file:
        # Leer el contenido del archivo
        with open(full_file, 'r', encoding='utf-8') as file:
            data = json.load(file)

            tags = data.get("data", {}).get("tags", [])
            if not isinstance(tags, list):
                tags = []

            for categoria_nombre, categoria_list in Categorias.items():
                if categoria_nombre in Listas_Coincidentes:
                    for categoria in categoria_list:
                        if categoria in tags and categoria not in Listas_Coincidentes[categoria_nombre]:
                            Listas_Coincidentes[categoria_nombre].append(categoria)

    # Retornar todas las listas del diccionario en forma de tuplas
    return {clave: Listas_Coincidentes[clave] for clave in ["Habilidades", "Dimensiones Musicales", "SubDimensiones Musicales", "Técnicas", "Modos"]}