import os
import json

from typing import Set

# -------------------CATEGORÍAS CENTRALES-------------------

#Habilidades =    ["Agilidad", "Independencia", "Resistencia", "Sensibilidad", "Timing", "Improvisación/Creatividad"]
#Dimensiones Musicales =    ["Ritmo y Breaks", "Armonía y Melodía", "Estructura"]
#SubDimensiones Musicales = ["Signatura/Compás", "Figura Musical", "Grupillos/Dupla", "Escalas", "Acordes", "Prog. de Acordes", "Secciones", "Formas"]
#Tecnicas =     ["Articulaciones", "Fills & Rolls", "Polirritmo", "Rudimentos", "Swing", "Arpegio", "Ornamentos", "Tremolo y Vibrato", "Síncopa"]
#Modos =        ["Libre", "Lineal", "Por Capas", "Cue Point Drumming", "One Handed Drumming", "Layout"]

Categorias = {
    "Habilidades": ["Agilidad", "Independencia", "Resistencia", "Sensibilidad", "Timing", "Improvisación/Creatividad"],
    "Dimensiones Musicales": ["Ritmo y Breaks", "Armonia y Melodia", "Estructura"],
    "SubDimensiones Musicales": ["Signatura/Compas", "Figura Musical", "Grupillos/Dupla", "Escalas", "Acordes", "Progresion de Acordes", "Secciones", "Formas"],
    "Técnicas": ["Articulaciones", "Fills & Rolls", "Polirritmo", "Rudimentos", "Swing", "Arpegios", "Ornamentos", "Tremolo y Vibrato"],
    "Modos": ["Libre", "Lineal", "Por Capas", "Cue Point Drumming", "One Handed Drumming", "Layout"]
}


# ¿CAMBIAR INDEPENDENCIA A COORDINACIÓN?

Categorias_Mejorado = {
    "Habilidades": { 
        "Agilidad": None, # No tiene sublistas por ahora
        "Precisión": None, # No tiene sublistas por ahora
        "Independencia": ["Manos", "Dedos"],
        "Resistencia": None, # No tiene sublistas por ahora
        "Sensibilidad": None, # No tiene sublistas por ahora
        "Improvisación/Creatividad": None, # No tiene sublistas por ahora
        "Concentración": None, # No tiene sublistas por ahora
        "Auditiva": ["Detección del Tono", "Sentido del Ritmo",
                      "Identificación de progresiones armónicas"],
        "Cognitiva": ["Lectura", "Memoria", "Análisis"]
    },
    "Dimensiones Musicales":{ 
        "Ritmo": ["Signatura/Compás", "Figura Musical", "Grupillos/Dupla"],
        "Armonía":{
            "Escalas": ["Mayor", "Menor Natural", "Menor Armónica", 
                        "Menor Melódica Ascendente", "Pentatónica Mayor",
                        "Pentatónica Menor", "Blues"],
            "Modos": ["Jónico (Ionian)", "Dórico (Dorian)","Frigio (Phrygian)", 
                      "Lidio (Lydian)", "Mixolidio (Mixolydian)", "Eólico (Aeolian)",
                      "Locrio (Locrian)"],
            "Acordes": ["Mayor", "Menor", "Disminuido", "Aumentado", "Séptima Mayor", 
                         "Séptima Menor", "Séptima Disminuida", "Séptima Aumentada", 
                         "Mayor Séptima", "Menor Séptima", "Suspensión", 
                         "Acordes de Quinta (Power Chords)", "Acordes de Novena", 
                         "Acordes de Oncena", "Acordes de Treceava"],
            "Progresión de Acordes": None # No tiene sublistas por ahora
        },
        "Estructura": ["Secciones", "Formas", "Desarrollo"],
        "Breaks": None, # No tiene sublistas por ahora
        "Melodía": None # No tiene sublistas por ahora
    },
    "Técnicas": {
        "Articulaciones": ["Staccato", "Legato", "Portato", 
                           ("Tremolo", ["Tremolo rápido", "Tremolo lento"])],
        "Fills & Rolls": ["Fill simple", "Fill complejo",
                          ("Roll de doble bombo", ["Roll rápido", "Roll lento"])],
        "Polirritmo": ["Polirritmo 3 contra 2", "Polirritmo 4 contra 3", 
                       "Polirritmo 5 contra 4"],
        "Rudimentos": ["Paradiddle", "Flam", "Drag",
                       ("Rudimentos de dos manos", ["Double Paradiddle", "Triple Paradiddle"])],
        "Swing": ["Swing clásico", "Swing moderno"],
        "Arpegios": ["Arpegio mayor", "Arpegio menor", "Arpegio disminuido"],
        "Ornamentos": ["Trinos", "Mordentes", "Appogiatura"],
        "Tremolo y Vibrato": ["Tremolo en cuerdas", "Vibrato en cuerdas",
                              ("Tremolo en percusión", ["Tremolo con baquetas", "Tremolo con mazo"])]
    },
    "Modos": ["Libre", "Lineal", "Por Capas", "Cue Point Drumming", "One Handed Drumming", "Layout"]
} # Al terminarlo trasladarlo a la variable "Categorías" -> Hay que añadir más relaciones

# Diccionario principal que almacena todas las listas
# Añadir o quitar aquí las categorías, 
# ya que es la matriz principal de la que dependen las demás
Listas_Coincidentes = {
    "Habilidades": [],
    "Dimensiones Musicales": [],
    "SubDimensiones Musicales": [],
    "Técnicas": [],
    "Modos": [],
    "Calentamiento": [],
    "Fundamentos": [],
    "Desarrollo": [],
    "Improvisación": [],
    "Objetivos": []
}

# -------------------RELACIONES-------------------

a=True
b=False

# NOTA: Se puede reducir a matrices de a y b, sin necesidad de usar el sistema de "if's"

## Descripción de Matrices:

###    | m1 | m2 | m3 | 
###    |----|----|----|
### i1 |    |    |    |
###    |----|----|----|
### i2 |    |    |    |
###    |----|----|----|
### i3 |    |    |    |
###    |----|----|----|


## Entre Habilidades

### 0: Agilidad, 1: Independencia, 2: Resistencia, 3: Sensibilidad, 4: Timing, 5: Improvisación/Creatividad

MatrHH = [[a,a,a,a,a,a],
          [a,a,a,a,a,a],
          [a,a,a,a,a,a],
          [a,a,a,a,a,a],
          [a,a,a,a,a,a],
          [a,a,a,a,a,a]]

RelHH = {
    "Agilidad": {
        "Agilidad": True,
        "Independencia": True,
        "Resistencia": True,
        "Sensibilidad": True,
        "Timing": True,
        "Improvisación/Creatividad": True,
    },
    "Independencia": {
        "Independencia": True,
        "Resistencia": True,
        "Sensibilidad": True,
        "Timing": True,
        "Improvisación/Creatividad": True,
    },
    "Resistencia": {
        "Resistencia": True,
        "Sensibilidad": True,
        "Timing": True,
        "Improvisación/Creatividad": True,
    },
    "Sensibilidad": {
        "Sensibilidad": True,
        "Timing": True,
        "Improvisación/Creatividad": True,
    },
    "Timing": {
        "Timing": True,
        "Improvisación/Creatividad": True,
    },
    "Improvisación/Creatividad": {
        "Improvisación/Creatividad": True,
    }
}



RelHH2 = [["","","","","",""],["","","","","",""],["","","","","",""],["","","","","",""],["","","","","",""],["","","","","",""]]

RelHH2[0][1] = "Facilitar que cada mano/dedo pueda trabajar de forma independiente."
RelHH2[0][2] = "Tocar de forma constante patrones rápidos y complejos."
RelHH2[0][3] = "La habilidad de manos y dedos puede ayudar a tener mayor sensibilidad a la hora de darle a la tecla."
RelHH2[0][4] = "La capacidad de tocar a altas velocidades y tener agilidad ayuda a tener un mejor timing."
RelHH2[0][5] = "Improvisar tocando patrones complejos rápidamente."

RelHH2[1][2] = "Mantener la independencia de manos/dedos de forma constante."
RelHH2[1][3] = "Tocar cada mano/dedo con la intensidad y forma independiente."
RelHH2[1][4] = "Tocar a la vez con timings diferentes en cada mano/dedo."
RelHH2[1][5] = "Improvisar de forma independiente con cada mano."

RelHH2[2][3] = "Mantener el tocar con la intensidad y forma deseada a lo largo del tiempo."
RelHH2[2][4] = "Mantener el timing adecuado de forma prolongada."
RelHH2[2][5] = "Improvisar durante largo tiempo manteniendo el sentido."

RelHH2[3][4] = "Además de tocar con la intensidad y forma adecuada saber hacerlo en el momento adecuado."
RelHH2[3][5] = "Improvisar tocando a distintas intensidades para darle matices."

RelHH2[4][5] = "Mantener el timing tocando sin referencias."


## Habilidad-Dimensión Musical

### i = 0: Agilidad, 1: Independencia, 2: Resistencia, 3: Sensibilidad, 4: Timing, 5: Improvisación
### m = 0: Ritmo, 1: Armonía, 2: Estructura

MatrHDM = [[a,a,a],
          [a,a,a],
          [a,a,a],
          [a,a,b],
          [a,b,b],
          [a,a,a]]

RelHDM = {
    "Agilidad": {
        "Ritmo y Breaks": True,
        "Armonía y Melodía": True,
        "Estructura": True,
    },
    "Independencia": {
        "Ritmo y Breaks": True,
        "Armonía y Melodía": True,
        "Estructura": True,
    },
    "Resistencia": {
        "Ritmo y Breaks": True,
        "Armonía y Melodía": True,
        "Estructura": True,
    },
    "Sensibilidad": {
        "Ritmo y Breaks": True,
        "Armonía y Melodía": True,
        "Estructura": False,
    },
    "Timing": {
        "Ritmo y Breaks": True,
        "Armonía y Melodía": False,
        "Estructura": False,
    },
    "Improvisación/Creatividad": {
        "Ritmo y Breaks": True,
        "Armonía y Melodía": True,
        "Estructura": True,
    },
}

RelHDM2 = [["","",""],["","",""],["","",""],["","",""],["","",""],["","",""]]

RelHDM2[0][0] = "Tocar patrones rítmicos rápidos y/o a BPMs altos."
RelHDM2[0][1] = "Tocar las notas adecuadas en patrones complejos."
RelHDM2[0][2] = "Tocar secuencias complejas en las transiciones y hacer los cambios entre dos partes."

RelHDM2[1][0] = "Tocar ritmos distintos con cada mano y dedo."
RelHDM2[1][1] = "Tocar líneas armónicas distintas en cada mano."
RelHDM2[1][2] = "Tocar fills y redobles de forma independiente en cada mano."

RelHDM2[2][0] = "Tocar patrones rítmicos de forma prolongada."
RelHDM2[2][1] = "Tocar secuencias armónicas de forma prolongada."
RelHDM2[2][2] = "Tocar temas enteros sin cansarme."

RelHDM2[3][0] = "Tocar patrones rítmicos(sea ritmo, riffs, basslines o melodías) con la intensidad y forma deseada."
RelHDM2[3][1] = "Tocar la intensidad y forma de la armonía a voluntad."

RelHDM2[4][0] = "Tocar patrones rítmicos, riffs, basslines y melodías en el momento deseado."

RelHDM2[5][0] = "Improvisar distintos tipos de patrones, tanto rítmicos como riffs y basslines."
RelHDM2[5][1] = "Improvisar progresiones de acordes, arpegios, melodías."
RelHDM2[5][2] = "Poder improvisar cambios de estructuras y piezas enteras."


## Habilidad-Sub-Dimensión Musical

### i = 0: Agilidad, 1: Independencia, 2: Resistencia, 3: Sensibilidad, 4: Timing, 5: Improvisación
### m = 0: "Signatura/Compás", "Figura Musical", "Grupillos/Dupla", "Escalas", "Acordes", "Prog. de Acordes", "Secciones", "Formas"

MatrHSE = [[a,a,a,a,a,a,a,a],
           [a,a,a,a,a,a,a,a],
           [a,a,a,a,a,a,a,a],
           [a,a,a,a,a,a,b,b],
           [a,a,a,b,b,b,b,b],
           [a,a,a,a,a,a,a,b]]


## Habilidad-Técnica

### i = 0: Agilidad, 1: Independencia, 2: Resistencia, 3: Sensibilidad, 4: Timing
### m = 0: Articulaciones, 
###     1: Fills & Rolls, 2: Polirritmo, 3: Rudimentos, 4: Swing
###     5: Arpegios, 6: Ornamentos, 7: Tremolo y Vibrato

MatrHT = [[b,a,b,a,b,a,a,b],
          [b,a,a,a,a,a,a,b],
          [b,a,a,a,a,b,b,b],
          [a,a,a,a,b,a,a,a],
          [b,a,a,a,a,a,a,b],
          [a,a,a,a,a,a,a,a]]


## Habilidad-Modo

### i = 0: Agilidad, 1: Independencia, 2: Resistencia, 3: Sensibilidad, 4: Timing, 5: Improvisación
### m = 0: Libre, 1: Lineal, 2: Por Capas, 3: Cue Point, 4: One Handed Drumming, 5: Layout

MatrHM = [[b,b,b,b,b,b],
          [b,a,b,b,a,b],
          [b,b,b,b,b,b],
          [b,b,b,b,b,b],
          [b,b,b,b,b,b],
          [a,a,a,a,a,a]]


## Dimensión Musical-Sub-Dimensión Musical

### i = 0: "Ritmo y Breaks", "Armonía y Melodía", "Estructura"
### m = 0: "Signatura/Compás", "Figura Musical", "Grupillos/Dupla", "Escalas", "Acordes", "Prog. de Acordes", "Secciones", "Formas"

MatrESE = [[a,a,a,b,b,b,b,b],
           [b,b,b,a,a,a,b,b],
           [b,b,b,b,b,b,a,a]]


## Dimensión Musical-Técnica

### i = 0: Ritmo, 1: Armonía, 2: Estructura
### m = 0: Articulaciones,
###     1: Fills & Rolls, 2: Polirritmo, 3: Rudimentos, 4: Swing
###     5: Arpegios, 6: Ornamentos, 7: Tremolo y Vibrato

MatrET = [[b,a,a,a,a,b,b,b],
          [a,b,b,b,b,a,a,a],
          [b,a,b,b,b,b,b,b]]


## Dimensión Musical-Modo

### i = 0: Ritmo, 1: Armonía, 2: Estructura
### m = 0: Libre, 1: Lineal, 2: Por Capas, 3: Cue Point, 4: One Handed Drumming, 5: Layout

MatrEM = [[b,b,b,b,a,a],
          [b,b,b,b,a,b],
          [b,b,b,b,b,b]]


## Sub-Dimensión Musical-Técnica

### i = 0: "Signatura/Compás", "Figura Musical", "Grupillos/Dupla", "Escalas", "Acordes", "Prog. de Acordes", "Secciones", "Formas"
### m = 0: Articulaciones,
###     1: Fills & Rolls, 2: Polirritmo, 3: Rudimentos, 4: Swing
###     5: Arpegios, 6: Ornamentos, 7: Tremolo y Vibrato

MatrSET = [[b,a,a,a,a,b,b,b],
           [b,a,a,a,a,b,b,b],
           [b,a,a,a,a,b,b,b],
           [a,b,b,b,b,a,a,a],
           [a,b,b,b,b,a,a,a],
           [a,b,b,b,b,a,a,a],
           [b,a,b,b,b,b,b,b],
           [b,b,b,b,b,b,b,b]]


## Sub-Dimensión Musical-Modo

### i = 0: "Signatura/Compás", "Figura Musical", "Grupillos/Dupla", "Escalas", "Acordes", "Prog. de Acordes", "Secciones", "Formas"
### m = 0: Libre, 1: Lineal, 2: Por Capas, 3: Cue Point, 4: One Handed Drumming, 5: Layout

MatrSEM = [[b,b,b,b,a,a],
           [b,b,b,b,a,a],
           [b,b,b,b,a,a],
           [b,b,b,b,a,b],
           [b,b,b,b,a,b],
           [b,b,b,b,a,b],
           [b,b,b,b,b,b],
           [b,b,b,b,b,b]]

# -------------------MATRIZ DE MATRICES-------------------

Matrices_de_Relaciones = {
    cat1: {
        cat2: matriz
        for cat2, matriz in zip(Categorias, fila)
    }
    for cat1, fila in zip(Categorias, [
        [MatrHH, MatrHDM, MatrHSE, MatrHT, MatrHM], 
        [MatrHDM, 0, MatrESE, MatrET, MatrEM],
        [MatrHSE, MatrESE, 0, MatrSET, MatrSEM],
        [MatrHT, MatrET, MatrSET, 0, 0],
        [MatrHM, MatrEM, MatrSEM, 0, 0]
    ])
}


# -------------------INTERFACE-------------------

Interface = ["Todos", "Keys", "Pads"]

# -------------------ESTILOS-------------------
"""
Estilos = ["Todos", "Alt Hip Hop", "Alternative", "Beats", "Boogie", "Calypso", "Chiptune",
           "Cinematic", "Classic Break", "Classical", "Dancehall", "Disco", "DnB",
           "Dub", "Dubstep", "EDM", "Electronic", "Footwork", "Funk", "Future Bass", 
           "Grime", "Hip Hop", "House", "Jazz", "Juke", "Jungle", "Modern Funk", 
           "New Jack Swing", "Pop", "Rap", "Reggae", "RnB", "Rock", "Soul", "Techno", "Trap", 
           "UK Garage"]
"""

all_tags: Set[str] = set()

# Folder where the script is located
carpeta_nota = os.path.dirname(os.path.abspath(__file__))

# Path to a folder named 'Lessons' in the same folder
path_relativo = os.path.join(carpeta_nota, 'Lecciones')

for root, _, files in os.walk(path_relativo):
    for file_name in files:
        if file_name.endswith(".json"):
            file_path = os.path.join(root, file_name)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if "data" in data and isinstance(data["data"], dict):
                        tags = data["data"].get("genres")
                        if isinstance(tags, list):
                            for tag in tags:
                                if isinstance(tag, str):
                                    all_tags.add(tag.strip())
            except (json.JSONDecodeError, UnicodeDecodeError, OSError):
                continue

Estilos = sorted(all_tags)


# -------------------VARIABLES/DICCIONARIOS-------------------

# Lista acumulativa de elementos seleccionados
selecciones_por_listbox = {}

# Diccionario que registra las lecciones (como claves/keys) junto con los elementos escogidos coincidentes (items)
Lecciones = {}

# Diccionario que registra las lecciones seleccionadas
Lecciones_Seleccionadas = {}

