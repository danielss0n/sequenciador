function moverPecaParaCima(element) {
    const linha = element.closest('tr');
    const anterior = linha.previousElementSibling;

    if (anterior) {
        const celulaAnterior = anterior.cells[3];
        if (celulaAnterior && celulaAnterior.textContent.trim() === "Em processo de pintura") {
            return; 
        }
        linha.parentNode.insertBefore(linha, anterior);
    }
    
    preparadorEnviarModificacaoAguardando()
}

function moverPecaParaBaixo(element) {
    const linha = element.closest('tr');
    const proximo = linha.nextElementSibling;

    if (proximo) {
        const celulaProxima = proximo.cells[3];
        if (celulaProxima && celulaProxima.textContent.trim() === "Em processo de pintura") {
            return; 
        }
        linha.parentNode.insertBefore(proximo, linha);
    }
    
    preparadorEnviarModificacaoAguardando();
}

function preparadorEnviarModificacaoAguardando() {
    const dados = pegarJsonTabela()
    fetch('http://10.1.39.20:5000/preparador/mover', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(dados)
    }).then()
}

function preparadorEnviarModificacao() {
    if (!confirm("Notificar o a modificação por email?")) {
        return
    } 
    const dados = pegarJsonTabela()
    fetch('http://10.1.39.20:5000/preparador/enviar-movimentacao', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(dados)
    })
}

function pegarJsonTabela() {
    const tabela = document.getElementById('data-table-body');
    const dados = [];
    for (let i = 0; i < tabela.rows.length; i++) {
        const linha = tabela.rows[i];
        
        var em_progresso = linha.cells[0].textContent.toLowerCase()
        var etapa_anterior = linha.cells[1].textContent;
        var peca = linha.cells[2].textContent;
        var tinta = linha.cells[3].textContent;


        if (em_progresso === "true") {
            em_progresso = true
        }
        if (em_progresso === "false") {
            em_progresso =  false
        }

        peca = peca.toUpperCase()
        tinta = tinta.toUpperCase()
        etapa_anterior = etapa_anterior.toUpperCase()

        dados.push({
            peca: peca.trim(),
            tinta: tinta.trim(),
            etapa_anterior: etapa_anterior,
            em_progresso: em_progresso
        });
    }
    console.log(dados)
    return dados
}

function preparadorRegistrarPeça() {
    window.location.assign('http://10.1.39.20:5000/preparador/registrar-peca');
}   

function postRegistrarPeca() {
    var peca = document.getElementById('peca').value;
    var tinta = document.getElementById('tinta').value;
    var tintaEspecial = document.getElementById('tinta-especial').value;
    var etapa_anterior = document.getElementById('etapa-anterior').value

    if (tintaEspecial.trim() !== "" && tintaEspecial !== null) {
        tinta = tintaEspecial
    }

    if (!peca || !tinta) {
        alert('Por favor, preencha todos os campos.');
        return;
    }

    peca = peca.toUpperCase()
    tinta = tinta.toUpperCase()
    etapa_anterior = etapa_anterior.toUpperCase()

    const dados = {
        peca: peca.trim(),
        tinta: tinta.trim(),
        etapa_anterior: etapa_anterior.trim(),
        em_progresso: false
    };


    fetch('http://10.1.39.20:5000/preparador/registrar-peca', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(dados)
    })
    .then(
        alert("Peça registrada, clique em 'voltar' para sair da página de registro")
    )
}
