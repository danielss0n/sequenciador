function FinalizarPeca(element) {
    var row = element.closest('tr');
    peca = row.cells[1].textContent;
    tinta = row.cells[2].textContent;

    fetch('http://10.1.39.20:5000/operador/peca-finalizar', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},

        body: JSON.stringify({
            peca: peca.trim(),
            tinta: tinta.trim(),
        })

    })
}

function EmProgressoPeca(element) {
    var row = element.closest('tr');
    peca = row.cells[1].textContent;
    
    fetch('http://10.1.39.20:5000/operador/peca-em-progresso', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},

        body: JSON.stringify({
            peca: peca.trim()
        })

    })
}