from tkinter import *
from tkinter import ttk
import tkinter as tk
from collections import defaultdict
import re

# Importaciones de módulos separados, para dividir funcionalidades
import Información
from Funciones_Principales import *


# -------------------VENTANA PRINCIPAL-------------------

main = Tk()
main.title("Organización Live")
main.geometry("1450x850")

# -------------------IMPORTAR VARIABLES-------------------

Categorias = Información.Categorias

# -------------------FUNCIONES AUXILIARES-------------------

# Función auxiliar para crear etiquetas en una ubicación específica dentro de un frame
def crear_label(texto, fila, columna, frame):
    label = Label(frame, text=texto)
    label.grid(row=fila, column=columna, padx=5, pady=5, sticky="w")
    return label

# Función auxiliar para crear Listboxes en una ubicación específica
def crear_listbox(fila, columna, frame, width=30, height=12):
    listbox = Listbox(frame, width=width, height=height)
    listbox.grid(row=fila, column=columna, padx=5, pady=5)
    return listbox

def Borrado_Resultado(Lista):
    for item in Lista:
        item.delete(0, END)

def Reorganizar_Coincidentes(Listas_Coincidentes_Lecciones):
    """ Reorganiza los elementos de 'Calentamiento', 'Fundamentos' y 'Desarrollo' en Listas_Coincidentes
    añadiendo la categoría de la agrupación a cada ítem según los elementos en Lecciones. """

    # Diccionario para agrupar claves por valores únicos
    agrupado = defaultdict(list)
    agrupado.clear()

    for clave, valores in Lecciones.items():
        # Convertimos la lista de valores en tupla para que sea hashable
        if len(valores) == 1:
            valor = next(iter(valores))  # Extraer el único valor del set/lista
            agrupado[valor].append(clave)
        else:
            agrupado[tuple(valores)].append(clave)

    # Paso 1: Ordenar por número de elementos en la tupla
    ordenado_por_elementos = sorted(
        agrupado.items(),
        key=lambda x: len(x[0]),
    )

    # Convertir a diccionario ordenado
    agrupado_ordenado = dict(ordenado_por_elementos)

    # Iterar por las claves específicas de Listas_Coincidentes 
    for grupo, valores in agrupado_ordenado.items():
        for clave in ["Calentamiento", "Fundamentos", "Desarrollo"]:
            for item in Listas_Coincidentes.get(clave, []):  # Asegurar que existe la clave en Listas_Coincidentes
                # Buscar el grupo (key) en agrupado_ordenado donde aparece el ítem
                if item in valores:
                    # Si el grupo no existe en Listas_Coincidentes_Lecciones[clave], crearlo
                    if grupo not in Listas_Coincidentes_Lecciones[clave]:
                        Listas_Coincidentes_Lecciones[clave][grupo] = []
                    # Agregar el ítem al grupo correspondiente dentro de Listas_Coincidentes_Lecciones
                    Listas_Coincidentes_Lecciones[clave][grupo].append(item)


    return Listas_Coincidentes_Lecciones

def Escritura_Resultado():

    ## OBTENCIÓN DE Listas_Coincidentes_Lecciones
    # Estructura correcta de Listas_Coincidentes_Lecciones
    Listas_Coincidentes_Lecciones = {
        "Calentamiento": defaultdict(list),
        "Fundamentos": defaultdict(list),
        "Desarrollo": defaultdict(list)
    }    

    # 🔹 Reorganizar los ítems antes de escribirlos
    Reorganizar_Coincidentes(Listas_Coincidentes_Lecciones)

    # Convertir defaultdict en diccionario normal para evitar problemas en otros procesos
    Listas_Coincidentes_Lecciones = {k: dict(v) for k, v in Listas_Coincidentes_Lecciones.items()}

    ## TRASLADAR LOS RESULTADOS  Listas_Coincidentes_Final
    Listas_Coincidentes_Final = Listas_Coincidentes.copy()

    # Reemplazar los valores en Listas_Coincidentes_Final por los de Listas_Coincidentes_Lecciones
    for clave in ["Calentamiento", "Fundamentos", "Desarrollo"]:
        if clave in Listas_Coincidentes_Lecciones:
            Listas_Coincidentes_Final[clave] = []  # Reiniciar clave en Final
            
            for grupo, items in Listas_Coincidentes_Lecciones[clave].items():
                # Agregar el grupo
                # Transformamos la tupla en un string y aplicamos las sustituciones
                grupo_str = str(grupo)
                if grupo_str.count(',') == 1 and grupo_str.endswith(',)'):
                    # Caso especial: solo una dupla
                    grupo_limpio = grupo_str.strip('(),')
                else:
                    grupo_limpio = re.sub(r",\s*", " + ", grupo_str)  # Reemplaza "," por " + "
                    
                grupo_limpio = re.sub(r"[()']", "", grupo_limpio)  # Elimina paréntesis y comillas simples
                grupo_limpio = grupo_limpio.strip()  # Elimina espacios en blanco al inicio y al final

                # Añadir al diccionario con el formato limpio
                Listas_Coincidentes_Final[clave].append(f"{grupo_limpio}:")
      
                # Agregar los ítems con sangría
                for item in items:
                    Listas_Coincidentes_Final[clave].append(f"  - {item}")

    ## ESCRIBIR LOS RESULTADOS
    claves = list(Listas_Coincidentes_Final.keys())
    valores = list(Listas_Coincidentes_Final.values())
    
    # Iterar sobre Lista_Resultado y asignar los valores correspondientes
    for lista_resultado, clave, lista_coincidentes in zip(Lista_Resultado, claves, valores):
        # Limpiar primero la lista_resultado antes de insertar nuevos valores
        lista_resultado.delete(0, END)  # Asume que `lista_resultado` es un Listbox de tkinter
        # Insertar los valores de la lista coincidente correspondiente
        for item in lista_coincidentes:
            lista_resultado.insert(END, item)

    # Resaltar el elemento central directamente en los Listbox (si aplica) -> Solo se aplica a los listbox pertenecientes a los ítems seleccionados
    for listbox, seleccionados in selecciones_por_listbox.items():
        # Obtener los elementos actuales del listbox
        items_actuales = listbox.get(0, "end")

        if listbox not in Lista_Resultado[5:8]:
            nuevos_items = list(seleccionados) + [item for item in items_actuales if item not in seleccionados]
        else:
            nuevos_items =  [item for item in items_actuales]

        # Limpiar el listbox y volver a llenarlo con los elementos ordenados
        
        listbox.delete(0, "end")
        for idx, item in enumerate(nuevos_items):
            listbox.insert("end", item)

        # Aplicar colores: Elemento Central en naranja, otros seleccionados en azul
        for i, item in enumerate(nuevos_items):
            if item == Elemento_Central and not item.startswith("  - "):
                listbox.itemconfig(i, {'bg': 'orange'})  # Elemento Central en naranja
            elif item in seleccionados and listbox in Lista_Resultado[0:5]:
                listbox.itemconfig(i, {'bg': 'lightblue'})  # Otros seleccionados en azul
            elif item in seleccionados and listbox in Lista_Resultado[5:8]:
                listbox.itemconfig(i, {'bg': 'lightgreen'})  # Otros seleccionados en azul
            else:
                listbox.itemconfig(i, {'bg': 'white'})  # Resto en blanco

    # Resaltar el elemento central directamente en los Listbox (si aplica) -> Solo se aplica a los listbox de lecciones
    for listbox_actual in Lista_Resultado[5:8]:
        items_actuales = listbox_actual.get(0, "end")

        for i, item in enumerate(items_actuales):
            if Elemento_Central in item and not item.startswith("  - "):
                listbox_actual.itemconfig(i, {'bg': 'orange'})  # Elemento Central en naranja
            else:
                encontrado = False
                for listbox_sel, seleccionados in selecciones_por_listbox.items():
                    if any(s in item for s in seleccionados) and listbox_sel in Lista_Resultado[0:5]:
                        encontrado = True
                        break

                if encontrado and not item.startswith("  - "):
                    listbox_actual.itemconfig(i, {'bg': 'lightblue'})  # Otros seleccionados en azul

    ## ESCRIBIR LAS LECCIONES DECIDIDAS
    # Preparar lecciones seleccionadas
    #Lecciones_Seleccionadas.clear()

    listbox_map = {
        str(Lista_Resultado[5]): str(listboxes_3[0]),
        str(Lista_Resultado[6]): str(listboxes_3[1]),
        str(Lista_Resultado[7]): str(listboxes_3[2]),
    }

    for listbox, seleccionados in selecciones_por_listbox.items():
        if str(listbox) in listbox_map:
            if listbox not in Lecciones_Seleccionadas:
                Lecciones_Seleccionadas[listbox] = {}  # Ahora será un dict de subclaves

            for item in seleccionados:
                # Buscar la subclave a la que pertenece este item
                subclave_encontrada = None
                for clave, lista in Listas_Coincidentes_Lecciones.items():
                    for subclave, sublista in lista.items(): 
                        if item.removeprefix("  - ") in sublista:
                            subclave_encontrada = subclave
                            break

                if subclave_encontrada is not None:
                    # Inicializar subclave si no existe
                    if subclave_encontrada not in Lecciones_Seleccionadas[listbox]:
                        Lecciones_Seleccionadas[listbox][subclave_encontrada] = set()

                    # Evitar duplicados
                    if item not in {texto for texto, _ in Lecciones_Seleccionadas[listbox][subclave_encontrada]}:
                        Lecciones_Seleccionadas[listbox][subclave_encontrada].add((item, False))

    for listbox, categorias in Lecciones_Seleccionadas.items():
        # Copiamos las claves para iterar sin problemas
        claves = list(categorias.keys())
        
        # Iteramos sobre todas las combinaciones
        for clave in claves:
            for otra_clave in claves:
                if clave == otra_clave:
                    continue
                
                # Convertimos todo a tupla para comparar fácilmente
                clave_t = clave if isinstance(clave, tuple) else (clave,)
                otra_t = otra_clave if isinstance(otra_clave, tuple) else (otra_clave,)
                
                # Si todos los elementos de la clave están en otra_clave (clave incluida en otra_clave)
                if all(elem in otra_t for elem in clave_t):
                    # Fusionamos lecciones en la clave más completa
                    categorias[otra_clave].update(categorias[clave])
                    # Eliminamos la clave más simple
                    del categorias[clave]
                    break

     
    # Escribir las lecciones seleccionadas en los listboxes destino
    for origen_listbox, subclaves in Lecciones_Seleccionadas.items(): 
        destino_nombre = listbox_map.get(str(origen_listbox))
        if destino_nombre:
            for listbox3 in listboxes_3:
                if str(listbox3) == destino_nombre:
                    listbox3.delete(0, END)
                    
                    for subclave, seleccionados in subclaves.items():
                        clave_str = str(subclave)
                        if subclave.count(',') == 1:
                            clave_limpio = subclave
                        else:
                            clave_limpio = re.sub(r",\s*", " + ", clave_str)  # Reemplaza "," por " + "
                            clave_limpio = re.sub(r"[()']", "", clave_limpio)

                        listbox3.insert("end", f"{clave_limpio}:")  # Encabezado del bloque
                        for item, _ in seleccionados:
                            listbox3.insert("end", item)

#------------------------------------------------------------
# -------------------FUNCIONES PRINCIPALES-------------------
#------------------------------------------------------------

# Función de búsqueda primaria

def Funcion_Busqueda(value_inside, tipo="elemento"):
    global Elemento_Central, Leccion_Central  # Indicar variables globales si es necesario
    Borrado_Resultado(Lista_Resultado)
    selecciones_por_listbox.clear()
    Lecciones.clear()

    # Determinar qué tipo de búsqueda se realiza
    if tipo == "musical":
        Elemento_Central = value_inside.get()
        Mostrar_Resultados_Musical(Elemento_Central)

        # Encontrar en qué categoría está el Elemento Central
        listbox_index = None
        for idx, (categoria, elementos) in enumerate(Categorias.items(), start=1):
            if Elemento_Central in elementos:
                listbox_index = idx - 1  # Índice del listbox correcto (0 a 4)
                break

        # Agregar a selecciones_por_listbox si corresponde
        if listbox_index is not None and listbox_index < len(listboxes):
            listbox = listboxes[listbox_index]
            if listbox not in selecciones_por_listbox:
                selecciones_por_listbox[listbox] = set()
            selecciones_por_listbox[listbox].add(Elemento_Central)

    elif tipo == "leccion":
        Elemento_Central = value_inside.get()
        Mostrar_Resultados_Leccion(Elemento_Central)

    Escritura_Resultado()  # Aplicar los cambios en los Listbox

#----------------------------------------------
# Función que maneja la selección en cualquier Listbox
#----------------------------------------------

def on_select(event):
    # Obtener el Listbox que disparó el evento
    listbox_actual = event.widget
    
    # Si el Listbox no está en el diccionario, inicializamos su conjunto de selecciones
    if listbox_actual not in selecciones_por_listbox:
        selecciones_por_listbox[listbox_actual] = set()

    # Obtener los índices seleccionados en el evento actual
    indices_seleccionados = listbox_actual.curselection()

    # Obtener los elementos seleccionados actuales
    seleccionados = {listbox_actual.get(i) for i in indices_seleccionados}
    #seleccionados = {listbox_actual.get(i).removeprefix("  - ") for i in indices_seleccionados}
    
    # Actualizar las selecciones acumuladas para este Listbox
    selecciones_por_listbox[listbox_actual].update(seleccionados)

    # Llamar a la función de procesamiento con los ítems seleccionados
    if seleccionados:
        # Procesar el primer ítem seleccionado (como ejemplo)
        combinacion(next(iter(seleccionados)))
        Escritura_Resultado()

#----------------------------------------------
# Funciones sobre las lecciones seleccionadas
#----------------------------------------------

def accion_1(): # Borrado de las lecciones
    global Lecciones_Seleccionadas
    for listbox in listboxes_3:
        listbox.delete(0, END)

    listbox_map = {
        str(Lista_Resultado[5]): str(listboxes_3[0]),
        str(Lista_Resultado[6]): str(listboxes_3[1]),
        str(Lista_Resultado[7]): str(listboxes_3[2]),
    }

    # Borrar ítems seleccionados de los listboxes lectivos
    for listbox, seleccionados in selecciones_por_listbox.items():
        if str(listbox) in listbox_map:
            selecciones_por_listbox[listbox].clear()

    # Borrar los ítems de Lecciones_Seleccionadas asignados como False
    # Crear nuevo dict limpio
    nuevas_lecciones = {}

    for listbox, subdict in Lecciones_Seleccionadas.items():
        nuevo_subdict = {}

        for subclave, items in subdict.items():
            verdaderos = {(texto, estado) for texto, estado in items if estado is True}
            if verdaderos:
                nuevo_subdict[subclave] = verdaderos

        if nuevo_subdict:
            nuevas_lecciones[listbox] = nuevo_subdict

    # Reemplazar original
    Lecciones_Seleccionadas = nuevas_lecciones


    # Escribir las lecciones seleccionadas en los listboxes destino
    for origen_listbox, subdict in Lecciones_Seleccionadas.items():
        destino_nombre = listbox_map.get(str(origen_listbox))
        if destino_nombre:
            for listbox3 in listboxes_3:
                if str(listbox3) == destino_nombre:
                    listbox3.delete(0, END)

                    for subclave, seleccionados in subdict.items():
                        clave_str = str(subclave)
                        if subclave.count(',') == 1:
                            clave_limpio = subclave
                        else:
                            clave_limpio = re.sub(r",\s*", " + ", clave_str)  # Reemplaza "," por " + "
                            clave_limpio = re.sub(r"[()']", "", clave_limpio)

                        listbox3.insert("end", f"{clave_limpio}:")  # Encabezado del bloque
                        for item, _ in seleccionados:
                            listbox3.insert("end", item)

def accion_2(): # Fijado de las lecciones
    for listbox, subdict in Lecciones_Seleccionadas.items():
        for subclave, items in subdict.items():
            nuevos_items = {(texto, True) for texto, _ in items}
            Lecciones_Seleccionadas[listbox][subclave] = nuevos_items


def borrado_general():
    Borrado_Resultado(Lista_Resultado)
    Borrado_Resultado(listboxes_3)
    selecciones_por_listbox.clear()
    Lecciones.clear()
    Lecciones_Seleccionadas.clear()


# -------------------ORGANIZACIÓN DE FRAMES Y ELEMENTOS-------------------

# Crear el frame principal para organización en columnas
frame_opciones = Frame(main)
frame_opciones.grid(row=0, column=0, rowspan=3, sticky="nw")


frame_resultados = Frame(main)
frame_resultados.grid(row=0, column=1, columnspan=5, sticky="nw")

# Crear los elementos en la columna de opciones
Label(frame_opciones, text="Opciones").grid(row=0, column=0, sticky="w")
value_inside1 = [StringVar(main), StringVar(main), StringVar(main)]
value_inside1[0].set("El. Musical Central")

# Menubutton "Elemento Central"
menubutton_elemento = Menubutton(frame_opciones, textvariable=value_inside1[0], indicatoron=True,
                                 borderwidth=2, relief="raised", width=20)
main_menu = Menu(menubutton_elemento, tearoff=False)
menubutton_elemento.configure(menu=main_menu)

# Crear opciones para el menubutton usando las categorías del diccionario
for categoria, items in Categorias.items():
    menu = Menu(main_menu, tearoff=False)
    main_menu.add_cascade(label=categoria, menu=menu)
    for item in items:
        menu.add_radiobutton(
            label=item,
            value=item,
            variable=value_inside1[0],
            command=lambda: Funcion_Busqueda(value_inside1[0], tipo="musical")  # Usar `item` en el lambda
        )

# Posicionar el menubutton
menubutton_elemento.grid(row=0, column=0, sticky="nw", pady=(0, 10))  # Añadir espacio debajo

# Menubutton "Lección Central"
value_inside1.append(StringVar(main))  # Añadir una nueva variable para "Lección Central"
value_inside1[1].set("El. Lectivo Central")

menubutton_leccion = Menubutton(frame_opciones, textvariable=value_inside1[1], indicatoron=True,
                                borderwidth=2, relief="raised", width=20)
leccion_menu = Menu(menubutton_leccion, tearoff=False)
menubutton_leccion.configure(menu=leccion_menu)

# Crear opciones para el menubutton usando categorías
for item in (("Interface", *Interface), ("Nivel", "Todos", "Fácil", "Intermedio", "Difícil"), 
             ("Estilo", *Estilos)):
    menu = Menu(leccion_menu, tearoff=False)
    leccion_menu.add_cascade(label=item[0], menu=menu)

    if item[0] == "Nivel":
        # Opción "Todos"
        menu.add_radiobutton(
            label="Todos",
            variable=value_inside1[1],
            value="Todos",
            command=lambda: Funcion_Busqueda(value_inside1[1], tipo="leccion")
        )

        # Submenú para "Fácil"
        facil_menu = Menu(menu, tearoff=False)
        menu.add_cascade(label="Fácil", menu=facil_menu)
        for i in range(1, 6):
            facil_menu.add_radiobutton(
                label=str(i),
                variable=value_inside1[1],
                value=str(i),
                command=lambda: Funcion_Busqueda(value_inside1[1], tipo="leccion")
            )

        # Submenú para "Intermedio"
        intermedio_menu = Menu(menu, tearoff=False)
        menu.add_cascade(label="Intermedio", menu=intermedio_menu)
        for i in range(6, 11):
            intermedio_menu.add_radiobutton(
                label=str(i),
                variable=value_inside1[1],
                value=str(i),
                command=lambda: Funcion_Busqueda(value_inside1[1], tipo="leccion")
            )

        # Submenú para "Difícil"
        dificil_menu = Menu(menu, tearoff=False)
        menu.add_cascade(label="Difícil", menu=dificil_menu)
        for i in range(11, 16):
            dificil_menu.add_radiobutton(
                label=str(i),
                variable=value_inside1[1],
                value=str(i),
                command=lambda: Funcion_Busqueda(value_inside1[1], tipo="leccion")
            )

    else:
        # Para otras categorías como Interface y Estilo
        for value in item[1:]:
            menu.add_radiobutton(
                value=value,
                label=value,
                variable=value_inside1[1],
                command=lambda: Funcion_Busqueda(value_inside1[1], tipo="leccion")
            )

menubutton_leccion.grid(row=1, column=0, sticky="nw", pady=(0, 10))  # Añadir espacio extra debajo

# Botones sobre las lecciones seleccionadas

boton1 = tk.Button(frame_opciones, text="Borrar Lecciones", command=accion_1)
boton1.grid(row=2, column=0, padx=10, pady=5)

boton2 = tk.Button(frame_opciones, text="Fijar Lecciones", command=accion_2)
boton2.grid(row=3, column=0, padx=10, pady=5)

# Botón para el borrado general

boton3 = tk.Button(frame_opciones, text="Borrado General", command=borrado_general)
boton3.grid(row=4, column=0, padx=10, pady=5)

# Crear las etiquetas y listboxes en las columnas de resultados
headers = ["Habilidades", "Dimensiones Musicales", "Sub-Dimensiones Musicales", "Técnicas", "Modos"]
listboxes = []

# Crear los listboxes de la 1º fila: Elementos musicales
for i, header in enumerate(headers):
    crear_label(header, 0, i, frame_resultados)
    listbox = crear_listbox(1, i, frame_resultados, width=40, height=12)
    listbox.bind("<<ListboxSelect>>", on_select)  # Vincular el evento de selección
    listboxes.append(listbox)

# Segunda fila de resultados
headers_2 = ["Calentamiento (Lecciones)", "Fundamentos (Lecciones)", "Desarrollo (Lecciones)", "Improvisacion (Lecciones)", "Objetivos (Lecciones)"]
listboxes_2 = []

# Crear los listboxes de la 2º fila: Lecciones y objetivos resultado
for i, header in enumerate(headers_2):
    crear_label(header, 2, i, frame_resultados)
    listbox = crear_listbox(3, i, frame_resultados, width=40, height=20)
    listbox.bind("<<ListboxSelect>>", on_select)  # Vincular el evento de selección
    listboxes_2.append(listbox)

# Guardar listboxes en Lista_Resultado para ser referenciados en otras funciones
Lista_Resultado = listboxes + listboxes_2

# Crear las etiquetas y listboxes en las columnas de resultados
headers = ["Calentamiento (Rutina)", "Fundamentos (Rutina)", "Desarrollo (Rutina)", "Improvisacion (Rutina)", "Objetivos (Rutina)"]
listboxes_3 = []

# Crear los listboxes de la 3º fila: Selección de la rutina
for i, header in enumerate(headers):
    crear_label(header, 4, i, frame_resultados)
    listbox = crear_listbox(5, i, frame_resultados, width=40, height=12)
    listbox.bind("<<ListboxSelect>>", on_select)  # Vincular el evento de selección
    listboxes_3.append(listbox)

# Ejecutar ventana
main.mainloop()
