import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# 1. SETUP E CONEXÃO
st.set_page_config(page_title="Calculadora do Trecho", layout="wide", page_icon="⚖️")
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1VBatkCYcuBFLcLkiTAiD99EREaHbJfKpeXrc-MPx0xQ/edit#gid=0"

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except:
    pass

# 2. ESTILO CSS
st.markdown("""
    <style>
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }
    .stApp { background-color: #000000 !important; }
    .block-container { padding-top: 1rem !important; margin-top: -30px !important; }
    label, p, span { color: #FFCC00 !important; font-weight: bold !important; }
    .stSelectbox div[data-baseweb="select"] { background-color: #FFFFFF !important; color: #000000 !important; }
    .stNumberInput input, .stTextInput input {
        background-color: #000000 !important; color: #FFFFFF !important;
        border: none !important; border-bottom: 2px solid #FFCC00 !important;
    }
    .stButton>button { 
        background-color: #FFCC00 !important; color: #000000 !important; 
        font-weight: 900 !important; width: 100%; height: 3.5em; border-radius: 8px;
    }
    .report-box { 
        background-color: #FFFFFF !important; padding: 25px; 
        border: 5px solid #FFCC00; border-radius: 10px; color: #000000 !important; 
    }
    .report-box * { color: #000000 !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. BANCOS GEOGRÁFICOS
municipios_rmsp = [" "] + sorted(["Arujá", "Barueri", "Biritiba-Mirim", "Caieiras", "Cajamar", "Carapicuíba", "Cotia", "Diadema", "Embu das Artes", "Embu-Guaçu", "Ferraz de Vasconcelos", "Francisco Morato", "Franco da Rocha", "Guararema", "Guarulhos", "Itapecerica da Serra", "Itapevi", "Itaquaquecetuba", "Jandira", "Juquitiba", "Mairiporã", "Mauá", "Mogi das Cruzes", "Osasco", "Pirapora do Bom Jesus", "Poá", "Ribeirão Pires", "Rio Grande da Serra", "Salesópolis", "Santa Isabel", "Santana de Parnaíba", "Santo André", "São Bernardo do Campo", "São Caetano do Sul", "São Lourenço da Serra", "São Paulo", "Suzano", "Taboão da Serra", "Vargem Grande Paulista"])
distritos_sp = [" "] + sorted(["Água Rasa", "Alto de Pinheiros", "Anhanguera", "Aricanduva", "Artur Alvim", "Barra Funda", "Bela Vista", "Belém", "Bom Retiro", "Brasilândia", "Butantã", "Cachoeirinha", "Cambuci", "Campo Belo", "Campo Grande", "Campo Limpo", "Cangaíba", "Capão Redondo", "Carrão", "Casa Verde", "Cidade Ademar", "Cidade Dutra", "Cidade Líder", "Cidade Tiradentes", "Consolação", "Cursino", "Ermelino Matarazzo", "Freguesia do Ó", "Grajaú", "Guaianases", "Iguatemi", "Ipiranga", "Itaim Bibi", "Itaim Paulista", "Itaquera", "Jabaquara", "Jaçanã", "Jaguara", "Jaguaré", "Jaraguá", "Jardim Ângela", "Jardim Helena", "Jardim Paulista", "Jardim São Luís", "Lapa", "Liberdade", "Limão", "Mandaqui", "Marsilac", "Moema", "Mooca", "Morumbi", "Parelheiros", "Pari", "Parque do Carmo", "Pedreira", "Penha", "Perdizes", "Perus", "Pinheiros", "Pirituba", "Ponte Rasa", "Raposo Tavares", "República", "Rio Pequeno", "Sacomã", "Santa Cecília", "Santana", "Santo Amaro", "São Domingos", "São Lucas", "São Mateus", "São Miguel", "São Rafael", "Sapopemba", "Saúde", "Sé", "Socorro", "Tatuapé", "Tremembé", "Tucuruvi", "Vila Andrade", "Vila Curuçá", "Vila Formosa", "Vila Guilherme", "Vila Jacuí", "Vila Leopoldina", "Vila Maria", "Vila Mariana", "Vila Matilde", "Vila Medeiros", "Vila Prudente", "Vila Sônia"])

# 4. CABEÇALHO
st.markdown("<h1 style='color:#FFCC00;'>⚖️ CALCULADORA DO TRECHO</h1>", unsafe_allow_html=True)

# 5. INPUTS: PERFIL (ORDEM E CATEGORIAS RESTAURADAS)
st.markdown("### 👤 PERFIL DO USUÁRIO")
p1, p2, p3, p4, p5 = st.columns(5)
idade = p1.number_input("IDADE", min_value=0, step=1, value=None, placeholder="0")
genero = p2.selectbox("Gênero", ["Feminino", "Masculino", "Não-binário", "Outro", "Prefiro não responder"])
cor_raça = p3.selectbox("Cor_Raça", ["Branca", "Preta", "Parda", "Amarela", "Indígena"])
escolaridade = p4.selectbox("ESCOLARIDADE", [
    "Fundamental Incompleto", "Fundamental Completo", 
    "Médio Incompleto", "Médio Completo", "Técnico", 
    "Superior Incompleto", "Superior Completo", "Pós-Graduação"
])
setor = p5.selectbox("SETOR DE ATIVIDADE", [
    "Comércio", "Construção Civil", "Educação", 
    "Indústria", "Serviços", "Saúde", "Outros"
])

# 6. INPUTS: LOCALIZAÇÃO
st.markdown("---")
st.markdown("### 🏠 LOCALIZAÇÃO")
m1, m2, t1, t2 = st.columns(4)
mun_moradia = m1.selectbox("MUNICÍPIO (Moradia)", municipios_rmsp)
dist_moradia = m2.selectbox("DISTRITO (Moradia)", distritos_sp) if mun_moradia == "São Paulo" else m2.text_input("BAIRRO (Moradia)")
mun_trabalho = t1.selectbox("MUNICÍPIO (Trabalho)", municipios_rmsp)
dist_trabalho = t2.selectbox("DISTRITO (Trabalho)", distritos_sp) if mun_trabalho == "São Paulo" else t2.text_input("BAIRRO (Trabalho)")

# 7. INPUTS: MODAIS E RENDIMENTOS
st.markdown("---")
st.markdown("### 🚌 CUSTOS E TEMPO")
c1, c2, c3, c4, c5 = st.columns(5)
g_on = c1.number_input("🚍 ÔNIBUS", min_value=0.0)
g_me = c2.number_input("🚇 METRÔ", min_value=0.0)
g_tr = c3.number_input("🚆 TREM", min_value=0.0)
g_ap = c4.number_input("🚕 APP", min_value=0.0)
g_ca = c5.number_input("🚗 CARRO", min_value=0.0)

r1, r2, r3 = st.columns(3)
salario = r1.number_input("💰 SALÁRIO BRUTO", min_value=0.0)
h_dia = r2.number_input("⏳ HORAS TRECHO/DIA", min_value=0.0)
dias = r3.number_input("📅 DIAS TRABALHADOS/MÊS", value=22)

# 8. LÓGICA E RESULTADOS
if st.button("📊 EFETUAR DIAGNÓSTICO"):
    if salario > 0 and mun_moradia != " ":
        custo_m = (g_on + g_me + g_tr + g_ap + g_ca) * dias
        h_m = h_dia * dias
        v_h_nom = salario / 176
        sal_liq = salario - custo_m
        v_h_re = sal_liq / (176 + h_m)
        confi = custo_m + (h_m * v_h_nom)
        depre = (1 - (v_h_re / v_h_nom)) * 100

        st.markdown("""<div style="background-color: #E63946; color: white; padding: 15px; text-align: center; font-weight: bold; border-radius: 5px; margin-bottom: 10px;">🚨 ALERTA DE EXPROPRIAÇÃO MENSAL</div>""", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="report-box">
            <h3 style="margin-top:0;">📋 RESULTADOS</h3>
            <p>• 💹 <b>VALOR DA HORA:</b> De R$ {v_h_nom:.2f} para <span style="color:#E63946;">R$ {v_h_re:.2f}</span></p>
            <p>• ⏳ <b>TEMPO NÃO PAGO:</b> {h_m:.1f}h/mês</p>
            <p>• 💸 <b>CONFISCO MENSAL:</b> R$ {confi:.2f}</p>
            <p>• 📉 <b>DEPRECIAÇÃO REAL:</b> <span style="color:#E63946; font-weight:900; font-size:1.3rem;">{depre:.1f}%</span></p>
            <hr>
            <h4>📝 NOTA TÉCNICA</h4>
            <div style="color: #333; font-family: serif; font-size: 1rem; text-align: justify; line-height: 1.5;">
                O <b>"Confisco"</b> calculado neste diagnóstico reflete o valor total subtraído do rendimento real do trabalhador. 
                Considera o trecho como <b>"trabalho não pago"</b>, gerando uma depreciação real de 
                <b>{depre:.1f}%</b> no valor da sua hora contratada.
            </div>
        </div>
        """, unsafe_allow_html=True)

        try:
            nova = pd.DataFrame([{
                "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Genero": genero, "Idade": idade, "Cor": cor_raça, 
                "Escolaridade": escolaridade, "Setor": setor,
                "Confisco": f"{confi:.2f}"
            }])
            conn.create(spreadsheet=URL_PLANILHA, data=nova)
            st.toast("✅ Sincronizado!")
        except:
            pass

