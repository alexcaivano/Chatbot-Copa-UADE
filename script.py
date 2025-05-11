import csv

archivo_csv = "preg.csv"

def buscar_respuesta(pregunta_usuario):
    with open(archivo_csv, newline='', encoding='utf-8') as archivo:
        lector = csv.reader(archivo, delimiter=';')
        for fila in lector:
            if len(fila) >= 2:
                pregunta, respuesta = fila
                if pregunta.strip(" ¿?").lower() == pregunta_usuario.strip().lower():
                    return respuesta.strip()
    return None

def agregar_pregunta_respuesta(pregunta, respuesta):
    with open(archivo_csv, mode='a', newline='', encoding='utf-8') as archivo:
        escritor = csv.writer(archivo, delimiter=';')
        escritor.writerow([pregunta, respuesta])

# Bucle principal
entrada = ""
while entrada.lower() != "salir":
    print("\nCuando desee finalizar, ingrese la palabra 'salir'\n")
    entrada = input("Ingrese la pregunta. Puede ser sin los ¿?: ").strip(" ¿?")
    
    if entrada.lower() != "salir":
        respuesta = buscar_respuesta(entrada)
        if respuesta:
            print("Respuesta:", respuesta)
        else:
            print("Respuesta: No conozco esa pregunta.")
            print("\nDesea ingresar una respuesta a su pregunta?")
            resp=input("Ingrese si o no: ")
            
            if resp.lower() != "si" and resp.lower() != "no":
                while resp.lower() != "si" and resp.lower() != "no":
                    resp=input("\nIngrese una opcion valida: ")
                    
            if resp.lower() == "si":
                nueva_respuesta = input("\nPor favor, ingrese la respuesta para guardarla: ").strip()
                agregar_pregunta_respuesta(entrada, nueva_respuesta)
                print("¡Pregunta y respuesta guardadas!")
            

    

    
