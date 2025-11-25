import sys
import os
from datetime import date, timedelta
from passlib.context import CryptContext 

# Adiciona o diretório atual ao path para encontrar o 'app'
sys.path.append(os.getcwd())

# Importações do SQLAlchemy e Models
from app.core.database import SessionLocal
from app.models.usuario import Usuario
from app.models.paciente import Paciente
from app.models.medicamento import Medicamento
from app.models.lote import Lote

# --- CONFIGURAÇÃO DE SEGURANÇA LOCAL ---
# Define o contexto de criptografia usando bcrypt, igual ao sistema principal
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hash_local(senha: str):
    """Gera o hash da senha usando bcrypt."""
    return pwd_context.hash(senha)

# Inicia a sessão com o banco
db = SessionLocal()

def seed_data():
    print("🌱 Iniciando o povoamento do banco de dados...")

    # --- 1. USUÁRIOS ---
    print("👤 Criando 10 Usuários...")
    usuarios = [
        {"nome": "Admin Principal", "email": "admin@sihealth.com", "senha": "admin", "ativo": True},
        {"nome": "João Silva", "email": "joao@farmacia.com", "senha": "123", "ativo": True},
        {"nome": "Maria Oliveira", "email": "maria@farmacia.com", "senha": "123", "ativo": True},
        {"nome": "Carlos Souza", "email": "carlos@farmacia.com", "senha": "123", "ativo": True},
        {"nome": "Ana Pereira", "email": "ana@farmacia.com", "senha": "123", "ativo": True},
        {"nome": "Pedro Santos", "email": "pedro@farmacia.com", "senha": "123", "ativo": False},
        {"nome": "Lucia Lima", "email": "lucia@farmacia.com", "senha": "123", "ativo": True},
        {"nome": "Roberto Costa", "email": "roberto@farmacia.com", "senha": "123", "ativo": True},
        {"nome": "Fernanda Alves", "email": "fernanda@farmacia.com", "senha": "123", "ativo": True},
        {"nome": "Lucas Martins", "email": "lucas@farmacia.com", "senha": "123", "ativo": True},
    ]

    for u in usuarios:
        if not db.query(Usuario).filter(Usuario.email == u["email"]).first():
            user = Usuario(
                nome=u["nome"],
                email=u["email"],
                senha_hash=get_hash_local(u["senha"]), # Usa a função local de hash
                ativo=u["ativo"]
            )
            db.add(user)
    db.commit()

    # --- 2. PACIENTES ---
    print("🏥 Criando 10 Pacientes...")
    pacientes = [
        {"nome": "Josefa da Silva", "cns": "111111111110001", "cpf": "111.111.111-11", "nasc": date(1950, 5, 20), "sexo": "F"},
        {"nome": "Antonio Francisco", "cns": "222222222220002", "cpf": "222.222.222-22", "nasc": date(1965, 8, 10), "sexo": "M"},
        {"nome": "Francisca Maria", "cns": "333333333330003", "cpf": "333.333.333-33", "nasc": date(1980, 1, 15), "sexo": "F"},
        {"nome": "Manoel Gomes", "cns": "444444444440004", "cpf": "444.444.444-44", "nasc": date(1990, 12, 5), "sexo": "M"},
        {"nome": "Adriana Melo", "cns": "555555555550005", "cpf": "555.555.555-55", "nasc": date(1995, 3, 25), "sexo": "F"},
        {"nome": "Paulo Ricardo", "cns": "666666666660006", "cpf": "666.666.666-66", "nasc": date(2000, 7, 7), "sexo": "M"},
        {"nome": "Juliana Paes", "cns": "777777777770007", "cpf": "777.777.777-77", "nasc": date(1985, 9, 30), "sexo": "F"},
        {"nome": "Marcos Vinicius", "cns": "888888888880008", "cpf": "888.888.888-88", "nasc": date(1975, 4, 12), "sexo": "M"},
        {"nome": "Beatriz Souza", "cns": "999999999990009", "cpf": "999.999.999-99", "nasc": date(2010, 2, 28), "sexo": "F"},
        {"nome": "Gabriel Medina", "cns": "101010101010010", "cpf": "000.000.000-00", "nasc": date(1993, 11, 22), "sexo": "M"},
    ]

    for p in pacientes:
        if not db.query(Paciente).filter(Paciente.cns == p["cns"]).first():
            pac = Paciente(
                nome=p["nome"], cns=p["cns"], cpf=p["cpf"], 
                data_nascimento=p["nasc"], sexo=p["sexo"]
            )
            db.add(pac)
    db.commit()

    # --- 3. MEDICAMENTOS ---
    print("💊 Criando 10 Medicamentos...")
    medicamentos = [
        {
            "nome": "Dipirona Sódica", "fab": "Medley", "cat": "Analgésico", 
            "tarja": "Sem Tarja", "dosagem": "500mg", "principio_ativo": "Dipirona"
        },
        {
            "nome": "Amoxicilina", "fab": "EMS", "cat": "Antibiótico", 
            "tarja": "Vermelha", "dosagem": "500mg", "principio_ativo": "Amoxicilina"
        },
        {
            "nome": "Clonazepam", "fab": "Eurofarma", "cat": "Ansiolítico", 
            "tarja": "Preta", "dosagem": "2mg", "principio_ativo": "Clonazepam"
        },
        {
            "nome": "Losartana Potássica", "fab": "Neo Química", "cat": "Anti-hipertensivo", 
            "tarja": "Vermelha", "dosagem": "50mg", "principio_ativo": "Losartana"
        },
        {
            "nome": "Paracetamol", "fab": "Teuto", "cat": "Analgésico", 
            "tarja": "Sem Tarja", "dosagem": "750mg", "principio_ativo": "Paracetamol"
        },
        {
            "nome": "Omeprazol", "fab": "Medley", "cat": "Antiúlcera", 
            "tarja": "Sem Tarja", "dosagem": "20mg", "principio_ativo": "Omeprazol"
        },
        {
            "nome": "Simvastatina", "fab": "EMS", "cat": "Hipolipemiante", 
            "tarja": "Vermelha", "dosagem": "20mg", "principio_ativo": "Simvastatina"
        },
        {
            "nome": "Azitromicina", "fab": "Eurofarma", "cat": "Antibiótico", 
            "tarja": "Vermelha", "dosagem": "500mg", "principio_ativo": "Azitromicina"
        },
        {
            "nome": "Diazepam", "fab": "Roche", "cat": "Ansiolítico", 
            "tarja": "Preta", "dosagem": "10mg", "principio_ativo": "Diazepam"
        },
        {
            "nome": "Ibuprofeno", "fab": "Bayer", "cat": "Anti-inflamatório", 
            "tarja": "Sem Tarja", "dosagem": "600mg", "principio_ativo": "Ibuprofeno"
        },
    ]

    ids_meds = []
    for m in medicamentos:
        # Verifica se já existe
        med_existente = db.query(Medicamento).filter(Medicamento.nome == m["nome"]).first()
        
        if not med_existente:
            med = Medicamento(
                nome=m["nome"], 
                fabricante=m["fab"], 
                categoria=m["cat"], 
                tarja=m["tarja"],
                dosagem=m["dosagem"],       
                principio_ativo=m["principio_ativo"], 
                descricao=f"Medicamento {m['nome']} {m['dosagem']} ({m['principio_ativo']}) para tratamento padrão."
            )
            db.add(med)
            db.commit()
            db.refresh(med)
            ids_meds.append(med.id_medicamento)
        else:
            ids_meds.append(med_existente.id_medicamento)

    # --- 4. LOTES (ESTOQUE) ---
    print("📦 Criando 10 Lotes (Estoque)...")
    hoje = date.today()
    validades = [hoje + timedelta(days=365 * (i % 3 + 1)) for i in range(10)]

    for i in range(10):
        num_lote = f"LOTE2025-{i+1:03d}"
        if not db.query(Lote).filter(Lote.numero_lote == num_lote).first():
            # Só tenta criar Lote se tivermos medicamentos suficientes (evita index error)
            if i < len(ids_meds):
                lote = Lote(
                    id_medicamento=ids_meds[i],
                    numero_lote=num_lote,
                    numero_caixa=f"CX-{i+100}",
                    quantidade_inicial=100,
                    quantidade_atual=100,
                    quantidade_por_caixa=10,
                    data_validade=validades[i],
                    data_fabricacao=hoje - timedelta(days=60),
                )
                db.add(lote)
    db.commit()

    print("✅ Banco de dados populado com sucesso!")
    db.close()

if __name__ == "__main__":
    seed_data()