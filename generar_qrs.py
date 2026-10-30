import json
import qrcode

# Tu URL base oficial en GitHub Pages
BASE_URL = "https://carlsantoniotorres.github.io/validacion-curso/"

# Cargar los datos desde alumnos.json
try:
  with open("alumnos.json", "r", encoding="utf-8") as f:
    data = json.load(f)
except FileNotFoundError:
  print("❌ Error: No se encontró el archivo 'alumnos.json'.")
  exit()

curso = data.get("curso", "Curso")
alumnos = data.get("alumnos", [])

print(
    f"🚀 Generando códigos QR para: {curso} ({len(alumnos)} alumnos"
    " encontrados)...\n"
)

for alumno in alumnos:
  alumno_id = alumno["id"]
  nombre = alumno["nombre"]

  # Construir la URL personalizada con el parámetro ?id=...
  url_personalizada = f"{BASE_URL}?id={alumno_id}"

  # Generar el código QR
  img = qrcode.make(url_personalizada)

  # Guardar la imagen con el formato QR_ID.png (ej: QR_CAT-001.png)
  nombre_archivo = f"QR_{alumno_id}.png"
  img.save(nombre_archivo)

  print(f"✅ QR creado: {nombre_archivo} -> {nombre}")

print(
    "\n🎉 ¡Listo! Todos los códigos QR se guardaron como imágenes en tu"
    " carpeta."
)