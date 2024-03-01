document.addEventListener('DOMContentLoaded', function() {
    // Llenar la lista desplegable con los datos de la columna "Nombre de la Columna"
    var columnData = [];
    var tableRows = document.querySelectorAll("#data-table tbody tr");

    tableRows.forEach(function(row) {
        var cellText = row.cells[0].innerText; // Asumimos que la columna "Nombre de la Columna" es la primera
        if (columnData.indexOf(cellText) === -1) {
            columnData.push(cellText);
        }
    });

    var searchInput = document.getElementById('searchInput');

    // Agregar opción para mostrar todas las filas
    var optionAll = document.createElement('option');
    optionAll.value = 'Todas';
    optionAll.innerText = 'Mostrar Todas';
    searchInput.appendChild(optionAll);

    // Agregar opciones de la columna a la lista desplegable
    columnData.forEach(function(data) {
        var option = document.createElement('option');
        option.value = data;
        option.innerText = data;
        searchInput.appendChild(option);
    });

    // Activar Select2 en el elemento
    $('#searchInput').select2({
        placeholder: "Seleccione un valor para buscar",
        allowClear: true
    });

    // Evento para manejar la búsqueda
    $('#searchInput').on('change', function() {
        console.log("Evento change detectado. Valor seleccionado: ", this.value);
        searchFunction(this.value);
    });
});

function searchFunction(searchTerm) {
    var table, tr, i, td, txtValue;
    table = document.getElementById("data-table");
    tr = table.getElementsByTagName("tr");

    // Iterar sobre todas las filas de la tabla, excepto la cabecera
    for (i = 1; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[0]; // Primera columna, donde se espera el valor a comparar
        if (td) {
            txtValue = td.textContent || td.innerText;
            if (txtValue.toUpperCase() === searchTerm.toUpperCase()) {
                tr[i].style.display = ""; // Mostrar la fila si el valor coincide
            } else {
                tr[i].style.display = "none"; // Ocultar la fila si no coincide
            }
        }       
    }

    // Caso especial para 'Todas'
    if (searchTerm.toUpperCase() === 'TODAS') {
        for (i = 1; i < tr.length; i++) {
            tr[i].style.display = ""; // Mostrar todas las filas
        }
    }
}
