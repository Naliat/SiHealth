// Ajustar conforme o backend
const API_BASE = '';

const tbody = document.getElementById('tbodyMedicamentos');
const statusEl = document.getElementById('status');
const inputFiltro = document.getElementById('filtro');
const btnLimpar = document.getElementById('btnLimpar');
const cardSemDados = document.getElementById('cardSemDados');

let dados = [];
let filtrados = [];

function formatarData(iso) {
  if (!iso) return '';
  const d = new Date(iso);
  if (isNaN(d.getTime())) return '';
  return d.toLocaleDateString('pt-BR') + ' ' + d.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
}

function renderTabela(rows) {
  tbody.innerHTML = '';
  if (!rows || rows.length === 0) {
    cardSemDados.style.display = 'block';
    return;
  }
  cardSemDados.style.display = 'none';
  const frag = document.createDocumentFragment();
  rows.forEach(m => {
    const tr = document.createElement('tr');
    const c = (t) => { const td = document.createElement('td'); td.textContent = t ?? ''; return td; };
    tr.append(
      c(m.nome),
      c(m.fabricante),
      c(m.principio_ativo),
      c(m.dosagem),
      c(m.categoria),
      c(formatarData(m.criado_em))
    );
    frag.appendChild(tr);
  });
  tbody.appendChild(frag);
}

function aplicarFiltro() {
  const q = (inputFiltro.value || '').toLowerCase().trim();
  if (!q) {
    filtrados = dados;
  } else {
    filtrados = dados.filter(m =>
      (m.nome || '').toLowerCase().includes(q) ||
      (m.principio_ativo || '').toLowerCase().includes(q) ||
      (m.fabricante || '').toLowerCase().includes(q)
    );
  }
  renderTabela(filtrados);
}

async function carregar() {
  try {
    const resp = await fetch(`${API_BASE}/medicamentos/`);
    if (!resp.ok) throw new Error(`Erro ${resp.status}`);
    dados = await resp.json();
    statusEl.textContent = `${dados.length} medicamento(s) encontrados`;
    filtrados = dados;
    aplicarFiltro();
  } catch (err) {
      console.error(err);
      dados = [
          {
              nome: 'Dipirona 500mg',
              fabricante: 'Medley',
              principio_ativo: 'Dipirona Monoidratada',
              dosagem: '500mg',
              categoria: 'Analgésico',
              criado_em: '2024-02-20T10:00:00'
          },
          {
              nome: 'Amoxicilina 500mg',
              fabricante: 'EMS',
              principio_ativo: 'Amoxicilina',
              dosagem: '500mg',
              categoria: 'Antibiótico',
              criado_em: '2024-02-19T14:30:00'
          },
          {
              nome: 'Omeprazol 20mg',
              fabricante: 'Medley',
              principio_ativo: 'Omeprazol',
              dosagem: '20mg',
              categoria: 'Antiácido',
              criado_em: '2024-02-18T09:15:00'
          }
      ];
      filtrados = dados;
      aplicarFiltro();
  }
}

inputFiltro.addEventListener('input', aplicarFiltro);
btnLimpar.addEventListener('click', () => { inputFiltro.value = ''; aplicarFiltro(); });

carregar();
