document.addEventListener("DOMContentLoaded", function () {
    const vcfUrl = "./statics/julianramirez.vcf";

    // --- Verificar que el CSS esté cargado ---
    const stylesheets = Array.from(document.styleSheets);
    const cssLoaded = stylesheets.some(sheet => sheet.href && sheet.href.includes('styles.css'));

    if (!cssLoaded) {
        console.warn('El CSS no se cargó correctamente, cargando de respaldo...');
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = './statics/css/styles.css';
        document.head.appendChild(link);
    }

    // --- Cargar datos desde el VCF ---
    fetch(vcfUrl)
        .then(res => res.text())
        .then(data => {
            const getValue = (key) => {
                const regex = new RegExp(`${key}:(.*)`, "i");
                const match = data.match(regex);
                return match ? match[1].trim() : "";
            };

            const nombre = getValue("FN");
            const profesion = getValue("ORG"); // Profesión
            const empresa = ""; // Vacío
            const cargo = getValue("TITLE");
            const telefono = getValue("TEL");
            const email = getValue("EMAIL");
            const direccionRaw = getValue("ADR;TYPE=home");
            const direccion = direccionRaw ? direccionRaw.split(";").filter(Boolean).join(" ").trim() : "";
            const nota = getValue("NOTE");
            const universidad = getValue("X-SCHOOL");

            const urls = data.match(/URL:(.*)/gi)?.map(u => u.replace("URL:", "").trim()) || [];

            // --- Rellenar HTML ---
            document.querySelector("h1").innerText = nombre;
            document.querySelector("h2").innerText = profesion;  // Profesión en lugar de empresa
            document.querySelector(".cargo").innerHTML = `<i class="fas fa-briefcase"></i> ${cargo}`;
            document.querySelector(".ubicacion.uni").innerHTML = `<i class="fas fa-university"></i> ${universidad}`;
            document.querySelector(".ubicacion.direccion").innerHTML = `<i class="fas fa-map-marker-alt"></i> ${direccion}`;
            document.querySelector(".mensaje p").innerText = nota;

            // --- Enlaces ---
            document.querySelector(".whatsapp").href = `https://wa.me/${telefono.replace("+", "")}`;
            document.querySelector(".email").href = `mailto:${email}`;
            if (urls[0]) document.querySelector(".linkedin").href = urls[0];
            if (urls[1]) document.querySelector(".github").href = urls[1];
            if (urls[2]) document.querySelector(".instagram").href = urls[2];
        })
        .catch(err => console.error("Error cargando datos del VCF:", err));

    // --- Botón Guardar Contacto ---
    const guardarBtn = document.getElementById("guardarContacto");
    if (guardarBtn) {
        guardarBtn.addEventListener("click", function (e) {
            e.preventDefault();

            const partesNombre = nombre.trim().split(" ");
            const nombreSolo = partesNombre.slice(0, -1).join(" ");
            const apellido = partesNombre.slice(-1).join(" ");
            const nombreCompleto = `${nombreSolo} ${apellido}`.trim();

            const urlGoogleContacts = `https://contacts.google.com/new?name=${encodeURIComponent(nombreCompleto)}&email=${encodeURIComponent(email)}`;
            window.open(urlGoogleContacts, "_blank");
        });
    }
});
