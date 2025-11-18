const API = "http://127.0.0.1:8000"; // ajustar conforme o necessario

    async function carregarUsuarios() {
      const res = await fetch(`${API}/usuarios`);
      const data = await res.json();
      const cont = document.getElementById('usuarios');
      cont.innerHTML = '';
      data.forEach(u => {
        const div = document.createElement('div');
        div.className = 'card';
        div.textContent = `${u.nome} — ${u.email}`;
        cont.appendChild(div);
      });
    }

    document.getElementById('formCadastro').addEventListener('submit', async (e) => {
      e.preventDefault();
      const form = e.target;
      const dados = new FormData(form);

      const res = await fetch(`${API}/cadastro`, {
        method: 'POST',
        body: dados
      });

      if (res.ok) {
        form.reset();
        await carregarUsuarios();
        alert('Cadastrado com sucesso!');
      } else {
        alert('Erro ao cadastrar');
      }
    });

    carregarUsuarios();