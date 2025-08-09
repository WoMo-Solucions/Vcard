import qrcode
from PIL import Image

# Configuración
qr_data = "https://ramiju81.github.io/Vcard/"
qr_logo_path = "logo.png"
qr_output_path = "qr_womo.png"
html_output_path = "index.html"

# 1. Generar el código QR
qr = qrcode.QRCode(
    error_correction=qrcode.constants.ERROR_CORRECT_H
)
qr.add_data(qr_data)
qr.make(fit=True)

qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

# 2. Procesar el logo con fondo blanco moderado
logo_size = 80  # Tamaño del logo
logo = Image.open(qr_logo_path).convert("RGBA")
logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

# Crear fondo blanco (solo 10px más grande en cada lado)
bg_size = (logo_size + 20, logo_size + 20)
background = Image.new("RGBA", bg_size, "white")

# Pegar el logo centrado en el fondo
logo_pos = (
    (bg_size[0] - logo_size) // 2,
    (bg_size[1] - logo_size) // 2
)
background.paste(logo, logo_pos, logo)

# 3. Pegar en el QR
qr_pos = (
    (qr_img.size[0] - bg_size[0]) // 2,
    (qr_img.size[1] - bg_size[1]) // 2
)
qr_img.paste(background, qr_pos, background)

# 4. Guardar QR
qr_img.save(qr_output_path)

# 5. HTML ORIGINAL COMPLETO (sin modificaciones)
html_content = """
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Julian Ramirez | Tarjeta Digital</title>
  <!-- Cambia la ruta del CSS así: -->
  <link rel="stylesheet" href="./statics/css/styles.css">
  <link href="https://fonts.googleapis.com/css2?family=Rubik:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
  <div class="vcard">
    <!-- Fondo degradado ámbar -->
    <div class="amber-fade"></div>
    
    <!-- Fondo de imagen -->
    <div class="bg-pattern"></div>
    
    <!-- Contenido principal -->
    <div class="content">
      <!-- Foto de perfil con ruta verificada -->
      <div class="photo-frame">
        <img src="./statics/img/foto.jpg" alt="Julian Ramirez" 
             onerror="this.src='https://via.placeholder.com/400'">
      </div>
      
      <!-- Información textual -->
      <div class="info">
        <h1>Julian Ramirez</h1>
        <h2>Profesional en Desarrollo de Software</h2>
        
        <div class="details">
          <p class="cargo"><i class="fas fa-briefcase"></i> Full Stack Developer</p>
          <p class="ubicacion uni"><i class="fas fa-university"></i> UNICUCES</p>
          <p class="ubicacion"><i class="fas fa-map-marker-alt"></i> Cali - Colombia</p>
        </div>
      </div>
      
      <!-- Botones sociales -->
      <div class="social">
        <a href="https://www.linkedin.com/in/julianramirezc"title="LinkedIn"  class="linkedin"><i class="fab fa-linkedin-in"></i></a>
        <a href="https://github.com/ramiju81" title="github" class="github"><i class="fab fa-github"></i></a>
        <a href="mailto:juliram81@hotmail.com" title="email" class="email"><i class="fas fa-envelope"></i></a>
        <a href="https://instagram.com/eljuliramirez" title="instagram" class="instagram"><i class="fab fa-instagram"></i></a>
        <a href="https://wa.me/573183863532" title="whatsapp" class="whatsapp"><i class="fab fa-whatsapp"></i></a>
      </div>
     
      <!-- Mensaje -->
    <div class="mensaje-box">
      <div class="mensaje">
      <p>
        Apasionado por el desarrollo de soluciones digitales que simplifican y transforman procesos reales. <br>
        Creo en la tecnología como medio para hacer la vida más fácil, automatizada y humana.
      </div>
    </div>
  </div>

  <!-- Añade esto para depuración -->
  <script>
    document.addEventListener('DOMContentLoaded', function() {
      // Verifica si el CSS se cargó
      const stylesheets = Array.from(document.styleSheets);
      const cssLoaded = stylesheets.some(sheet => sheet.href && sheet.href.includes('styles.css'));
      
      if (!cssLoaded) {
        console.error('El CSS no se cargó correctamente');
        // Carga alternativa
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

# 6. Guardar HTML
with open(html_output_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ QR, HTML generados.")