document.addEventListener("DOMContentLoaded", function () {
    // --- 1. Verificar que el CSS esté cargado ---
    const stylesheets = Array.from(document.styleSheets);
    const cssLoaded = stylesheets.some(sheet => sheet.href && sheet.href.includes('styles.css'));

    if (!cssLoaded) {
        console.error('El CSS no se cargó correctamente');
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = './statics/css/styles.css';
        document.head.appendChild(link);
    }

    // --- 2. Cargar datos desde el VCF ---
    fetch("./statics/julianramirez.vcf")
        .then(res => res.text())
        .then(data => {
            const getValue = (key) => {
                const regex = new RegExp(`${key}:(.*)`, "i");
                const match = data.match(regex);
                return match ? match[1].trim() : "";
            };

            const nombre = getValue("FN");
            const empresa = "";
            const cargo = getValue("ORG");
            const telefono = getValue("TEL");
            const email = getValue("EMAIL");
            const direccionRaw = getValue("ADR;TYPE=home");
            const direccion = direccionRaw ? direccionRaw.split(";").filter(Boolean).join(" ").trim() : "";
            const nota = getValue("NOTE");
            const universidad = getValue("X-SCHOOL");

            const urls = data.match(/URL:(.*)/gi)?.map(u => u.replace("URL:", "").trim()) || [];

            // Rellenar HTML
            document.querySelector("h1").innerText = nombre;
            document.querySelector("h2").innerText = profesion;
            document.querySelector(".cargo").innerHTML = `<i class="fas fa-briefcase"></i> ${cargo}`;
            //document.querySelector(".ubicacion.uni").innerHTML = `<i class="fas fa-university"></i> ${universidad}`;
            document.querySelector(".ubicacion.direccion").innerHTML = `<i class="fas fa-map-marker-alt"></i> ${direccion}`;
            document.querySelector(".mensaje p").innerText = nota;

            // Enlaces
            document.querySelector(".whatsapp").href = `https://wa.me/${telefono.replace("+", "")}`;
            document.querySelector(".email").href = `mailto:${email}`;
            if (urls[0]) document.querySelector(".linkedin").href = urls[0];
            if (urls[1]) document.querySelector(".github").href = urls[1];
            if (urls[2]) document.querySelector(".instagram").href = urls[2];
        })
        .catch(err => console.error("Error cargando datos del VCF:", err));

    // --- 3. Botón Guardar Contacto ---
    const guardarBtn = document.getElementById("guardarContacto");
    if (guardarBtn) {
        guardarBtn.addEventListener("click", function (e) {
            e.preventDefault();
            const vcfUrl = "./statics/julianramirez.vcf";
            const link = document.createElement("a");
            link.href = vcfUrl;
            link.download = "Julian_Ramirez.vcf";
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        });
    }
});