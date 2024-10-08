const rows = Array.from(document.getElementsByTagName('tr'));
let draggedRow = null;

rows.forEach(row => {
    row.addEventListener('dragstart', (event) => {
        draggedRow = row;
        event.dataTransfer.effectAllowed = 'move';
    });

    row.addEventListener('dragover', (event) => {
        event.preventDefault(); // Permite o drop
    });

    row.addEventListener('drop', (event) => {
        event.preventDefault();

        if (row !== draggedRow) {
            const tbody = row.parentNode;
            tbody.insertBefore(draggedRow, row.nextSibling);

            preparadorEnviarModificacaoAguardando()
        }
    });
});
