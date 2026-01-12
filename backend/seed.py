import sys
import os
import random
from datetime import date, timedelta, datetime
from dotenv import load_dotenv

# 1. Carrega variáveis de ambiente (.env)
load_dotenv()

# Adiciona o diretório atual ao path
sys.path.append(os.getcwd())

# Importações do SQLAlchemy e Models
from app.core.database import SessionLocal
from app.models.medicamento import Medicamento
from app.models.lote import Lote
from app.models.saida import Saida

db = SessionLocal()

def seed_data():
    print("🌱 Iniciando Seed Completo (Estrutura Normalizada)...")

    # ==============================================================================
    # 1. MEDICAMENTOS (BASE GENÉRICA)
    # Apenas identidade do remédio.
    # ==============================================================================
    print("💊 Criando Catálogo de Medicamentos Genéricos...")
    
    lista_base = [
        {"nome": "Dipirona Monohidratada", "principio": "Dipirona", "tarja": "Sem Tarja"},
        {"nome": "Amoxicilina", "principio": "Amoxicilina", "tarja": "Vermelha"},
        {"nome": "Clonazepam", "principio": "Clonazepam", "tarja": "Preta"},
        {"nome": "Losartana Potássica", "principio": "Losartana", "tarja": "Vermelha"},
        {"nome": "Paracetamol", "principio": "Paracetamol", "tarja": "Sem Tarja"},
        {"nome": "Omeprazol", "principio": "Omeprazol", "tarja": "Sem Tarja"},
        {"nome": "Simvastatina", "principio": "Simvastatina", "tarja": "Vermelha"},
        {"nome": "Ibuprofeno", "principio": "Ibuprofeno", "tarja": "Sem Tarja"},
        {"nome": "Diazepam", "principio": "Diazepam", "tarja": "Preta"},
        {"nome": "Metformina", "principio": "Metformina", "tarja": "Vermelha"},
        {"nome": "Captopril", "principio": "Captopril", "tarja": "Vermelha"},
        {"nome": "Atenolol", "principio": "Atenolol", "tarja": "Vermelha"},
    ]

    ids_meds = {} # Mapa { "Nome": ID_Banco }

    for m in lista_base:
        med = db.query(Medicamento).filter(Medicamento.nome == m["nome"]).first()
        if not med:
            med = Medicamento(
                nome=m["nome"],
                principio_ativo=m["principio"],
                tarja=m["tarja"]
            )
            db.add(med)
            db.commit()
            db.refresh(med)
        ids_meds[m["nome"]] = med.id_medicamento

    # ==============================================================================
    # 2. LOTES (ESTOQUE DETALHADO)
    # Aqui definimos Fabricante, Dosagem, Validade e Cenários de Alerta
    # ==============================================================================
    print("📦 Criando Lotes com Detalhes (Cenários Dashboard)...")
    hoje = date.today()
    
    # Lista para guardar lotes válidos para gerar saídas depois
    lotes_disponiveis = []

    def criar_lote(nome_med, fab, dosagem, cat, qtd, dias_validade, prefixo_lote):
        if nome_med not in ids_meds: return

        # Gera número aleatório para simular caixa real
        num_lote = f"{prefixo_lote}-{random.randint(1000,9999)}"
        
        if not db.query(Lote).filter(Lote.numero_lote == num_lote).first():
            lote = Lote(
                id_medicamento=ids_meds[nome_med],
                numero_lote=num_lote,
                numero_caixa=f"CX-{random.randint(10,99)}",
                quantidade_inicial=qtd + 100,
                quantidade_atual=qtd,
                quantidade_por_caixa=20,
                data_fabricacao=hoje - timedelta(days=150),
                data_validade=hoje + timedelta(days=dias_validade),
                
                # --- NOVOS CAMPOS NORMALIZADOS ---
                # Agora o fabricante e a dosagem ficam aqui no Lote
                fabricante=fab,
                dosagem=dosagem,
                categoria=cat,
                descricao=f"Lote {num_lote} de {nome_med} {dosagem} ({fab})"
            )
            db.add(lote)
            db.commit()
            db.refresh(lote)
            
            # Se for um lote bom para venda (tem estoque e não venceu), guarda na lista
            if qtd > 0 and dias_validade > 0:
                lotes_disponiveis.append(lote)

    # --- CENÁRIOS DE TESTE ---

    # A. VENCIDOS (Dashboard Card Vermelho)
    criar_lote("Clonazepam", "Roche", "2.5mg/ml", "Ansiolítico", 30, -20, "VENC") 
    criar_lote("Amoxicilina", "Prati", "500mg", "Antibiótico", 50, -5, "VENC")

    # B. PRÓXIMO VENCIMENTO (Dashboard Card Amarelo)
    criar_lote("Simvastatina", "EMS", "20mg", "Hipolipemiante", 100, 15, "ALERT") 
    criar_lote("Paracetamol", "Teuto", "750mg", "Analgésico", 150, 25, "ALERT")

    # C. BAIXO ESTOQUE (Dashboard Tabela)
    criar_lote("Losartana Potássica", "Neo Química", "50mg", "Anti-hipertensivo", 5, 300, "BAIXO") 
    criar_lote("Diazepam", "Eurofarma", "10mg", "Ansiolítico", 12, 400, "BAIXO")

    # D. ESTOQUE SAUDÁVEL (Verde - Para gerar volume de saídas)
    criar_lote("Dipirona Monohidratada", "Medley", "500mg", "Analgésico", 500, 700, "OK")
    criar_lote("Dipirona Monohidratada", "EMS", "1g", "Analgésico", 300, 600, "OK") # Mesmo remédio, outro detalhe
    
    criar_lote("Ibuprofeno", "Bayer", "600mg", "Anti-inflamatório", 400, 500, "OK")
    criar_lote("Metformina", "Prati", "850mg", "Antidiabético", 250, 365, "OK")
    criar_lote("Omeprazol", "Medley", "20mg", "Antiúlcera", 300, 400, "OK")
    criar_lote("Captopril", "Teuto", "25mg", "Anti-hipertensivo", 200, 500, "OK")
    criar_lote("Atenolol", "Sandoz", "50mg", "Anti-hipertensivo", 150, 450, "OK")

    # ==============================================================================
    # 3. SAÍDAS / DISPENSAÇÕES (HISTÓRICO)
    # Gera dados mês a mês para o Gráfico de Linha e Relatórios
    # ==============================================================================
    print("📉 Gerando Histórico de Dispensações (Jan - Hoje)...")
    
    mes_atual = hoje.month
    ano_atual = hoje.year

    # Helper para gerar CNS fictício
    def gerar_cns_fake():
        return f"7{random.randint(10000000000000, 99999999999999)}"

    # Helper para nomes fictícios
    nomes_pacientes = ["Maria Silva", "José Santos", "Ana Oliveira", "Pedro Souza", "Lucas Lima", "Carla Dias", "João da Silva"]

    # Loop pelos meses do ano
    for mes in range(1, mes_atual + 1):
        # Quantidade aleatória de atendimentos no mês
        qtd_atendimentos = random.randint(15, 30)
        
        for _ in range(qtd_atendimentos):
            if not lotes_disponiveis: break
            
            # Escolhe um lote aleatório dos disponíveis
            lote_escolhido = random.choice(lotes_disponiveis)
            nome_med = lote_escolhido.medicamento.nome

            # Lógica para viciar o gráfico de "Mais Retirados":
            if nome_med == "Dipirona Monohidratada":
                qtd_retirada = random.randint(4, 8)
            elif nome_med == "Amoxicilina":
                qtd_retirada = random.randint(2, 5)
            else:
                qtd_retirada = random.randint(1, 2)
            
            # Gera data aleatória dentro do mês correto
            dia_max = 28 
            data_simulada = datetime(ano_atual, mes, random.randint(1, dia_max), 10, 0, 0)

            # Cria a saída sem usuário/paciente ID (apenas texto, conforme sua nova arquitetura)
            saida = Saida(
                id_lote=lote_escolhido.id_lote,
                # Dados do Paciente (String)
                cns_paciente=gerar_cns_fake(),
                nome_paciente=random.choice(nomes_pacientes),
                numero_receita=f"REC-{random.randint(100,999)}/{ano_atual}",
                
                # Dados da Transação
                quantidade=qtd_retirada,
                tipo_saida="Receita Médica",
                observacao="Seed Automático",
                data_saida=data_simulada # Importante para o gráfico de linha
            )
            db.add(saida)
    
    db.commit()
    print("✅ Banco Populado com Sucesso!")
    print("   -> Teste o Dashboard: GET /api/v1/dashboard")
    print("   -> Teste a Listagem: GET /api/v1/medicamentos")
    print("   -> Teste o Relatório PDF: GET /api/v1/relatorios/geral/pdf")
    db.close()

if __name__ == "__main__":
    seed_data()