// Validación cambio de contraseña
document.addEventListener("DOMContentLoaded", () => {
    const contrasena = document.getElementById("contrasena");
    const contrasena_ = document.getElementById("contrasena_");
    const mensajeError = document.getElementById("mensaje-error");
    const formulario = document.getElementById("form-cambiar-contrasena");

    function validarContrasenasIguales() {
        if (contrasena.value !== contrasena_.value) {
            mensajeError.style.display = "block";
            mensajeError.style.textAlign = "center";
            mensajeError.style.backgroundColor = "#bd1414";
            mensajeError.style.color = "#fff";
            mensajeError.style.fontWeight = "600";
            mensajeError.textContent = "Las contraseñas no coinciden.";
            return false;
        } else {
            mensajeError.style.display = "none";
            return true;
        }
    }

    contrasena.addEventListener("input", validarContrasenasIguales);
    contrasena_.addEventListener("input", validarContrasenasIguales);

    formulario.addEventListener("submit", function (e) {
        if (!validarContrasenasIguales()) {
            e.preventDefault();
        }
    });
});

// Validación elimina cuenta
function elimina_cuenta() {
    const contenedorUA = document.getElementById("contenedor-ua");
    let urlEliminar = contenedorUA.dataset.url;

    contenedorUA.innerHTML = `
        <p style="font-weight: bold;">Esta acción es irreversible</p>
        <p>¿Seguro que desea eliminar su cuenta?</p> 
        <a href="${urlEliminar}" class="enlace-ts">Eliminar cuenta</a>
        <a href="/" class="enlace-ts">Cancelar</a>
    `;
    contenedorUA.style.padding = "10px";
}

// Paginación
document.addEventListener("DOMContentLoaded", () => {
    const ejerciciosPorPagina = 10;

    document.querySelectorAll(".paginado").forEach((contenedor) => {
        const lista = contenedor.querySelector(".lista-ejercicios");
        const template = contenedor.querySelector(".ejercicios-data");
        const datos = Array.from(template.content.children);

        const totalPaginas = Math.max(
            1,
            Math.ceil(datos.length / ejerciciosPorPagina)
        );
        let paginaActual = 1;

        const spanPagina = contenedor.querySelector(".pagina-actual");
        const btnAnterior = contenedor.querySelector(".anterior");
        const btnSiguiente = contenedor.querySelector(".siguiente");

        function renderPagina(pagina) {
            lista.innerHTML = "";
            const inicio = (pagina - 1) * ejerciciosPorPagina;
            const fin = Math.min(inicio + ejerciciosPorPagina, datos.length);
            for (let i = inicio; i < fin; i++) {
                const data = datos[i].dataset;
                const li = document.createElement("li");

                // numeración manual: 1., 2., 3., etc.
                const numero = document.createElement("span");
                numero.textContent = `${i + 1}. `;
                numero.style.fontWeight = "500";

                const a = document.createElement("a");
                a.href = data.url;
                a.textContent = data.titulo;

                li.appendChild(numero);
                li.appendChild(a);
                lista.appendChild(li);
            }
            paginaActual = pagina;
            spanPagina.textContent = `${pagina} / ${totalPaginas}`;
            btnAnterior.disabled = pagina === 1;
            btnSiguiente.disabled = pagina === totalPaginas;
        }

        btnAnterior.addEventListener("click", () => {
            if (paginaActual > 1) renderPagina(paginaActual - 1);
        });

        btnSiguiente.addEventListener("click", () => {
            if (paginaActual < totalPaginas) renderPagina(paginaActual + 1);
        });

        renderPagina(1);
    });
});

// Mensajes
document.addEventListener('DOMContentLoaded', function() {
    const mensaje = document.getElementById('mensaje');

    if (mensaje) {
        setInterval(() => {
            mensaje.style.display = 'none';
        }, 8000);
    }
})