import qrcode
from PIL import Image, ImageDraw, ImageFont

# Configuración
qr_data = "https://ramiju81.github.io/Vcard/"
qr_logo_path = "logo.png"
qr_output_path = "QR_Ing_Juli.png"
qr_output_path_colored = "QR_Ing_Juli_colored.png"
html_output_path = "index.html"

# Colores
color_fondo = "white"
color_normal = "black"
color_letras = (0, 102, 204)  # Azul fuerte

# 1. Generar QR base
qr = qrcode.QRCode(
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4
)
qr.add_data(qr_data)
qr.make(fit=True)

qr_img = qr.make_image(fill_color=color_normal, back_color=color_fondo).convert("RGB")

# 2. Crear máscara para letras "JR"
mask = Image.new("L", qr_img.size, 0)
draw_mask = ImageDraw.Draw(mask)

# Usar una fuente TrueType para mejor control
try:
    font = ImageFont.truetype("arial.ttf", 200)
except:
    font = ImageFont.load_default()

text = "JR"
bbox = draw_mask.textbbox((0, 0), text, font=font)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]
text_x = (qr_img.size[0] - text_width) // 2
text_y = (qr_img.size[1] - text_height) // 2

draw_mask.text((text_x, text_y), text, font=font, fill=255)

# 3. Recolorear los módulos dentro de las letras
colored_qr = qr_img.copy()
pixels_qr = colored_qr.load()
pixels_mask = mask.load()

for y in range(qr_img.size[1]):
    for x in range(qr_img.size[0]):
        if pixels_mask[x, y] > 128 and pixels_qr[x, y] == (0, 0, 0):
            pixels_qr[x, y] = color_letras

# 4. Crear área blanca en el centro para el logo
logo_size = 80
blank_size = logo_size + 10  # un poco más grande que el logo
blank = Image.new("RGB", (blank_size, blank_size), color_fondo)

blank_pos = (
    (colored_qr.size[0] - blank_size) // 2,
    (colored_qr.size[1] - blank_size) // 2
)
colored_qr.paste(blank, blank_pos)

# 5. Colocar logo en el centro
logo = Image.open(qr_logo_path).convert("RGBA")
logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

logo_pos = (
    (colored_qr.size[0] - logo_size) // 2,
    (colored_qr.size[1] - logo_size) // 2
)
colored_qr.paste(logo, logo_pos, logo)

# 6. Guardar resultado
colored_qr.save(qr_output_path)

print(f"✅ QR generado: {qr_output_path}")

# 6. HTML original (sin cambios)
html_content = """
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Julian Ramirez | Tarjeta Digital</title>
  <link rel="stylesheet" href="./statics/css/styles.css">
  <link href="https://fonts.googleapis.com/css2?family=Rubik:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
  <div class="vcard">
    <div class="amber-fade"></div>
    <div class="bg-pattern"></div>
    <div class="content">
      <div class="photo-frame">
        <img src="./statics/img/foto.jpg" alt="Julian Ramirez" 
             onerror="this.src='https://via.placeholder.com/400'">
      </div>
      <div class="info">
        <h1>Julian Ramirez</h1>
        <h2>Profesional en Desarrollo de Software</h2>
        <div class="details">
          <p class="cargo"><i class="fas fa-briefcase"></i> Full Stack Developer</p>
          <p class="ubicacion uni"><i class="fas fa-university"></i> UNICUCES</p>
          <p class="ubicacion"><i class="fas fa-map-marker-alt"></i> Cali - Colombia</p>
        </div>
      </div>
      <div class="social">
        <a href="https://www.linkedin.com/in/julianramirezc" title="LinkedIn" class="linkedin"><i class="fab fa-linkedin-in"></i></a>
        <a href="https://github.com/ramiju81" title="github" class="github"><i class="fab fa-github"></i></a>
        <a href="mailto:juliram81@hotmail.com" title="email" class="email"><i class="fas fa-envelope"></i></a>
        <a href="https://instagram.com/eljuliramirez" title="instagram" class="instagram"><i class="fab fa-instagram"></i></a>
        <a href="https://wa.me/573183863532" title="whatsapp" class="whatsapp"><i class="fab fa-whatsapp"></i></a>
      </div>
      <div class="mensaje-box">
        <div class="mensaje">
          <p>
            Apasionado por el desarrollo de soluciones digitales que simplifican y transforman procesos reales. <br>
            Creo en la tecnología como medio para hacer la vida más fácil, automatizada y humana.
          </p>
        </div>
      </div>
    </div>
  </div>
  <script>
    document.addEventListener('DOMContentLoaded', function() {
      const stylesheets = Array.from(document.styleSheets);
      const cssLoaded = stylesheets.some(sheet => sheet.href && sheet.href.includes('styles.css'));
      if (!cssLoaded) {
        console.error('El CSS no se cargó correctamente');
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = './statics/css/styles.css';
        document.head.appendChild(link);
      }
    });
  </script>
</body>
</html>
"""

# 7. Guardar HTML
with open(html_output_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ Generados QR HTML")
