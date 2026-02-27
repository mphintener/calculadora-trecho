import streamlit as st 
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# 1. SETUP E CONEXÃO
st.set_page_config(page_title="Calculadora do Trecho", layout="wide")
conn = st.connection("gsheets", type=GSheetsConnection)
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1VBatkCYcuBFLcLkiTAiD99EREaHbJfKpeXrc-MPx0xQ/edit#gid=0"

# --- ESTILIZAÇÃO CSS ---
st.markdown("""
    <style>
    header, [data-testid="stHeader"], [data-testid="stStatusWidget"] { visibility: hidden; display: none; height: 0px; }
    .stApp { background-color: #000000 !important; }
    .block-container { padding-top: 1rem !important; margin-top: -40px !important; }
    
    input { caret-color: #FFCC00 !important; }
    .stNumberInput input:focus, .stTextInput input:focus, .stSelectbox div[data-baseweb="select"]:focus-within {
        border-bottom: 3px solid #FFFFFF !important;
        box-shadow: 0px 0px 15px rgba(255, 204, 0, 0.8) !important;
        transition: 0.3s ease-in-out;
    }
    label, p, span { color: #FFCC00 !important; font-weight: bold !important; }
    .stSelectbox div[data-baseweb="select"] { background-color: #FFFFFF !important; color: #000000 !important; }
    .stTextInput input, .stNumberInput input {
        background-color: #000000 !important; color: #FFFFFF !important;
        border: none !important; border-bottom: 2px solid #FFCC00 !important;
    }
    .stButton>button { 
        background-color: #FFCC00 !important; border: 3px solid #000000 !important;
        border-radius: 5px !important; height: 4em; width: 100%;
    }
    .stButton>button * { color: #000000 !important; font-weight: 900 !important; text-transform: uppercase; }
    .report-box { background-color: #FFFFFF !important; padding: 30px; border: 6px solid #FFCC00; border-radius: 12px; color: #000000 !important; }
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
    except: st.markdown("<div style='height:80px;'></div>", unsafe_allow_html=True)

# 3. DADOS GEOGRÁFICOS
municipios_rmsp = [" "] + sorted(["Arujá", "Barueri", "Biritiba-Mirim", "Caieiras", "Cajamar", "Carapicuíba", "Cotia", "Diadema", "Embu das Artes", "Embu-Guaçu", "Ferraz de Vasconcelos", "Francisco Morato", "Franco da Rocha", "Guararema", "Guarulhos", "Itapecerica da Serra", "Itapevi", "Itaquaquecetuba", "Jandira", "Juquitiba", "Mairiporã", "Mauá", "Mogi das Cruzes", "Osasco", "Pirapora do Bom Jesus", "Poá", "Ribeirão Pires", "Rio Grande da Serra", "Salesópolis", "Santa Isabel", "Santana de Parnaíba", "Santo André", "São Bernardo do Campo", "São Caetano do Sul", "São Lourenço da Serra", "São Paulo", "Suzano", "Taboão da Serra", "Vargem Grande Paulista"])
distritos_sp = [" "] + sorted(["Água Rasa", "Alto de Pinheiros", "Anhanguera", "Aricanduva", "Artur Alvim", "Barra Funda", "Bela Vista", "Belém", "Bom Retiro", "Brasilândia", "Butantã", "Cachoeirinha", "Cambuci", "Campo Belo", "Campo Grande", "Campo Limpo", "Cangaíba", "Capão Redondo", "Carrão", "Casa Verde", "Cidade Ademar", "Cidade Dutra", "Cidade Líder", "Cidade Tiradentes", "Consolação", "Cursino", "Ermelino Matarazzo", "Freguesia do Ó", "Grajaú", "Guaianases", "Iguatemi", "Ipiranga", "Itaim Bibi", "Itaim Paulista", "Itaquera", "Jabaquara", "Jaçanã", "Jaguara", "Jaguaré", "Jaraguá", "Jardim Ângela", "Jardim Helena", "Jardim Paulista", "Jardim São Luís", "Lapa", "Liberdade", "Limão", "Mandaqui", "Marsilac", "Moema", "Mooca", "Morumbi", "Parelheiros", "Pari", "Parque do Carmo", "Pedreira", "Penha", "Perdizes", "Perus", "Pinheiros", "Pirituba", "Ponte Rasa", "Raposo Tavares", "República", "Rio Pequeno", "Sacomã", "Santa Cecília", "Santana", "Santo Amaro", "São Domingos", "São Lucas", "São Mateus", "São Miguel", "São Rafael", "Sapopemba", "Saúde", "Sé", "Socorro", "Tatuapé", "Tremembé", "Tucuruvi", "Vila Andrade", "Vila Curuçá", "Vila Formosa", "Vila Guilherme", "Vila Jacuí", "Vila Leopoldina", "Vila Maria", "Vila Mariana", "Vila Matilde", "Vila Medeiros", "Vila Prudente", "Vila Sônia"])

# 4. ENTRADA DE DADOS
st.markdown("### 👤 PERFIL DO USUÁRIO")
p1, p2, p3, p4, p5 = st.columns(5)
idade = p1.number_input("IDADE", min_value=14, step=1, value=None)
genero = p2.selectbox("Gênero", ["Feminino","Masculino", "Não-binário", "Outro", "Prefiro não responder"])
cor_raça = p3.selectbox("Cor_Raça", ["Branca", "Preta", "Parda", "Amarela", "Indígena"])
escolaridade = p4.selectbox("ESCOLARIDADE", ["Fundamental Incompleto", "Fundamental Completo", "Médio Incompleto", "Médio Completo", "Técnico", "Superior Incompleto", "Superior Completo", "Pós-Graduação"])
setor = p5.selectbox("SETOR DE ATIVIDADE", ["Comércio", "Construção Civil", "Educação", "Indústria", "Serviços", "Saúde", "Outros"])

st.markdown("---")
st.markdown("### 🏠 LOCALIZAÇÃO")
m1, m2 = st.columns(2)
mun_moradia = m1.selectbox("MUNICÍPIO (Moradia)", municipios_rmsp, index=0)
dist_moradia = m2.selectbox("DISTRITO (Moradia)", distritos_sp, index=0) if mun_moradia == "São Paulo" else m2.text_input("BAIRRO/DISTRITO (Moradia)", placeholder="Digite seu bairro")

t1, t2, t3 = st.columns(3)
mun_trabalho = t1.selectbox("MUNICÍPIO (Trabalho)", municipios_rmsp, index=0)
dist_trabalho = t2.selectbox("DISTRITO (Trabalho)", distritos_sp, index=0) if mun_trabalho == "São Paulo" else t2.text_input("BAIRRO/DISTRITO (Trabalho)", placeholder="Digite o bairro de trabalho")
h_dia = t3.number_input("⏳ HORAS NO TRECHO (Ida/Volta)", value=2.0, step=0.5)

st.markdown("---")
st.markdown("### 🚌 CUSTOS E RENDIMENTOS")
tr1, tr2, tr3, tr4, tr5 = st.columns(5)
g_on = tr1.number_input("🚍 ÔNIBUS", min_value=0.0)
g_me = tr2.number_input("🚇 METRÔ", min_value=0.0)
g_tr = tr3.number_input("🚆 TREM", min_value=0.0)
g_ap = tr4.number_input("🚗 APP", min_value=0.0)
g_ca = tr5.number_input("⛽ CARRO", min_value=0.0)

r1, r2, r3 = st.columns(3)
sal = r1.number_input("💰 SALÁRIO BRUTO (R$)", min_value=0.0)
c_vida = r2.number_input("🏠 CUSTO DE VIDA (R$)", min_value=0.0)
dias = r3.number_input("📅 DIAS TRABALHADOS/MÊS", value=22)

# 5. LÓGICA E RESULTADOS
if st.button("📊 EFETUAR DIAGNÓSTICO"):
    if salario > 0:
        # Cálculos
        custo_m = gasto_transp * dias_mes
        h_m = h_dia * dias_mes
        v_h_nom = salario / 176
        sal_liq = salario - custo_m
        v_h_re = sal_liq / (176 + h_m)
        confi = custo_m + (h_m * v_h_nom)
        depre = (1 - (v_h_re / v_h_nom)) * 100

        # ALERTA VERMELHO
        st.markdown("""<div style="background-color: #E63946; color: white; padding: 15px; text-align: center; font-weight: bold; border-radius: 5px; margin: 10px 0;">🚨 ALERTA DE EXPROPRIAÇÃO MENSAL</div>""", unsafe_allow_html=True)

        # RESULTADOS + NOTA TÉCNICA (HTML PURO PARA NÃO DAR ERRO)
        st.markdown(f"""
        <div class="report-box">
            <h3 style="margin-top:0;">📋 RESULTADOS</h3>
            <p>• 💹 <b>VALOR DA HORA TRABALHADA:</b> De R$ {v_h_nom:.2f} para <span style="color:#E63946;">R$ {v_h_re:.2f}</span></p>
            <p>• ⏳ <b>TEMPO DE TRABALHO NÃO PAGO:</b> {h_m:.1f}h/mês</p>
            <p>• 💸 <b>VALOR DO CONFISCO (TARIFA + TEMPO):</b> R$ {confi:.2f}</p>
            <p>• 💵 <b>SALÁRIO LÍQUIDO (-TRANSPORTE):</b> R$ {sal_liq:.2f}</p>
            <p>• 📉 <b>SOBRA RESIDUAL (PÓS-TRANSPORTE):</b> R$ {sal_liq:.2f}</p>
            <p>• 📉 <b>DEPRECIAÇÃO REAL DO VALOR/HORA:</b> <span style="color:#E63946; font-weight:900;">{depre:.1f}%</span></p>
            <p style="font-size:0.85rem; color:#666; font-style:italic;">*Isso significa que sua força de trabalho vale {depre:.1f}% menos devido ao deslocamento.</p>
            
            <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">
            
            <h4 style="color:#000;">📝 NOTA TÉCNICA</h4>
            <div style="color: #333; font-family: serif; font-size: 1rem; text-align: justify; line-height: 1.5;">
                O <b>"Confisco"</b> calculado neste diagnóstico reflete o valor total subtraído do rendimento real do trabalhador. 
                Ele não considera apenas a tarifa, mas o <b>valor monetário do tempo de vida</b> convertido em deslocamento. 
                Na perspectiva da economia política, o trecho é <b>"trabalho não pago"</b>: um tempo obrigatório para a 
                reprodução da força de trabalho que não é remunerado, gerando uma depreciação real de 
                <span style="color: #E63946; font-weight: bold;">{depre:.1f}%</span> no valor da sua hora contratada.
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 3. EXPORTAÇÃO AUTOMÁTICA (SILENCIOSA)
        try:
            nova_entrada = pd.DataFrame([{
                "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Genero": genero, "Idade": idade, "Raca": cor_raça, 
                "Escolaridade": escolaridade, "Setor": setor,
                "Moradia": mun_moradia, "Trabalho": mun_trabalho, 
                "Salario": f"{sal:.2f}", "Confisco": f"{confi:.2f}"
            }])
            conn.create(spreadsheet=URL_PLANILHA, data=nova_entrada)
            st.toast("✅ Sincronizado com a base de dados!")
        except:
            pass

# --- 6. EXPORTAÇÃO MANUAL (FINAL DO ARQUIVO) ---
st.markdown("---")
st.subheader("📤 Enviar para Base de Dados")
st.write("Clique abaixo para salvar este diagnóstico na base de dados manualmente.")

if st.button("🚀 Salvar Dados na Planilha"):
    try:
        # Recalcula o confisco para garantir que a variável exista neste contexto
        gasto_total = g_on + g_me + g_tr + g_ap + g_ca
        conf_manual = (gasto_total * dias) + ((h_dia * dias) * (sal/176 if sal>0 else 0))
        
        man_entrada = pd.DataFrame([{
            "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Genero": genero, "Idade": idade, "Setor": setor,
            "Residencia": mun_moradia, "Trabalho": mun_trabalho,
            "Salario": f"{sal:.2f}", "Confisco": f"{conf_manual:.2f}"
        }])
        conn.create(spreadsheet=URL_PLANILHA, data=man_entrada)
        st.success("✅ Dados salvos com sucesso!")
        st.balloons()
    except Exception as e:
        st.error(f"Erro ao salvar: {e}")
