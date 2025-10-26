import cv2
import os
import numpy as np

# --- Configuración ---
input_folder = "test_images_originales"
output_folder = "test_images_invertidas_vertical"
# ---------------------

os.makedirs(output_folder, exist_ok=True)
print(f"Generando imágenes en: {output_folder}")

if not os.path.exists(input_folder):
    print(f"Error: La carpeta de entrada '{input_folder}' no existe.")
else:
    for filename in os.listdir(input_folder):
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".ppm")):
            img_path = os.path.join(input_folder, filename)
            image = cv2.imread(img_path)
            
            if image is None:
                print(f"  - No se pudo leer {filename}")
                continue

            # --- Aplicamos el giro vertical (Flip) ---
            # 0 = Giro Vertical (eje X)
            # 1 = Giro Horizontal (eje Y)
            # -1 = Giro en ambos ejes (equivale a rotación de 180°)
            flipped_img = cv2.flip(image, 0) 
            
            # Guardamos la nueva imagen
            output_path = os.path.join(output_folder, filename)
            cv2.imwrite(output_path, flipped_img)
    
    print(f"¡Carpeta con imágenes invertidas generada con éxito!")