import sys
import os
from datetime import date, timedelta
from passlib.context import CryptContext 

# Adiciona o diretório atual ao path para encontrar o 'app'
sys.path.append(os.getcwd())

# Importações do SQLAlchemy e Models
from app.core.database import SessionLocal
# Importações dos models mantidas para evitar erros de referência,
# mas o foco será apenas na criação do Lote.
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
    print("🌱 Iniciando a inserção de Lote...")

    # --- 4. LOTES (ESTOQUE) ---
    print("📦 Criando 1 Lote com Validade em 2024...")
    hoje = date.today()
    
    # Define o Lote
    num_lote = "LOTE2024-001"
    
    # Define a data de validade para 2024 (Ex: 31 de Dezembro de 2024)
    data_validade_2024 = date(2024, 12, 31) 
    
    # Define a data de fabricação (Ex: 6 meses antes da validade)
    data_fabricacao = data_validade_2024 - timedelta(days=180) 

    if not db.query(Lote).filter(Lote.numero_lote == num_lote).first():
        lote = Lote(
            # ATENÇÃO: É necessário que o Medicamento com id_medicamento=4 exista.
            id_medicamento=4, 
            numero_lote=num_lote,
            numero_caixa="CX-2024",
            quantidade_inicial=250,
            quantidade_atual=250,
            quantidade_por_caixa=25,
            data_validade=data_validade_2024, # <-- Validade em 2024
            data_fabricacao=data_fabricacao,
        )
        db.add(lote)
        db.commit()
        print(f"   Lote '{num_lote}' (Validade: {data_validade_2024}) adicionado com sucesso.")
    else:
        print(f"   Lote '{num_lote}' já existe, pulando.")

    print("✅ Inserção concluída!")
    db.close()

if __name__ == "__main__":
    seed_data()