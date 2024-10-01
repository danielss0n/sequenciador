const socket = io();

socket.on('update_sequencia_aguardando', (newData) => {
    const tbody = document.getElementById('lista-solicitacao');
    tbody.innerHTML = '';



    newData.forEach((item, index) => {
        const tr = document.createElement('tr');
        var elementoIcone = ""
        if(item.casas_movidas < 0) {
            classeCimaOuBaixo = "movido-baixo"
            elementoIcone = `<i class="bi bi-caret-down-fill"></i>${item.casas_movidas}`
        }
        if(item.casas_movidas > 0) {
            classeCimaOuBaixo = "movido-cima"
            elementoIcone = `<i class="bi bi-caret-up-fill"></i>${item.casas_movidas}`
        }

        if(item.casas_movidas == 99) {
            classeCimaOuBaixo = "nova-peca"
            elementoIcone = `<i class="bi bi-caret-left-fill"></i> novo`
        }

        if(item.casas_movidas == 0) {
            classeCimaOuBaixo = ""
            elementoIcone = ""
        }

        var casasMovidas = ""
        if(item.casas_movidas != 0) {
            casasMovidas = `${item.casas_movidas}`
        }

        tr.className = item.tinta;
        
        tr.innerHTML = `
            <td><span class="${classeCimaOuBaixo}">${index + 1}</span></td>
            <td>${item.etapa_anterior}</td>
            <td>
                ${item.peca} <span class="${classeCimaOuBaixo}">${elementoIcone}</span>
            </td>
            <td>${item.tinta}</span></td>
            <td><span>${item.em_progresso}</span></td>
        `;
        tbody.appendChild(tr);
    });
});

socket.on('update_sequencia_aprovada', (newData) => {
    const tbody = document.getElementById('lista-aprovada');
    tbody.innerHTML = '';

    console.log(newData)
    newData.forEach((item, index) => {
        const tr = document.createElement('tr');
        tr.className = item.tinta;
        tr.innerHTML = `
            <td>${index + 1}</td>
            <td>${item.etapa_anterior}</td>
            <td>${item.peca}</td>
            <td>${item.tinta}</td>
            <td>${item.em_progresso}</td>
        `;
        tbody.appendChild(tr);
    });
});

socket.on('usuario_que_modificou', (usuario) => {
    const elemento_titulo = document.getElementById('titulo-usuario-modificou');
    elemento_titulo.innerHTML = `SEQUÊNCIA MODIFICADA POR ${usuario.toUpperCase()}`
})
