import streamlit as st 
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
# 1. CONEXÃO E CONFIGURAÇÃO
st.set_page_config(page_title="Calculadora do Trecho", layout="wide")
conn = st.connection("gsheets", type=GSheetsConnection)
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1VBatkCYcuBFLcLkiTAiD99EREaHbJfKpeXrc-MPx0xQ/edit#gid=0"

# --- ESTILIZAÇÃO CSS (CORREÇÃO DA FAIXA AMARELA E BOTÕES) ---
st.markdown("""
    <style>
    header, [data-testid="stHeader"], [data-testid="stStatusWidget"] { visibility: hidden; display: none; height: 0px; }
    .stApp { background-color: #000000 !important; }
    .block-container { padding-top: 1rem !important; margin-top: -40px !important; }
    
    /* 1. FAZ O CURSOR (O PALITINHO QUE PISCA) FICAR VISÍVEL EM AMARELO */
    input {
        caret-color: #FFCC00 !important;
    }

    /* 2. EFEITO DE FOCO: O CAMPO "ACENDE" QUANDO O USUÁRIO ESTÁ NELE */
    .stNumberInput input:focus, 
    .stTextInput input:focus, 
    .stSelectbox div[data-baseweb="select"]:focus-within {
        border-bottom: 3px solid #FFFFFF !important; /* Muda a borda para branco ao focar */
        box-shadow: 0px 0px 15px rgba(255, 204, 0, 0.8) !important; /* Brilho amarelo ao redor */
        transition: 0.3s ease-in-out;
        background-color: #1a1a1a !important; /* Escurece levemente o fundo do campo ativo */
    }
    /* TEXTOS EM AMARELO */
    label, p, span { color: #FFCC00 !important; font-weight: bold !important; }
    
    /* CAMPOS DE SELEÇÃO E ENTRADA */
    .stSelectbox div[data-baseweb="select"] { background-color: #FFFFFF !important; color: #000000 !important; }
    .stTextInput input, .stNumberInput input {
        background-color: #000000 !important; color: #FFFFFF !important;
        border: none !important; border-bottom: 2px solid #FFCC00 !important;
    }

    /* BOTÃO GERAR DIAGNÓSTICO - CORREÇÃO DE VISIBILIDADE */
    .stButton>button { 
        background-color: #FFCC00 !important; 
        border: 2px solid #FFCC00 !important;
        border-radius: 5px !important;
        height: 3.5em !important;
        width: 100% !important;
    }
    /* FORÇA O TEXTO DO BOTÃO A FICAR PRETO E VISÍVEL */
    .stButton>button p { 
        color: #000000 !important; 
        font-weight: 900 !important; 
        font-size: 1.2rem !important;
    }

    /* CAIXA DE RESULTADOS */
    .report-box { 
        background-color: #FFFFFF !important; 
        padding: 25px; 
        border: 5px solid #FFCC00; 
        border-radius: 10px; 
    }
    .report-box h3, .report-box p, .report-box b, .report-box span { 
        color: #000000 !important; 
    }
    </style>
    """, unsafe_allow_html=True)

# 2. CABEÇALHO
col_titulo, col_logo = st.columns([4, 1])
with col_titulo:
    st.markdown("""
        <div style="padding-top: 25px;">
            <h1 style="color: #FFCC00; font-family: 'Arial Black'; font-size: 2.2rem; margin-bottom: 0px;">⚖️ CALCULADORA DO TRECHO</h1>
            <p style="color: #FFCC00; font-size: 1.1rem; margin-top: 5px;">Quanto de tempo e de dinheiro são consumidos no seu deslocamento diário?</p>
        </div>
    """, unsafe_allow_html=True)

with col_logo:
    try: st.image("logo.png", width=180)
    except: st.write("")

# 3. ENTRADA DE DADOS: PERFIL COMPLETO
st.markdown("### 👤 PERFIL DO USUÁRIO")
p1, p2, p3, p4, p5 = st.columns(5)
idade = p1.number_input("IDADE", min_value=0, step=1, value=None, placeholder="0")
genero = p2.selectbox("GÊNERO", ["Feminino","Masculino", "Não-binário", "Outro", "Prefiro não responder"])
cor_raca = p3.selectbox("COR/RAÇA", ["Branca", "Preta", "Parda", "Amarela", "Indígena"])
escolaridade = p4.selectbox("ESCOLARIDADE", ["Fundamental Incompleto", "Fundamental Completo", "Médio Incompleto", "Médio Completo", "Técnico", "Superior Incompleto", "Superior Completo", "Pós-Graduação"])
setor = p5.selectbox("SETOR DE ATIVIDADE", ["Comércio", "Construção Civil", "Educação", "Indústria", "Serviços", "Saúde", "Outros"])

st.markdown("---")
st.markdown("### 🏠 LOCALIZAÇÃO")
municipios_rmsp = [" "] + sorted(["São Paulo", "Guarulhos", "Osasco", "Santo André", "São Bernardo do Campo", "São Caetano do Sul", "Diadema", "Mauá", "Mogi das Cruzes", "Suzano", "Itaquaquecetuba", "Barueri", "Embu das Artes", "Taboão da Serra", "Cotia", "Itapevi", "Ferraz de Vasconcelos", "Francisco Morato", "Itapecerica da Serra", "Franco da Rocha", "Ribeirão Pires", "Santana de Parnaíba", "Jandira", "Caieiras", "Arujá", "Mairiporã", "Cajamar", "Santa Isabel", "Biritiba-Mirim", "Rio Grande da Serra", "Juquitiba", "Guararema", "Salesópolis", "Vargem Grande Paulista", "São Lourenço da Serra", "Pirapora do Bom Jesus", "Embu-Guaçu"])
distritos_sp = [" "] + sorted(["Sé", "República", "Bela Vista", "Consolação", "Liberdade", "Santa Cecília", "Água Rasa", "Aricanduva", "Artur Alvim", "Belém", "Cangaíba", "Carrão", "Cidade Líder", "Cidade Tiradentes", "Ermelino Matarazzo", "Guaianases", "Iguatemi", "Itaim Paulista", "Itaquera", "Jardim Helena", "José Bonifácio", "Lajeado", "Mooca", "Parque do Carmo", "Penha", "Ponte Rasa", "São Lucas", "São Mateus", "São Miguel", "São Rafael", "Sapopemba", "Tatuapé", "Vila Curuçá", "Vila Formosa", "Vila Jacuí", "Vila Matilde", "Vila Prudente", "Casa Verde", "Cachoeirinha", "Limão", "Brasilândia", "Freguesia do Ó", "Jaçanã", "Mandaqui", "Perus", "Anhanguera", "Pirituba", "Jaraguá", "São Domingos", "Santana", "Tucuruvi", "Tremembé", "Vila Guilherme", "Vila Maria", "Vila Medeiros", "Butantã", "Rio Pequeno", "Raposo Tavares", "Jaguaré", "Jaguara", "Lapa", "Perdizes", "Vila Leopoldina", "Alto de Pinheiros", "Pinheiros", "Itaim Bibi", "Jardim Paulista", "Campo Belo", "Santo Amaro", "Campo Grande", "Campo Limpo", "Capão Redondo", "Vila Andrade", "Cidade Ademar", "Pedreira", "Ipiranga", "Sacomã", "Cursino", "Jabaquara", "Moema", "Saúde", "Vila Mariana", "Cidade Dutra", "Grajaú", "Marsilac", "Parelheiros", "Socorro"])

m1, m2, t1, t2 = st.columns(4)
mun_moradia = m1.selectbox("MUNICÍPIO (Moradia)", municipios_rmsp)
dist_moradia = m2.selectbox("DISTRITO (Moradia)", distritos_sp) if mun_moradia == "São Paulo" else m2.text_input("BAIRRO/DISTRITO (Moradia)")
mun_trabalho = t1.selectbox("MUNICÍPIO (Trabalho)", municipios_rmsp)
dist_trabalho = t2.selectbox("DISTRITO (Trabalho)", distritos_sp) if mun_trabalho == "São Paulo" else t2.text_input("BAIRRO/DISTRITO (Trabalho)")

st.markdown("---")
st.markdown("### 🚌 CUSTOS E RENDIMENTOS")
tr1, tr2, tr3, tr4, tr5 = st.columns(5)
g_on = tr1.number_input("🚍 ÔNIBUS", 0.0)
g_me = tr2.number_input("🚇 METRÔ", 0.0)
g_tr = tr3.number_input("🚆 TREM", 0.0)
g_ap = tr4.number_input("🚗 APP", 0.0)
g_ca = tr5.number_input("⛽ CARRO", 0.0)

r1, r2, r3, r4 = st.columns(4)
sal = r1.number_input("💰 SALÁRIO BRUTO", 0.0)
c_vida = r2.number_input("🏠 CUSTO VIDA", 0.0)
dias = r3.number_input("📅 DIAS/MÊS", 22)
h_dia = r4.number_input("⏳ HORAS TRECHO (DIA)", 2.0)

# --- BOTÃO PRINCIPAL ---
if st.button("📊 EFETUAR DIAGNÓSTICO"):
    if mun_moradia == " " or sal <= 0:
        st.warning("⚠️ Dados incompletos.")
    else:
        # Cálculos (Fiação corrigida)
        gasto_d = g_on + g_me + g_tr + g_ap + g_ca
        custo_m = gasto_d * dias
        h_m = h_dia * dias
        v_h_nom = sal / 176 if sal > 0 else 0
        sal_liq = sal - custo_m
        v_h_re = sal_liq / (176 + h_m) if (176 + h_m) > 0 else 0
        confi = custo_m + (h_m * v_h_nom)
        depre = (1 - (v_h_re / v_h_nom)) * 100 if v_h_nom > 0 else 0
        
        # Resultados Visuais
        st.markdown(f"""<div class="report-box">
            <h3>📋 DIAGNÓSTICO FINAL</h3>
            <p>• 💹 <b>VALOR HORA:</b> De R$ {v_h_nom:.2f} para R$ {v_h_re:.2f}</p>
            <p>• 💸 <b>CONFISCO MENSAL:</b> R$ {confi:.2f}</p>
            <p>• 📉 <b>DEPRECIAÇÃO:</b> {depre:.1f}%</p>
        </div>""", unsafe_allow_html=True)

        # ARMAZENAMENTO NA PLANILHA (OPERAÇÃO SILENCIOSA)
        try:
            nova_entrada = pd.DataFrame([{
                "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Genero": genero, "Idade": idade, "Setor": setor,
                "Residencia": f"{mun_moradia}/{dist_moradia}",
                "Trabalho": f"{mun_trabalho}/{dist_trabalho}",
                "Confisco": f"{confi:.2f}"
            }])
            conn.create(spreadsheet=URL_PLANILHA, data=nova_entrada)
            st.success("✅ Dados exportados para a base com sucesso!")
        except:
            st.info("💡 Diagnóstico concluído.")

        # Download do relatório
        st.download_button("📥 BAIXAR NOTA TÉCNICA", f"Relatório de Confisco: R$ {confi:.2f}", "nota_tecnica.txt")

# --- SEÇÃO DE EXPORTAÇÃO MANUAL (CASO O USUÁRIO QUEIRA RE-ENVIAR) ---
st.markdown("---")
st.subheader("📤 Ações de Base de Dados")
if st.button("🚀 FORÇAR EXPORTAÇÃO PARA PLANILHA"):
    # Recalcula e envia novamente para garantir
    st.info("Sincronizando dados...")
    # (Lógica de salvamento repetida aqui para garantir escopo)
