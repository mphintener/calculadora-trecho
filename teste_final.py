import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# 1. CONEXÃO E CONFIGURAÇÃO
st.set_page_config(page_title="Calculadora do Trecho", layout="wide")
conn = st.connection("gsheets", type=GSheetsConnection)
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1VBatkCYcuBFLcLkiTAiD99EREaHbJfKpeXrc-MPx0xQ/edit#gid=0"

# --- ESTILIZAÇÃO CSS (SEU DESIGN ORIGINAL) ---
st.markdown("""
    <style>
    header, [data-testid="stHeader"], [data-testid="stStatusWidget"] { visibility: hidden; display: none; height: 0px; }
    .stApp { background-color: #000000 !important; }
    .block-container { padding-top: 1rem !important; margin-top: -40px !important; }
    label, p, span { color: #FFCC00 !important; font-weight: bold !important; }
    .stSelectbox div[data-baseweb="select"] { background-color: #FFFFFF !important; color: #000000 !important; }
    .stTextInput input, .stNumberInput input {
        background-color: #000000 !important; color: #FFFFFF !important;
        border: none !important; border-bottom: 2px solid #FFCC00 !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }
    .report-box { background-color: #FFFFFF !important; padding: 25px; border: 5px solid #FFCC00; border-radius: 10px; color: #000000 !important; }
    .report-box p, .report-box b, .report-box h3, .report-box span { color: #000000 !important; }
    .stButton>button { 
        background-color: #FFCC00 !important; color: #000000 !important; 
        font-weight: 900 !important; width: 100%; height: 3.5em; text-transform: uppercase;
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

# 3. BANCO DE DADOS GEOGRÁFICO
municipios_rmsp = [" "] + sorted(["Arujá", "Barueri", "Biritiba-Mirim", "Caieiras", "Cajamar", "Carapicuíba", "Cotia", "Diadema", "Embu das Artes", "Embu-Guaçu", "Ferraz de Vasconcelos", "Francisco Morato", "Franco da Rocha", "Guararema", "Guarulhos", "Itapecerica da Serra", "Itapevi", "Itaquaquecetuba", "Jandira", "Juquitiba", "Mairiporã", "Mauá", "Mogi das Cruzes", "Osasco", "Pirapora do Bom Jesus", "Poá", "Ribeirão Pires", "Rio Grande da Serra", "Salesópolis", "Santa Isabel", "Santana de Parnaíba", "Santo André", "São Bernardo do Campo", "São Caetano do Sul", "São Lourenço da Serra", "São Paulo", "Suzano", "Taboão da Serra", "Vargem Grande Paulista"])
distritos_sp = [" "] + sorted(["Água Rasa", "Alto de Pinheiros", "Anhanguera", "Aricanduva", "Artur Alvim", "Barra Funda", "Bela Vista", "Belém", "Bom Retiro", "Brasilândia", "Butantã", "Cachoeirinha", "Cambuci", "Campo Belo", "Campo Grande", "Campo Limpo", "Cangaíba", "Capão Redondo", "Carrão", "Casa Verde", "Cidade Ademar", "Cidade Dutra", "Cidade Líder", "Cidade Tiradentes", "Consolação", "Cursino", "Ermelino Matarazzo", "Freguesia do Ó", "Grajaú", "Guaianases", "Iguatemi", "Ipiranga", "Itaim Bibi", "Itaim Paulista", "Itaquera", "Jabaquara", "Jaçanã", "Jaguara", "Jaguaré", "Jaraguá", "Jardim Ângela", "Jardim Helena", "Jardim Paulista", "Jardim São Luís", "Lapa", "Liberdade", "Limão", "Mandaqui", "Marsilac", "Moema", "Mooca", "Morumbi", "Parelheiros", "Pari", "Parque do Carmo", "Pedreira", "Penha", "Perdizes", "Perus", "Pinheiros", "Pirituba", "Ponte Rasa", "Raposo Tavares", "República", "Rio Pequeno", "Sacomã", "Santa Cecília", "Santana", "Santo Amaro", "São Domingos", "São Lucas", "São Mateus", "São Miguel", "São Rafael", "Sapopemba", "Saúde", "Sé", "Socorro", "Tatuapé", "Tremembé", "Tucuruvi", "Vila Andrade", "Vila Curuçá", "Vila Formosa", "Vila Guilherme", "Vila Jacuí", "Vila Leopoldina", "Vila Maria", "Vila Mariana", "Vila Matilde", "Vila Medeiros", "Vila Prudente", "Vila Sônia"])

# 4. ENTRADA DE DADOS: PERFIL DO USUÁRIO
st.markdown("### 👤 PERFIL DO USUÁRIO")
p1, p2, p3, p4, p5 = st.columns(5)
idade = p1.number_input("IDADE", min_value=14, step=1, value=25)
genero = p2.selectbox("GÊNERO", ["Feminino","Masculino", "Não-binário", "Outro", "Prefiro não responder"])
cor_raca = p3.selectbox("COR/RAÇA", ["Branca", "Preta", "Parda", "Amarela", "Indígena"])
escolaridade = p4.selectbox("ESCOLARIDADE", ["Fundamental Incompleto", "Fundamental Completo", "Médio Incompleto", "Médio Completo", "Técnico", "Superior Incompleto", "Superior Completo", "Pós-Graduação"])
setor = p5.selectbox("SETOR DE ATIVIDADE", ["Comércio", "Construção Civil", "Educação", "Indústria", "Serviços", "Saúde", "Outros"])

st.markdown("---")
st.markdown("### 🏠 LOCALIZAÇÃO")
m1, m2, t1, t2 = st.columns(4)
mun_moradia = m1.selectbox("MUNICÍPIO (Moradia)", municipios_rmsp)
dist_moradia = m2.selectbox("DISTRITO (Moradia)", distritos_sp) if mun_moradia == "São Paulo" else m2.text_input("BAIRRO/DISTRITO (Moradia)")
mun_trabalho = t1.selectbox("MUNICÍPIO (Trabalho)", municipios_rmsp)
dist_trabalho = t2.selectbox("DISTRITO (Trabalho)", distritos_sp) if mun_trabalho == "São Paulo" else t2.text_input("BAIRRO/DISTRITO (Trabalho)")

st.markdown("---")
st.markdown("### 🚌 CUSTOS DIÁRIOS E RENDIMENTOS")
tr1, tr2, tr3, tr4, tr5 = st.columns(5)
g_on = tr1.number_input("🚍 ÔNIBUS", 0.0)
g_me = tr2.number_input("🚇 METRÔ", 0.0)
g_tr = tr3.number_input("🚆 TREM", 0.0)
g_ap = tr4.number_input("🚗 APP", 0.0)
g_ca = tr5.number_input("⛽ CARRO", 0.0)

r1, r2, r3, r4 = st.columns(4)
sal = r1.number_input("💰 SALÁRIO BRUTO (R$)", 0.0)
c_vida = r2.number_input("🏠 CUSTO DE VIDA (R$)", 0.0)
dias = r3.number_input("📅 DIAS TRABALHADOS/MÊS", value=22)
h_dia = r4.number_input("⏳ HORAS NO TRECHO (Ida/Volta)", value=2.0, step=0.5)

st.markdown("---")

# 5. BOTÃO E LÓGICA DE DIAGNÓSTICO
if st.button("📊 EFETUAR DIAGNÓSTICO"):
    if mun_moradia == " " or sal <= 0:
        st.warning("⚠️ Preencha o município de moradia e o salário para gerar o diagnóstico.")
    else:
        # CÁLCULOS
        gasto_d = g_on + g_me + g_tr + g_ap + g_ca
        custo_m = gasto_d * dias
        v_h_nom = sal / 176 if sal > 0 else 0
        h_m = h_dia * dias
        sal_liq_transp = sal - custo_m
        sobra = sal_liq_transp - c_vida
        v_h_re = sal_liq_transp / (176 + h_m) if (176 + h_m) > 0 else 0
        confi = custo_m + (h_m * v_h_nom)
        depre = (1 - (v_h_re / v_h_nom)) * 100 if v_h_nom > 0 else 0

        # FLUXO VISUAL
        label_m = (dist_moradia or mun_moradia).upper()
        label_t = (dist_trabalho or mun_trabalho).upper()
        st.markdown(f"""<div style="background:#000; padding:20px; border:2px solid #E63946; text-align:center; margin-bottom:20px;">
            <div style="color:#FFCC00; font-weight:bold; font-size:1.4rem;">🏠 {label_m} ———▶ 💼 {label_t}</div>
        </div>""", unsafe_allow_html=True)

        # CAIXA DE RESULTADOS
        cor_alerta = "#E63946" if depre > 20 else "#000000"
        st.markdown(f"""<div class="report-box">
            <h3 style="margin-top:0;">📋 RESULTADOS</h3>
            <p>• 💹 <b>VALOR DA HORA TRABALHADA:</b> De R$ {v_h_nom:.2f} para <span style="color:#E63946;">R$ {v_h_re:.2f}</span></p>
            <p>• ⏳ <b>TEMPO DE TRABALHO NÃO PAGO:</b> {h_m:.1f}h/mês</p>
            <p>• 💸 <b>VALOR DO CONFISCO (TARIFA + TEMPO):</b> R$ {confi:.2f}</p>
            <p>• 💵 <b>SALÁRIO LÍQUIDO (-TRANSPORTE):</b> R$ {sal_liq_transp:.2f}</p>
            <p>• 📉 <b>SOBRA RESIDUAL:</b> R$ {sobra:.2f}</p>
            <p>• 📉 <b>DEPRECIAÇÃO REAL:</b> <span style="color:{cor_alerta}; font-weight:900; font-size:1.4rem;">{depre:.1f}%</span></p>
        </div>""", unsafe_allow_html=True)

        # NOTA TÉCNICA DETALHADA
        st.markdown(f"""
            <div style='background-color: #FFFFFF; padding: 25px; border-left: 12px solid #FFCC00; border: 1px solid #E0E0E0; border-radius: 8px; margin-top: 25px;'>
                <h2 style='color: #000000; font-size: 1.3rem; margin-top: 0;'>📝 NOTA TÉCNICA</h2>
                <div style='color: #333333; font-size: 1.1rem; line-height: 1.6; text-align: justify;'>
                    O <b>"Confisco"</b> calculado reflete o valor total subtraído do rendimento real. 
                    O trecho é <b>trabalho não pago</b>: tempo obrigatório para a reprodução da força de trabalho 
                    que gera uma depreciação de <span style='color: #E63946; font-weight: bold;'>{depre:.1f}%</span> no valor da sua hora.
                </div>
            </div>
        """, unsafe_allow_html=True)

        # SALVAMENTO AUTOMÁTICO (CORRIGIDO)
        try:
            nova_entrada = pd.DataFrame([{
                "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Genero": genero, "Idade": idade, "Cor_Raca": cor_raca, 
                "Escolaridade": escolaridade, "Setor": setor,
                "Residencia": f"{mun_moradia} ({dist_moradia})",
                "Trabalho": f"{mun_trabalho} ({dist_trabalho})",
                "Transporte_Total": f"{gasto_d:.2f}",
                "Salario_Bruto": f"{sal:.2f}",
                "Confisco_Total": f"{confi:.2f}"
            }])
            conn.create(spreadsheet=URL_PLANILHA, data=nova_entrada)
            st.toast("✅ Sincronizado com a base de dados!")
        except:
            pass

        # BOTÃO DE DOWNLOAD
        relatorio_txt = f"DIAGNÓSTICO TÉCNICO\nCONFISCO: R$ {confi:.2f}\nDEPRECIAÇÃO: {depre:.1f}%"
        st.download_button("📥 BAIXAR NOTA TÉCNICA (TXT)", relatorio_txt, file_name="diagnostico.txt")
