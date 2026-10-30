import json
import os
from weasyprint import HTML

def generar_constancias_pdf():
    # 1. Cargar datos desde alumnos.json
    try:
        with open("alumnos.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("❌ Error: No se encontró el archivo 'alumnos.json'.")
        return

    curso = data.get("curso", "Curso Práctico en Línea")
    alumnos = data.get("alumnos", [])
    print(f"🚀 Generando constancias en PDF para {len(alumnos)} alumno(s)...\n")

    # 2. Plantilla HTML/CSS con posicionamiento absoluto y tamaños aumentados (QR y Firma +30%)
    html_template = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <style>
            @page {{
                size: A4 landscape;
                margin: 0; 
            }}
            * {{
                box-sizing: border-box;
                -webkit-print-color-adjust: exact;
                print-color-adjust: exact;
            }}
            body {{
                margin: 0;
                padding: 0;
                font-family: 'Montserrat', 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
            }}
            
            /* Lienzo principal exacto A4 */
            .certificate {{
                width: 297mm;
                height: 210mm;
                background-color: #f0ece3; /* Margen beige exterior */
                padding: 12mm;
                position: relative;
            }}
            
            /* Contenedor blanco interior */
            .cert-bg {{
                width: 100%;
                height: 100%;
                background-color: #fcfbfa; 
                border: 4.5pt solid #152238; /* Borde azul marino */
                position: relative;
            }}
            
            /* Marco interior doble gris */
            .inner-border {{
                position: absolute;
                top: 6mm; bottom: 6mm; left: 6mm; right: 6mm;
                border: 1.5pt solid #9aa5b6;
                pointer-events: none;
            }}
            
            /* Barra decorativa superior tricolor */
            .top-bar-container {{
                position: absolute;
                top: -3mm; 
                left: 50%;
                transform: translateX(-50%);
                width: 90mm;
                height: 5mm;
                border-radius: 2.5mm;
                overflow: hidden;
            }}
            .bar-blue {{ position: absolute; left: 0; top: 0; bottom: 0; width: 65%; background-color: #2e6094; }}
            .bar-yellow {{ position: absolute; right: 0; top: 0; bottom: 0; width: 35%; background-color: #edbf33; }}

            /* ---------------------------------------------------
               POSICIONAMIENTO ABSOLUTO DE CONTENIDO 
               --------------------------------------------------- */
            
            /* Encabezado */
            .header {{
                position: absolute;
                top: 12mm; left: 15mm; right: 15mm;
                height: 25mm;
            }}
            .logo-img-container {{
                position: absolute;
                left: 50%;
                transform: translateX(-50%);
                top: 0;
                width: 22mm; height: 22mm;
            }}
            .logo-img {{ width: 100%; height: 100%; border-radius: 50%; object-fit: cover; }}
            .cert-info {{
                position: absolute; right: 0; top: 0;
                text-align: right; font-size: 10.5pt; color: #4a5568; line-height: 1.4;
            }}

            /* Títulos principales */
            .title-section {{
                position: absolute;
                top: 38mm; left: 0; right: 0;
                text-align: center;
            }}
            .main-title {{ font-size: 34pt; font-weight: 900; color: #152238; letter-spacing: 0.5pt; margin: 0 0 2mm 0; text-transform: uppercase; }}
            .sub-title {{ font-size: 16pt; color: #6b7c93; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5pt; }}
            .otorga-text {{ font-size: 15pt; color: #2d3748; margin-top: 10mm; }}

            /* Nombre del Alumno */
            .student-name-container {{
                position: absolute;
                top: 80mm; left: 0; right: 0;
                text-align: center;
            }}
            .student-name {{
                font-size: 44pt; color: #111; font-weight: bold; margin: 0;
                padding: 0 5mm 3mm 5mm; border-bottom: 1.5pt solid #9aa5b6; display: inline-block; min-width: 65%;
            }}

            /* Descripción del Curso */
            .course-description {{
                position: absolute;
                top: 108mm; left: 0; right: 0;
                text-align: center;
                font-size: 15pt; color: #2d3748;
            }}
            .course-name {{ font-size: 22pt; font-weight: 800; color: #152238; margin-top: 2mm; }}

            /* Pie de Página (Aumentado para acomodar firma/QR más grandes) */
            .footer-section {{
                position: absolute;
                bottom: 12mm; left: 15mm; right: 15mm;
                height: 45mm; 
            }}
            
            /* Bloques individuales del pie de página */
            .footer-block-left {{ position: absolute; left: 0; bottom: 0; width: 65mm; text-align: center; }}
            .footer-block-center {{ position: absolute; left: 50%; transform: translateX(-50%); bottom: 0; width: 50mm; text-align: center; }}
            .footer-block-right {{ position: absolute; right: 0; bottom: 0; width: 65mm; text-align: center; }}

            /* Código QR (AUMENTADO APROX 30%) */
            .qr-box {{ 
                width: 31mm; 
                height: 31mm; 
                background: white; 
                padding: 1.5mm; 
                border: 1pt solid #ccc; 
                margin: 0 auto 2mm auto; 
            }}
            .qr-box img {{ width: 100%; height: 100%; object-fit: contain; }}
            .qr-text {{ font-size: 8pt; color: #4a5568; font-weight: bold; text-transform: uppercase; letter-spacing: 0.5pt; }}

            /* FIRMA (AUMENTADA APROX 30%) */
            .signature-container {{
                height: 32mm; 
                position: relative;
                margin-bottom: 2mm;
            }}
            .signature-img {{
                position: absolute;
                bottom: 0;
                left: 50%;
                transform: translateX(-50%);
                height: 31mm; /* Firma notablemente más grande */
                max-width: 75mm;
                object-fit: contain;
            }}

            /* Líneas y textos inferiores */
            .footer-line {{ width: 100%; height: 1.5pt; background-color: #9aa5b6; margin-bottom: 2mm; }}
            .footer-label {{ font-size: 12pt; color: #152238; line-height: 1.2; }}
            .footer-label-sub {{ font-size: 8.5pt; color: #6b7c93; text-transform: uppercase; font-weight: normal; display: block; margin-top: 1mm; }}
        </style>
    </head>
    <body>
        <div class="certificate">
            <div class="cert-bg">
                
                <!-- Borde interior gris -->
                <div class="inner-border"></div>

                <!-- Barra tricolor superior -->
                <div class="top-bar-container">
                    <div class="bar-blue"></div>
                    <div class="bar-yellow"></div>
                </div>

                <!-- Cabecera con logo -->
                <div class="header">
                    <div class="logo-img-container">
                        <img src="logo.png" class="logo-img" alt="Logo">
                    </div>
                    <div class="cert-info">
                        Certificado ID: CAT-PY-2026-{id_num}<br>
                        Referencia: {id_num}
                    </div>
                </div>

                <!-- Títulos -->
                <div class="title-section">
                    <h1 class="main-title">Constancia de Acreditación</h1>
                    <div class="sub-title">{curso}</div>
                    <div class="otorga-text">Se otorga el presente reconocimiento a:</div>
                </div>

                <!-- Nombre del Alumno -->
                <div class="student-name-container">
                    <h2 class="student-name">{nombre_alumno}</h2>
                </div>

                <!-- Curso aprobado -->
                <div class="course-description">
                    Por haber completado satisfactoriamente el curso:
                    <div class="course-name">Python desde Cero — Fundamentos y POO.</div>
                </div>

                <!-- Pie de página con Fecha, QR dinámico y Firma -->
                <div class="footer-section">
                    
                    <!-- Fecha (Izquierda) -->
                    <div class="footer-block-left">
                        <div class="footer-line"></div>
                        <div class="footer-label">
                            {fecha}
                            <span class="footer-label-sub">FECHA</span>
                        </div>
                    </div>

                    <!-- Código QR (Centro) -->
                    <div class="footer-block-center">
                        <div class="qr-box">
                            <img src="{qr_filename}" alt="Código QR">
                        </div>
                        <div class="qr-text">Verificación Técnica</div>
                    </div>

                    <!-- Firma e Instructor (Derecha) -->
                    <div class="footer-block-right">
                        <div class="signature-container">
                            <img src="firma.png" class="signature-img" alt="Firma Instructor">
                        </div>
                        <div class="footer-line"></div>
                        <div class="footer-label">
                            Carlos Antonio Torres
                            <span class="footer-label-sub">INSTRUCTOR • DATA ENGINEER</span>
                        </div>
                    </div>

                </div>

            </div>
        </div>
    </body>
    </html>
    """

    # 3. Procesar cada alumno del JSON
    for alumno in alumnos:
        alumno_id = alumno["id"]
        nombre_alumno = alumno["nombre"]
        fecha = alumno.get("fecha", "Noviembre 2026")
        id_num = alumno_id.split("-")[-1] if "-" in alumno_id else "0001"

        # Detección inteligente del QR correspondiente al alumno
        qr_filename = f"QR_{alumno_id}.png"
        if not os.path.exists(qr_filename):
            if os.path.exists("QR_CAT-001.png"):
                qr_filename = "QR_CAT-001.png"
            else:
                print(f"⚠️ Advertencia: No se encontró el archivo QR para {alumno_id}.")
                qr_filename = "" 

        # Preparar HTML con los datos del alumno
        html_contenido = html_template.format(
            nombre_alumno=nombre_alumno,
            curso=curso,
            alumno_id=alumno_id,
            id_num=id_num,
            fecha=fecha,
            qr_filename=qr_filename
        )

        # Nombre del archivo PDF resultante
        archivo_pdf = f"Constancia_{alumno_id}.pdf"

        # Generar el PDF mediante WeasyPrint (base_url mantiene el mapeo de imágenes locales)
        HTML(string=html_contenido, base_url=os.getcwd()).write_pdf(archivo_pdf)
        print(f"✅ PDF generado correctamente: {archivo_pdf} para {nombre_alumno}")

    print("\n🎉 ¡Proceso finalizado con éxito! Todos los PDFs están listos en tu carpeta.")

if __name__ == "__main__":
    generar_constancias_pdf()