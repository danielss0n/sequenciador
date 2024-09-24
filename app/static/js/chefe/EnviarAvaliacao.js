function enviarAprovacao() {
    fetch('http://10.1.39.20:5000/chefe/aprovacao', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: ""
    })
}

function enviarReprovacao() {
    fetch('http://10.1.39.20:5000/chefe/reprovacao', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: "" 
    })
}

function pegarJsonTabela() {
    const tabela = document.getElementById("lista-solicitacao");
    const dados = [];
    for (let i = 0; i < tabela.rows.length; i++) {
        const linha = tabela.rows[i];
        const emProgresso = linha.cells[1].textContent
        if (emProgresso == "true") {
            emProgresso == true
        }
        if (emProgresso == "false") {
            emProgresso == false
        }
        const peca = linha.cells[2].textContent
        const tinta = linha.cells[3].textContent
        dados.push({
            peca: peca.trim(),
            tinta: tinta.trim(),
            em_progresso: emProgresso
        });
    }
    console.log(dados)
    return dados
}
