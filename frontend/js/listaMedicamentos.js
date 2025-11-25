const API_BASE = 'http://localhost:8000/api/v1';

let medicamentos = [];

document.addEventListener("DOMContentLoaded", () => {
    const tbody = document.getElementById("tbodyMedicamentos");
    const filtro = document.getElementById("filtro");
    const btnLimpar = document.getElementById("btnLimpar");

    if (!tbody || !filtro || !btnLimpar) {
        console.error("Elementos da página não encontrados.");
        return;
    }

    carregarMedicamentos();

    filtro.addEventListener("input", () => {
        const termo = filtro.value.toLowerCase();
        const filtrados = medicamentos.filter(med => {
            return Object.values(med).some(valor =>
                String(valor).toLowerCase().includes(termo)
            );
        });
        renderizarTabela(filtrados);
    });

    btnLimpar.addEventListener("click", () => {
        filtro.value = "";
        renderizarTabela(medicamentos);
    });
});

async function carregarMedicamentos() {
    try {
        const response = await fetch(`${API_BASE}/medicamentos/`);
        const data = await response.json();
        medicamentos = data;

        renderizarTabela(medicamentos);

    } catch (error) {
        console.error("Erro ao carregar medicamentos:", error);
    }
}

function renderizarTabela(lista) {
    const tbody = document.getElementById("tbodyMedicamentos");
    const cardSemDados = document.getElementById("cardSemDados");

    tbody.innerHTML = "";

    if (!lista.length) {
        cardSemDados.style.display = "block";
        return;
    } else {
        cardSemDados.style.display = "none";
    }

    lista.forEach(med => {
        const tr = document.createElement("tr");

        tr.innerHTML = `
            <td>${med.id_medicamento}</td>
            <td>${med.nome}</td>
            <td>${med.fabricante}</td>
            <td>${med.principio_ativo}</td>
            <td>${med.dosagem}</td>
            <td>${med.categoria}</td>
            <td>${med.tarja}</td>
            <td>
                <span class="status-${med.status_geral.toLowerCase()}">
                    ${med.status_geral}
                </span>
            </td>
            <td>${med.descricao}</td>
            <td>${formatarData(med.criado_em)}</td>
        `;

        tbody.appendChild(tr);
    });
}

function formatarData(dataISO) {
    const data = new Date(dataISO);
    return data.toLocaleDateString("pt-BR") + " " + data.toLocaleTimeString("pt-BR");
}
