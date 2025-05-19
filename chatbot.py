'''
-----------------------------------------------------------------------------------------------
Título: ChatBot Contable
Fecha: Mayo 2025
Autor: Equipo Junior Dev

Descripción:
Chatbot que responde preguntas frecuentes a partir de coincidencia por palabras clave.
Permite agregar nuevas preguntas, buscar por tema libre y evita respuestas erróneas.
-----------------------------------------------------------------------------------------------
'''
#----------------------------------------------------------------------------------------------
# MÓDULOS
#----------------------------------------------------------------------------------------------

import csv
import unicodedata
import os

#----------------------------------------------------------------------------------------------
# FUNCIONES
#----------------------------------------------------------------------------------------------

#Carpeta donde estan guardadas la preguntas y respuestas
archivo_csv = "../data/preg.csv"

#Diccionario de sinónimos
sinonimos = {
    "salario": ["sueldo", "remuneracion", "honorarios", "paga"],
    "vacaciones": ["licencia", "descanso", "feriado"],
    "trabajo": ["empleo", "laburo", "oficio"],
    "dinero": ["plata", "efectivo", "cash"],
    "monotributo": ["monotributista", "monotribut"],
    "factura": ["comprobante", "recibo", "ticket", "boleta", "fact"],
    "empresa": ["compañía", "firma", "sociedad", "negocio"],
    "contador": ["contador público", "profesional contable"],
    "IVA": ["impuesto al valor agregado", "impuesto", "impuestos"],
    "pago": ["abono", "cuota", "cancelación"],
    "empleado": ["trabajador", "personal", "colaborador"],
    "responsable inscripto": ["inscripto", "contribuyente", "registrado"],
}

def quitar_tildes(texto):
    """
    Funcion para quitar tildes y acentos de un texto
    """
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )

def normalizar(texto):
    """
    Convierte el texto a una forma estándar: minúsculas, sin tildes ni signos
    """
    return quitar_tildes(texto.lower().strip(" ¿?"))

def obtener_palabra_canonica(palabra):
    """
    Recibe una palabra y devuelve su version 'oficial' segun el diccionario de sinonimos
    """
    palabra = normalizar(palabra)
    for canonica, lista in sinonimos.items():
        if palabra == canonica or palabra in lista:
            return canonica
    return palabra

def buscar_respuesta(pregunta_usuario):
    """
    Busca una pregunta exacta en el archivo y devuelve la respuesta correspondiente 
    """
    pregunta_usuario = normalizar(pregunta_usuario)
    with open(archivo_csv, newline='', encoding='utf-8') as archivo:
        lector = csv.reader(archivo, delimiter=';')
        for fila in lector:
            if len(fila) >= 2:
                pregunta, respuesta = fila
                if normalizar(pregunta) == pregunta_usuario:
                    return respuesta.strip()
    return None

def buscar_por_palabras_clave(pregunta_usuario):
    """
    Busca la mejor respuesta basandose en la coincidencia por palabras clave
    """
    pregunta_usuario = normalizar(pregunta_usuario)
    palabras_usuario = set(obtener_palabra_canonica(p) for p in pregunta_usuario.split())

    mejor_coincidencia = None
    mejor_pregunta = None
    mejor_ratio = 0

    try:
        with open(archivo_csv, newline='', encoding='utf-8') as archivo:
            lector = csv.reader(archivo, delimiter=';')
            for fila in lector:
                if len(fila) >= 2:
                    pregunta, respuesta = fila
                    palabras_pregunta = set(obtener_palabra_canonica(p) for p in normalizar(pregunta).split())
                    coincidencias = palabras_usuario.intersection(palabras_pregunta)
                    total_palabras = len(palabras_usuario.union(palabras_pregunta))

                    if total_palabras > 0:
                        ratio = len(coincidencias) / total_palabras
                        if ratio > mejor_ratio:
                            mejor_ratio = ratio
                            mejor_coincidencia = respuesta.strip()
                            mejor_pregunta = pregunta.strip()

        #Devuelve la mejor respuesta encontrada solo si la coincidencia es al menos 30%
        if mejor_ratio >= 0.3:
            print(f"(Usuario: '{mejor_pregunta}')")
            return mejor_coincidencia
        return None
    except FileNotFoundError:
        print("Error: No se encontró el archivo de preguntas.")
        return None
    except Exception as e:
        print("Error inesperado al leer las preguntas:", e)
        return None

def agregar_pregunta_respuesta(pregunta, respuesta):
    """
    Agrega pregunta en caso que no se encuentre en el archivo
    """
    try:
        with open(archivo_csv, mode='a', newline='', encoding='utf-8') as archivo:
            escritor = csv.writer(archivo, delimiter=';')
            escritor.writerow([pregunta.strip(), respuesta.strip()])
    except Exception as e:
        print("Error al guardar la nueva pregunta:", e)


#----------------------------------------------------------------------------------------------
# CUERPO PRINCIPAL
#----------------------------------------------------------------------------------------------

def main():
    """
    Función principal del programa. Muestra el menú y gestiona la interacción con el usuario.
    """
    #Verifica si el archivo existe antes de continuar
    if not os.path.exists(archivo_csv):
        print(f"El archivo '{archivo_csv}' no existe. El programa no puede continuar.")
        input("Presione Enter para cerrar...")
    else:
        print("\nBienvenido al ChatBot Contable")
        ejecutando = True
        while ejecutando:
            print("\nSeleccione una opción:")
            print("1 - Hacer una pregunta específica")
            print("2 - Ver todas las preguntas de una temática")
            print("0 - Finalizar")
            modo = input("Usuario: ").strip().lower()

            if modo == "0":
                #Opción 0: Finaliza el programa
                print("\nGracias por usar el chatbot. ¡Hasta luego!")
                input("Presione Enter para cerrar...")
                ejecutando = False

            elif modo == "2":
                #Opción 2: Ver preguntas por palabra clave
                palabra_clave = input("\nEscriba una palabra clave para buscar preguntas relacionadas (o presione Enter para volver al menú): ").strip().lower()
                if palabra_clave == "":
                    continue

                palabra_clave = obtener_palabra_canonica(normalizar(palabra_clave))
                print(f"\nPreguntas relacionadas con '{palabra_clave}':\n")

                preguntas_relacionadas = []

                try:
                    with open(archivo_csv, newline='', encoding='utf-8') as archivo:
                        lector = csv.reader(archivo, delimiter=';')
                        for fila in lector:
                            if len(fila) >= 2:
                                pregunta, respuesta = fila
                                palabras_pregunta = set(obtener_palabra_canonica(p) for p in normalizar(pregunta).split())
                                if palabra_clave in palabras_pregunta:
                                    preguntas_relacionadas.append((pregunta.strip(), respuesta.strip()))
                except Exception as e:
                    print("Error al leer el archivo de preguntas:", e)
                    return

                if preguntas_relacionadas:
                    for i, (preg, _) in enumerate(preguntas_relacionadas, start=1):
                        print(f"{i}. {preg}")

                    eleccion = input("\nElija el número de la pregunta que desea ver (o presione Enter para volver): ").strip()
                    if eleccion.isdigit():
                        idx = int(eleccion) - 1
                        if 0 <= idx < len(preguntas_relacionadas):
                            print("\nChatbot:", preguntas_relacionadas[idx][1])
                        else:
                            print("Número inválido.")
                else:
                    print("No se encontraron preguntas relacionadas con esa temática.")


            elif modo == "1":
                #Opción 1: realizar una pregunta especifica
                entrada = "a"  # cualquier valor que no sea cadena vacía
                while entrada != "":
                    print("\nSi desea volver al Menú Principal, presione la tecla Enter\n")
                    entrada = input("Ingrese la pregunta. Puede ser sin los signos de interrogación: ").strip(" ¿?")

                    if entrada != "":
                        respuesta_aproximada = buscar_por_palabras_clave(entrada)
                        if respuesta_aproximada:
                            print("Chatbot:", respuesta_aproximada)
                        else:
                            print("Chatbot: No conozco esa pregunta.")
                            print("¿Desea ingresar una respuesta a su pregunta?")
                            resp = input("Ingrese 'sí' si desea hacerlo. Caso contrario, presione la tecla Enter para volver al Menú Principal: ")
                            if resp.lower() in ["si", "sí"]:
                                nueva_respuesta = input("Por favor, ingrese la respuesta para guardarla: ").strip()
                                agregar_pregunta_respuesta(entrada, nueva_respuesta)
                                print("¡Pregunta y respuesta guardadas!")
            else:
                print("Opción inválida. Por favor ingrese 0, 1 o 2.")

# Punto de entrada al programa
main()
