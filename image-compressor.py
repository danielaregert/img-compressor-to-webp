import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import Image


def compress_images(source_folder, destination_folder):
    compressed_files = []

    # Crear la carpeta de destino si no existe
    compressed_folder = os.path.join(destination_folder, os.path.basename(source_folder) + "_compressed")
    if not os.path.exists(compressed_folder):
        os.makedirs(compressed_folder)

    for filename in os.listdir(source_folder):
        if filename.endswith('.jpg'):
            image_path = os.path.join(source_folder, filename)
            image = Image.open(image_path)

            webp_path = os.path.join(compressed_folder, os.path.splitext(filename)[0] + '.webp')

            # Comprimir la imagen y guardarla en formato WebP
            image.save(webp_path, 'webp', quality=80)

            # Calcular el tamaño y tamaño final
            jpg_size = os.path.getsize(image_path)
            webp_size = os.path.getsize(webp_path)

            # Redondear el tamaño y agregar la unidad de peso
            jpg_size_kb = round(jpg_size / 1024, 2)
            webp_size_kb = round(webp_size / 1024, 2)

            # Calcular el porcentaje de compresión
            compression_percentage = round((1 - (webp_size / jpg_size)) * 100, 2)

            # Almacenar los datos en un diccionario
            file_info = {
                'archivo': filename,
                'tamaño': f"{jpg_size_kb} KB",
                'tamaño_final': f"{webp_size_kb} KB",
                'ubicacion': compressed_folder,
                'porcentaje_compresion': f"{compression_percentage}%"
            }
            compressed_files.append(file_info)

    return compressed_files


def select_folder(label):
    folder_path = filedialog.askdirectory()
    label.config(text=folder_path)


def compress_and_convert():
    source_folder = source_label.cget("text")
    destination_folder = destination_label.cget("text")

    if not source_folder or not destination_folder:
        result_label.config(text="Selecciona una carpeta de origen y destino.")
        return

    compressed_files = compress_images(source_folder, destination_folder)

    # Limpiar tabla existente
    for child in result_treeview.get_children():
        result_treeview.delete(child)

    # Llenar tabla con los datos
    for file in compressed_files:
        result_treeview.insert("", "end", values=(file['archivo'], file['tamaño'], file['tamaño_final'], file['ubicacion'], file['porcentaje_compresion']))

    result_label.config(text="Archivos comprimidos")


# Crear la ventana principal
window = tk.Tk()
window.title("Compresor y Convertidor de Imágenes")
window.geometry("800x400")

# Etiqueta y botón para seleccionar la carpeta de origen
source_label = tk.Label(window, text="Carpeta de origen:")
source_label.pack()
source_button = tk.Button(window, text="Seleccionar", command=lambda: select_folder(source_label))
source_button.pack()

# Etiqueta y botón para seleccionar la carpeta de destino
destination_label = tk.Label(window, text="Carpeta de destino:")
destination_label.pack()
destination_button = tk.Button(window, text="Seleccionar", command=lambda: select_folder(destination_label))
destination_button.pack()

# Botón para iniciar la compresión y conversión
compress_button = tk.Button(window, text="Comprimir y Convertir", command=compress_and_convert)
compress_button.pack()

# Tabla para mostrar los resultados
columns = ("Archivo", "Tamaño", "Tamaño final", "Ubicación", "Porcentaje de compresión")
result_treeview = ttk.Treeview(window, columns=columns, show="headings")

for col in columns:
    result_treeview.heading(col, text=col)

result_treeview.pack(fill="both", expand=True)

# Etiqueta para mostrar el resultado
result_label = tk.Label(window, text="")
result_label.pack()

# Ejecutar la ventana
window.mainloop()
