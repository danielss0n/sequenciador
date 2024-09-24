const socket = io();

socket.on('update_sequencia_aguardando', (data) => {
    const tabela = document.getElementById('data-table-body');
    tabela.innerHTML = '';

    data.forEach((item, index) => {
        const tr = document.createElement('tr');
        tr.setAttribute('draggable', 'true');
        tr.className = item.tinta === 'Fundo' ? 'tinta-fundo' :
                      item.tinta === 'Intermediaria' ? 'tinta-intermediaria' :
                      item.tinta === 'Azul' ? 'tinta-azul' :
                      item.tinta === 'Laranja' ? 'tinta-laranja' : '';
        
        tr.innerHTML = `
            <td>${item.em_progresso}</td>
            <td>${item.peca}</td>
            <td>${item.tinta}</td>
            <td class="celula_acoes">
                ${item.em_progresso ? 'Em processo de pintura' : 
                  '<i class="bi bi-arrow-up-circle-fill" style="font-size: 25px;" onclick="moverPecaParaCima(this)"></i>' +
                  '<i class="bi bi-arrow-down-circle-fill" style="font-size: 25px;" onclick="moverPecaParaBaixo(this)"></i>'}
            </td>
        `;
        tabela.appendChild(tr);

        tr.addEventListener('dragstart', (event) => {
            event.dataTransfer.setData('text/plain', index);
            event.dataTransfer.effectAllowed = 'move';
        });

        tr.addEventListener('dragover', (event) => {
            event.preventDefault();
        });

        tr.addEventListener('drop', (event) => {
            event.preventDefault();
            const draggedIndex = event.dataTransfer.getData('text/plain');
            const rows = Array.from(tabela.children);
            const draggedRow = rows[draggedIndex];
            const targetRow = rows[index];


            if (draggedIndex !== index.toString()) {
                
                tabela.insertBefore(draggedRow, rows[index + (draggedIndex < index ? 1 : 0)]);
                preparadorEnviarModificacaoAguardando()
            }
        });
    });
});
