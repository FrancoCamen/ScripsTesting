import cv2
import os
import numpy as np
import random # <--- Añadido para fondos aleatorios

# --- Configuración ---
input_folder = "test_images_originales"
background_folder = "fondos_reales" # <--- Añadido: Carpeta de fondos
angles_to_test = [5, 10, 20, 40, 80, 160] # Los grados que queremos probar
# fill_color ya no es necesario
# ---------------------

def rotate_image(image, angle, background_canvas):
    """
    Rota una imagen y la 'pega' sobre un lienzo de fondo real,
    rellenando el espacio vacío de la rotación con el fondo.
    """
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)

    # Obtenemos la matriz de rotación
    M = cv2.getRotationMatrix2D((cX, cY), angle, 1.0)
    
    # Aplicamos la rotación a la señal, llenando los bordes con negro
    rotated_signal = cv2.warpAffine(image, M, (w, h), borderValue=(0, 0, 0))

    # --- Creación de la Máscara y Combinación ---
    
    # Creamos una máscara de la señal rotada (todo lo que NO es negro)
    gray_rotated = cv2.cvtColor(rotated_signal, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray_rotated, 1, 255, cv2.THRESH_BINARY)
    
    # Creamos la máscara inversa (el área que SÍ es negra)
    mask_inv = cv2.bitwise_not(mask)
    
    # "Cortamos" el área de la señal del fondo
    bg_part = cv2.bitwise_and(background_canvas, background_canvas, mask=mask_inv)
    
    # "Cortamos" la señal de la imagen rotada (esto es redundante pero seguro)
    signal_part = cv2.bitwise_and(rotated_signal, rotated_signal, mask=mask)

    # Combinamos el fondo "cortado" con la señal "cortada"
    combined = cv2.add(bg_part, signal_part)
    return combined

# --- Bucle Principal ---

# Cargamos la lista de fondos UNA VEZ
background_files = [f for f in os.listdir(background_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

if not background_files:
    print(f"Error: No se encontraron imágenes de fondo en la carpeta '{background_folder}'.")
    exit()

print(f"Cargados {len(background_files)} fondos realistas.")

if not os.path.exists(input_folder):
    print(f"Error: La carpeta de entrada '{input_folder}' no existe.")
else:
    for angle in angles_to_test:
        output_folder = f"test_images_rotadas_{angle}_grados_fondo_real" # Renombrada la carpeta de salida
        os.makedirs(output_folder, exist_ok=True)
        print(f"Generando imágenes en: {output_folder}")

        for filename in os.listdir(input_folder):
            if filename.lower().endswith((".png", ".jpg", ".jpeg", ".ppm")):
                img_path = os.path.join(input_folder, filename)
                image = cv2.imread(img_path)
                
                if image is None:
                    print(f"  - No se pudo leer {filename}")
                    continue

                # --- Cargar y preparar el fondo para CADA imagen ---
                random_bg_name = random.choice(background_files)
                bg_path = os.path.join(background_folder, random_bg_name)
                background = cv2.imread(bg_path)
                
                # Redimensionamos el fondo para que coincida con el tamaño de la imagen original
                (h, w) = image.shape[:2]
                bg_canvas = cv2.resize(background, (w, h), interpolation=cv2.INTER_CUBIC)

                # Rotamos la imagen pasándole el lienzo de fondo
                rotated_img = rotate_image(image, angle, bg_canvas)
                
                # Guardamos la nueva imagen
                output_path = os.path.join(output_folder, filename)
                cv2.imwrite(output_path, rotated_img)
        
        print(f"¡Carpeta con rotación de {angle}° y fondo real generada con éxito!")