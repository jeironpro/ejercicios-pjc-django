var editor = ace.edit("editor");
editor.setTheme("ace/theme/chrome");
editor.session.setMode("ace/mode/python");
editor.getSession().setTabSize(4);
editor.getSession().setUseSoftTabs(true);

function setPreferencies(editor, mida, tema) {
    editor.setFontSize(mida);
    editor.setTheme("ace/theme/" + tema);
}

var getMedidaLetra = document.getElementById("medida");
var getTema = document.getElementById("tema");

getMedidaLetra.addEventListener("change", function() {
    var selMedidaLetra = getMedidaLetra.value;
    var selTema = getTema.value;
    
    setPreferencies(editor, parseInt(selMedidaLetra), selTema);
});

getTema.addEventListener("change", function() {
    var selMedidaLetra = getMedidaLetra.value;
    var selTema = getTema.value;

    setPreferencies(editor, parseInt(selMedidaLetra), selTema);
});

setPreferencies(editor, parseInt(getMedidaLetra.value), getTema.value);

function posicionCursor() {
    var longLinia = editor.getSession().getLength();
    var contLinia = editor.getSession().getLine(0).trim();
    var posLinia = 0;
    
    for (var i = 0; i < longLinia; i++) {
        var linia = editor.getSession().getLine(i).trim();
        if (linia.length > 0) {
            posLinia = i;
        }
    }
    
    if (contLinia.length > 0) {
        if (longLinia === 1) {
            editor.session.insert({row: 1, column: 0}, '\n    ');
            setTimeout(() => {
                editor.moveCursorTo(1, 4);
                editor.focus();
            }, 10);
        } else if (longLinia > 1) {
            var ultimaLinia = editor.getSession().getLine(posLinia).length;
            editor.moveCursorTo(posLinia, ultimaLinia);
            editor.focus();
        }
    }
}
posicionCursor();

async function ejecutarPrueba() {
    var codigoUsuario = editor.getValue();
    var idUnico = document.getElementById("editor").dataset.idunico;
    const lenguaje = document.getElementById("lenguaje").value;

    let resposta = await fetch("/ejecuta_prueba/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ codigo: codigoUsuario, id_unico: idUnico, lenguaje: lenguaje })
    });

    let datos = await resposta.json();
    let tbody = document.getElementById("pruebas").getElementsByTagName("tbody")[0];
    tbody.innerHTML = "";

    const tabla = document.getElementById("pruebas")
    tabla.style.display = "block";

    const pasaTodas = document.getElementById("pasa-todas");
    let contador = 0;
    
    datos.resultados.forEach(function(prueba) {
        let fila = tbody.insertRow();
        let celdaPrueba = fila.insertCell();
        let celdaEsperado = fila.insertCell();
        let celdaResultado = fila.insertCell();
        let celdaPasa = fila.insertCell();
        
        celdaPrueba.textContent = prueba.prueba;
        celdaEsperado.textContent = prueba.esperado;
        celdaResultado.textContent = prueba.resultado;
        
        if (String(prueba.esperado) === String(prueba.resultado)) {
            celdaPasa.textContent = "✅";
        } else {
            celdaPasa.textContent = "❌";
            contador++;
        }
    });
    if (contador == 0) {
        pasaTodas.innerHTML = "<p>&#x1F389; Felicidades pasa todas las pruebas.</p>"
    } else {
        pasaTodas.innerHTML = ""
    }
};