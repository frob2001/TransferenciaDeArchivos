import requests

# Primero, definimos la URL de donde vamos a descargar el archivo y el nombre bajo el cual queremos guardarlo.
url_descargar = "http://127.0.0.1:5000/descargar-csv"
nombre_archivo_local = "archivo_descargado.csv"

# Descargar el archivo CSV
try:
    respuesta_descarga = requests.get(url_descargar)
    respuesta_descarga.raise_for_status()  # Esto lanzará un error si la descarga falla
    with open(nombre_archivo_local, "wb") as archivo:
        archivo.write(respuesta_descarga.content)
    print(f"Archivo {nombre_archivo_local} descargado con éxito.")
except Exception as e:
    print(f"Error al descargar el archivo: {e}")
    exit()

# Ahora, preparamos para subir el archivo
url_subir = "http://localhost:5500/subir"

with open(nombre_archivo_local, 'rb') as archivo:
    archivos = {'file': archivo}
    try:
        # Nota: No es necesario especificar el content-type; requests lo hace por ti.
        respuesta_subir = requests.post(url_subir, files=archivos)
        respuesta_subir.raise_for_status()  # Esto lanzará un error si la subida falla
        print("Archivo subido con éxito.")
    except Exception as e:
        print(f"Error al subir el archivo: {e}")

