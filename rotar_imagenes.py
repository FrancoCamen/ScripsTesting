import cv2
import os
import numpy as np

# --- Configuración ---
input_folder = "test_images_originales"
angles_to_test = [5, 10, 20, 40, 80, 160] # Los grados que queremos probar
fill_color = (255, 255, 255) # Color de fondo (blanco) para el relleno
# ---------------------

def rotate_image(image, angle, fill_color):
    """Rota una imagen manteniendo el centro y rellenando el fondo."""
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)

    # Obtenemos la matriz de rotación
    M = cv2.getRotationMatrix2D((cX, cY), angle, 1.0)
    
    # Aplicamos la rotación
    rotated = cv2.warpAffine(image, M, (w, h), borderValue=fill_color)
    return rotated

# --- Bucle Principal ---
if not os.path.exists(input_folder):
    print(f"Error: La carpeta de entrada '{input_folder}' no existe.")
else:
    for angle in angles_to_test:
        output_folder = f"test_images_rotadas_{angle}_grados"
        os.makedirs(output_folder, exist_ok=True)
        print(f"Generando imágenes en: {output_folder}")

        for filename in os.listdir(input_folder):
            if filename.lower().endswith((".png", ".jpg", ".jpeg", ".ppm")):
                img_path = os.path.join(input_folder, filename)
                image = cv2.imread(img_path)
                
                if image is None:
                    print(f"  - No se pudo leer {filename}")
                    continue

                # Rotamos la imagen
                rotated_img = rotate_image(image, angle, fill_color)
                
                # Guardamos la nueva imagen
                output_path = os.path.join(output_folder, filename)
                cv2.imwrite(output_path, rotated_img)
        
        print(f"¡Carpeta con rotación de {angle}° generada con éxito!")