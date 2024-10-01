const socket = io();

socket.on('update_sequencia_aprovada', function(data) {

    const tbody = document.getElementById('data-table-body');
    tbody.innerHTML = '';

    data.forEach(item => {
        const row = document.createElement('tr');

        row.className = `${item.tinta}`

        const progressoCell = document.createElement('td');
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.checked = item.em_progresso;
        checkbox.onclick = function() { EmProgressoPeca(this); };
        progressoCell.appendChild(checkbox);
        progressoCell.appendChild(document.createTextNode('Em progresso'));
        row.appendChild(progressoCell);

        row.appendChild(createCell(item.etapa_anterior));
        row.appendChild(createCell(item.peca));
        row.appendChild(createCell(item.tinta));

        const finalizarCell = document.createElement('td');
        const finalizarIcon = document.createElement('i');
        finalizarIcon.className = 'bi bi-check2-square';
        finalizarIcon.onclick = function() { FinalizarPeca(this); };
        finalizarCell.appendChild(finalizarIcon);
        row.appendChild(finalizarCell);

        tbody.appendChild(row);
    });
});

function createCell(content) {
    const cell = document.createElement('td');
    cell.textContent = content;
    return cell;
}
