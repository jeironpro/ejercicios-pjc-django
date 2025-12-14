function agregarEjercicio() {
    let tbody = document
        .getElementById("ejercicios")
        .getElementsByTagName("tbody")[0];

    let fila = document.createElement("tr");
    fila.classList.add("fila-agregar");
    fila.setAttribute("id", "fila-agregar");

    let celdaId = document.createElement("td");
    celdaId.innerHTML = `<input type="number" name="id" placeholder="default" readonly>`;

    let celdaIdUnico = document.createElement("td");
    celdaIdUnico.innerHTML = `<input type="number" name="id_unico" placeholder="default" readonly>`;

    let celdaTitulo = document.createElement("td");
    celdaTitulo.innerHTML = `<input type="text" name="titulo" class="titulo" placeholder="Titulo">`;

    let celdaNivel = document.createElement("td");
    celdaNivel.innerHTML = `<input type="text" name="nivel" class="nivel" placeholder="Nivel">`;

    let celdaTipo = document.createElement("td");
    celdaTipo.innerHTML = `<input type="text" name="tipo" class="tipo" placeholder="Tipo">`;

    let celdaEnunciado = document.createElement("td");
    celdaEnunciado.innerHTML = `<textarea name="enunciado" class="enunciado" placeholder="Enunciado"></textarea>`;

    let celdaTareas = document.createElement("td");
    celdaTareas.innerHTML = `<textarea name="tareas" class="tareas" placeholder="Tareas"></textarea>`;

    let celdaPistas = document.createElement("td");
    celdaPistas.innerHTML = `<textarea name="pistas" class="pistas" placeholder="Pistas"></textarea>`;

    let celdaEntrada = document.createElement("td");
    celdaEntrada.innerHTML = `<textarea name="entrada" class="entrada" placeholder="Entrada"></textarea>`;

    let celdaSalida = document.createElement("td");
    celdaSalida.innerHTML = `<textarea name="salida" class="salida" placeholder="Salida"></textarea>`;

    let celdaDefinicion = document.createElement("td");
    celdaDefinicion.innerHTML = `<textarea name="definicion" class="definicion" placeholder="Definición"></textarea>`;

    let celdaUml = document.createElement("td");
    celdaUml.innerHTML = `<input type="text" name="uml" class="uml" placeholder="UML">`;

    let celdaPrueba = document.createElement("td");
    celdaPrueba.innerHTML = `<input type="text" name="prueba" class="prueba" placeholder="Prueba">`;

    let celdaLenguaje = document.createElement("td");
    celdaLenguaje.innerHTML = `<input type="text" name="lenguaje" class="lenguaje" placeholder="Lenguaje">`;

    let celdaBotonEnviar = document.createElement("td");
    celdaBotonEnviar.innerHTML = `<button type="submit" class="boton-enviar">Enviar</button>`;

    fila.appendChild(celdaId);
    fila.appendChild(celdaIdUnico);
    fila.appendChild(celdaTitulo);
    fila.appendChild(celdaNivel);
    fila.appendChild(celdaTipo);
    fila.appendChild(celdaEnunciado);
    fila.appendChild(celdaTareas);
    fila.appendChild(celdaPistas);
    fila.appendChild(celdaEntrada);
    fila.appendChild(celdaSalida);
    fila.appendChild(celdaDefinicion);
    fila.appendChild(celdaUml);
    fila.appendChild(celdaPrueba);
    fila.appendChild(celdaLenguaje);
    fila.appendChild(celdaBotonEnviar);

    tbody.appendChild(fila);
    document.querySelector(".titulo").focus();
    document.querySelector(".titulo").setAttribute("required", "required");
    document.querySelector(".nivel").setAttribute("required", "required");
    document.querySelector(".tipo").setAttribute("required", "required");
    document.querySelector(".enunciado").setAttribute("required", "required");
    document.querySelector(".tareas").setAttribute("required", "required");
    document.querySelector(".pistas").setAttribute("required", "required");
    document.querySelector(".entrada").setAttribute("required", "required");
    document.querySelector(".salida").setAttribute("required", "required");
    document.querySelector(".definicion").setAttribute("required", "required");
    document.querySelector(".uml").setAttribute("required", "required");
    document.querySelector(".prueba").setAttribute("required", "required");
    document.querySelector(".lenguaje").setAttribute("required", "required");

    document.getElementById("boton-agregar").style.display = "none";
    document.getElementById("boton-cancelar").style.display = "inline-block";
}

function cancelarEjercicio() {
    let filaAgregar = document.getElementById("fila-agregar");

    if (filaAgregar) {
        filaAgregar.remove();
    }

    document.getElementById("boton-agregar").style.display = "inline-block";
    document.getElementById("boton-cancelar").style.display = "none";
}

function editarEjercicio(filaEditar) {
    let fila = filaEditar.closest("tr");

    let celdaTitulo = fila.children[2];
    let celdaNivel = fila.children[3];
    let celdaTipo = fila.children[4];
    let celdaEnunciado = fila.children[5];
    let celdaTareas = fila.children[6];
    let celdaPistas = fila.children[7];
    let celdaEntrada = fila.children[8];
    let celdaSalida = fila.children[9];
    let celdaDefinicion = fila.children[10];
    let celdaUml = fila.children[11];
    let celdaPrueba = fila.children[12];
    let celdaLenguaje = fila.children[13];
    let celdaGestion = fila.children[14];

    let valorTitulo = celdaTitulo.innerText.trim();
    let valorNivel = celdaNivel.innerText.trim();
    let valorTipo = celdaTipo.innerText.trim();
    let valorEnunciado = celdaEnunciado.innerText.trim();
    let valorTareas = celdaTareas.innerText.trim();
    let valorPistas = celdaPistas.innerText.trim();
    let valorEntrada = celdaEntrada.innerText.trim();
    let valorSalida = celdaSalida.innerText.trim();
    let valorDefinicion = celdaDefinicion.innerText.trim();
    let valorUml = celdaUml.innerText.trim();
    let valorPrueba = celdaPrueba.innerText.trim();
    let valorLenguaje = celdaLenguaje.innerText.trim();

    let urlEliminar = fila.querySelector(".gestion a:nth-child(2)").href;

    celdaTitulo.innerHTML = `<input type="text" name="titulo" value="${valorTitulo}" class="titulo">`;
    celdaNivel.innerHTML = `<input type="text" name="nivel" value="${valorNivel}" class="nivel">`;
    celdaTipo.innerHTML = `<input type="text" name="tipo" value="${valorTipo}" class="tipo">`;
    celdaEnunciado.innerHTML = `<textarea name="enunciado" class="enunciado">${valorEnunciado}</textarea>`;
    celdaTareas.innerHTML = `<textarea name="tareas" class="tareas">${valorTareas}</textarea>`;
    celdaPistas.innerHTML = `<textarea name="pistas" class="pistas">${valorPistas}</textarea>`;
    celdaEntrada.innerHTML = `<textarea name="entrada" class="entrada">${valorEntrada}</textarea>`;
    celdaSalida.innerHTML = `<textarea name="salida" class="salida">${valorSalida}</textarea>`;
    celdaDefinicion.innerHTML = `<textarea name="definicion" class="definicion">${valorDefinicion}</textarea>`;
    celdaUml.innerHTML = `<input type="text" name="uml" value="${valorUml}" class="uml">`;
    celdaPrueba.innerHTML = `<input type="text" name="prueba" value="${valorPrueba}" class="prueba">`;
    celdaLenguaje.innerHTML = `<input type="text" name="lenguaje" value="${valorLenguaje}" class="lenguaje">`;

    celdaGestion.innerHTML = `
        <div class="gestion">
            <a href="#" onclick="guardarEjercicio(this)" class="boton-guardar"><span class="material-symbols-outlined">save</span></a>
            <a href="#" class="boton-cancelar" 
            data-titulo="${valorTitulo}"
            data-nivel="${valorNivel}"
            data-tipo="${valorTipo}"
            data-enunciado="${valorEnunciado}"
            data-tareas="${valorTareas}"
            data-pistas="${valorPistas}"
            data-entrada="${valorEntrada}"
            data-salida="${valorSalida}"
            data-definicion="${valorDefinicion}"
            data-uml="${valorUml}"
            data-prueba="${valorPrueba}"
            data-lenguaje="${valorLenguaje}"
            data-urlEliminar="${urlEliminar}"
            onclick="cancelarEdicion(this)">
            <span class="material-symbols-outlined">close</span>
            </a>
        </div>`
    ;
}

function guardarEjercicio(filaEditar) {
    let fila = filaEditar.closest("tr");
    let idUnico = fila.children[1].innerText.trim();

    let formulario = fila.closest("form");

    formulario.action = `/editar_ejercicio/${idUnico}/`;

    formulario.submit();
}

function cancelarEdicion(enlaceCancelar) {
    const fila = enlaceCancelar.closest("tr");
    const e = enlaceCancelar.dataset;

    fila.children[2].innerText = e.titulo;
    fila.children[3].innerText = e.nivel;
    fila.children[4].innerText = e.tipo;
    fila.children[5].innerText = e.enunciado;
    fila.children[6].innerText = e.tareas;
    fila.children[7].innerText = e.pistas;
    fila.children[8].innerText = e.entrada;
    fila.children[9].innerText = e.salida;
    fila.children[10].innerText = e.definicion;
    fila.children[11].innerText = e.uml;
    fila.children[12].innerText = e.prueba;
    fila.children[13].innerText = e.lenguaje;

    fila.children[14].innerHTML = `
        <div class="gestion">
            <a href="#" onclick="editarEjercicio(this)"><span class="material-symbols-outlined">edit</span></a>
            <a href="${e.url}"><span class="material-symbols-outlined">delete</span></a>
        </div>
    `;
}