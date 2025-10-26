import cv2
import os
import numpy as np
import random # Para elegir fondos al azar

# --- Configuración ---
input_folder = "test_images_originales" # Tus imágenes de prueba (las del Test Case 14)
background_folder = "fondos_reales" # La carpeta que acabas de crear
scale_factor = 0.5 # 0.866 para 75%, 0.707 para 50%, 0.5 para 25%
# ---------------------

output_folder_real_bg = "test_images_fondo_real"
os.makedirs(output_folder_real_bg, exist_ok=True)

# --- Cargar la lista de fondos ---
background_files = [f for f in os.listdir(background_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

if not background_files:
    print(f"Error: No se encontraron imágenes de fondo en la carpeta '{background_folder}'.")
    # Salir o detener el script si no hay fondos
    exit()

print(f"Cargados {len(background_files)} fondos realistas.")

# --- Bucle Principal ---
for filename in os.listdir(input_folder):
    if not filename.lower().endswith((".png", ".jpg", ".jpeg", ".ppm")):
        continue
        
    img_path = os.path.join(input_folder, filename)
    signal_image = cv2.imread(img_path)
    
    if signal_image is None:
        print(f"  - No se pudo leer la señal {filename}")
        continue
    
    (h, w) = signal_image.shape[:2]
    
    # 1. Cargar y preparar el fondo
    random_bg_name = random.choice(background_files)
    bg_path = os.path.join(background_folder, random_bg_name)
    background = cv2.imread(bg_path)
    # Redimensionamos el fondo para que tenga el mismo tamaño que el lienzo original
    background_canvas = cv2.resize(background, (w, h), interpolation=cv2.INTER_CUBIC)

    # 2. Crear la señal pequeña
    new_h, new_w = int(h * scale_factor), int(w * scale_factor)
    small_signal = cv2.resize(signal_image, (new_w, new_h), interpolation=cv2.INTER_AREA)
    
    # 3. Pegar la señal pequeña en el fondo (centrada)
    x_offset = (w - new_w) // 2
    y_offset = (h - new_h) // 2
    
    # Copiamos el fondo
    final_image = background_canvas.copy() 
    # Pegamos la señal encima
    final_image[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = small_signal

    # 4. Guardar la nueva imagen
    cv2.imwrite(os.path.join(output_folder_real_bg, filename), final_image)

print(f"¡Dataset con fondos reales generado en '{output_folder_real_bg}'!")