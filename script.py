
import csv
import unicodedata

# Archivo donde se guardan preguntas y respuestas
archivo_csv = "preg.csv"

#----------------------------------------------------------------------------------------------
# FUNCIONES
#----------------------------------------------------------------------------------------------

def normalizar_texto(texto):
    texto = texto.strip(" ¿?¡!.,:;").lower()  # Limpia signos comunes y espacios
    texto = unicodedata.normalize('NFD', texto)
    texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')  # Elimina tildes
    return texto

def buscar_respuesta(pregunta_usuario):
    pregunta_usuario = normalizar_texto(pregunta_usuario)
    with open(archivo_csv, newline='', encoding='utf-8') as archivo:
        lector = csv.reader(archivo, delimiter=';')
        for fila in lector:
            if len(fila) >= 2:
                pregunta, respuesta = fila
                if normalizar_texto(pregunta) == pregunta_usuario:
                    return respuesta.strip()
    return None

def agregar_pregunta_respuesta(pregunta, respuesta):
    with open(archivo_csv, mode='a', newline='', encoding='utf-8') as archivo:
        escritor = csv.writer(archivo, delimiter=';')
        escritor.writerow([pregunta, respuesta])

def validar_si_o_no(respuesta):
    while respuesta.lower() not in ["si", "no"]:
        respuesta = input("\nIngrese una opción válida (si o no): ").strip().lower()
    return respuesta.lower()

#----------------------------------------------------------------------------------------------
# CUERPO PRINCIPAL
#----------------------------------------------------------------------------------------------

def main():
    print("Bienvenido al ChatBot de preguntas. Escriba 'salir' para terminar.")
    entrada = ""
    while entrada.lower() != "salir":
        entrada = input("\nIngrese la pregunta. Puede ser sin los ¿?: ").strip(" ¿?")
        
        if entrada.lower() != "salir":
            respuesta = buscar_respuesta(entrada)
            if respuesta:
                print("Respuesta:", respuesta)
            else:
                print("Respuesta: No conozco esa pregunta.")
                print("\nDesea ingresar una respuesta a su pregunta?")
                resp = input("Ingrese si o no: ")
                resp = validar_si_o_no(resp)
                
                if resp.lower() == "si":
                    nueva_respuesta = input("\nPor favor, ingrese la respuesta para guardarla: ").strip()
                    agregar_pregunta_respuesta(entrada, nueva_respuesta)
                    print("¡Pregunta y respuesta guardadas!")
                    
# Punto de entrada al programa
main()
    

    
