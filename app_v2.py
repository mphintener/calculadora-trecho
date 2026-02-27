import streamlit as st
import pandas as pd
from datetime import datetime

# 1. CONFIGURAÇÃO E ESTILO
st.set_page_config(page_title="Calculadora do Trecho", layout="wide", page_icon="⚖️")

st.markdown("""
    <style>
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }
    .stApp { background-color: #000000 !important; }
    .block-container { padding-top: 1rem !important; }
    label, p, span { color: #FFCC00 !important; font-weight: bold !important; }
    .stNumberInput input, .stTextInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: #000000 !important; color: #FFFFFF !important;
        border: none !important; border-bottom: 2px solid #FFCC00 !important;
    }
    .stSelectbox div[data-baseweb="select"] { background-color: #FFFFFF !important; color: #000000 !important; }
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

# 2. BANCO DE DADOS GEOGRÁFICO
municipios_rmsp = [" "] + sorted(["Arujá", "Barueri", "Biritiba-Mirim", "Caieiras", "Cajamar", "Carapicuíba", "Cotia", "Diadema", "Embu das Artes", "Embu-Guaçu", "Ferraz de Vasconcelos", "Francisco Morato", "Franco da Rocha", "Guararema", "Guarulhos", "Itapecerica da Serra", "Itapevi", "Itaquaquecetuba", "Jandira", "Juquitiba", "Mairiporã", "Mauá", "Mogi das Cruzes", "Osasco", "Pirapora do Bom Jesus", "Poá", "Ribeirão Pires", "Rio Grande da Serra", "Salesópolis", "Santa Isabel", "Santana de Parnaíba", "Santo André", "São Bernardo do Campo", "São Caetano do Sul", "São Lourenço da Serra", "São Paulo", "Suzano", "Taboão da Serra", "Vargem Grande Paulista"])
distritos_sp = [" "] + sorted(["Água Rasa", "Alto de Pinheiros", "Anhanguera", "Aricanduva", "Artur Alvim", "Barra Funda", "Bela Vista", "Belém", "Bom Retiro", "Brasilândia", "Butantã", "Cachoeirinha", "Cambuci", "Campo Belo", "Campo Grande", "Campo Limpo", "Cangaíba", "Capão Redondo", "Carrão", "Casa Verde", "Cidade Ademar", "Cidade Dutra", "Cidade Líder", "Cidade Tiradentes", "Consolação", "Cursino", "Ermelino Matarazzo", "Freguesia do Ó", "Grajaú", "Guaianases", "Iguatemi", "Ipiranga", "Itaim Bibi", "Itaim Paulista", "Itaquera", "Jabaquara", "Jaçanã", "Jaguara", "Jaguaré", "Jaraguá", "Jardim Ângela", "Jardim Helena", "Jardim Paulista", "Jardim São Luís", "Lapa", "Liberdade", "Limão", "Mandaqui", "Marsilac", "Moema", "Mooca", "Morumbi", "Parelheiros", "Pari", "Parque do Carmo", "Pedreira", "Penha", "Perdizes", "Perus", "Pinheiros", "Pirituba", "Ponte Rasa", "Raposo Tavares", "República", "Rio Pequeno", "Sacomã", "Santa Cecília", "Santana", "Santo Amaro", "São Domingos", "São Lucas", "São Mateus", "São Miguel", "São Rafael", "Sapopemba", "Saúde", "Sé", "Socorro", "Tatuapé", "Tremembé", "Tucuruvi", "Vila Andrade", "Vila Curuçá", "Vila Formosa", "Vila Guilherme", "Vila Jacuí", "Vila Leopoldina", "Vila Maria", "Vila Mariana", "Vila Matilde", "Vila Medeiros", "Vila Prudente", "Vila Sônia"])

# 3. CABEÇALHO
st.markdown("<h1 style='color:#FFCC00;'>⚖️ CALCULADORA DO TRECHO</h1>", unsafe_allow_html=True)
st.write("Quanto de tempo e de dinheiro são consumidos no seu deslocamento diário?")

# 4. ENTRADA DE DADOS
st.markdown("### 👤 PERFIL")
p1, p2, p3, p4 = st.columns(4)
idade = p1.number_input("IDADE", min_value=0, value=None, placeholder="0")
genero = p2.selectbox("GÊNERO", ["Feminino", "Masculino", "Não-binário", "Outro"])
raca = p3.selectbox("COR/RAÇA", ["Branca", "Preta", "Parda", "Amarela", "Indígena"])
setor = p4.selectbox("SETOR", ["Serviços", "Comércio", "Indústria", "Saúde", "Educação", "Outros"])

st.markdown("---")
st.markdown("### 🏠 LOCALIZAÇÃO")
m1, m2, t1, t2 = st.columns(4)
mun_moradia = m1.selectbox("MUNICÍPIO (Moradia)", municipios_rmsp)
dist_moradia = m2.selectbox("DISTRITO (Moradia)", distritos_sp) if mun_moradia == "São Paulo" else m2.text_input("BAIRRO (Moradia)")
mun_trabalho = t1.selectbox("MUNICÍPIO (Trabalho)", municipios_rmsp)
dist_trabalho = t2.selectbox("DISTRITO (Trabalho)", distritos_sp) if mun_trabalho == "São Paulo" else t2.text_input("BAIRRO (Trabalho)")

st.markdown("---")
st.markdown("### 💰 RENDIMENTOS E CUSTOS")
r1, r2, r3, r4 = st.columns(4)
salario = r1.number_input("💰 SALÁRIO BRUTO", min_value=0.0)
h_dia = r2.number_input("⏳ HORAS TRECHO/DIA", min_value=0.0)
dias_mes = r3.number_input("📅 DIAS/MÊS", value=22)
gasto_transp = r4.number_input("🚍 GASTO TRANSP./DIA", min_value=0.0)

# 5. LÓGICA E DIAGNÓSTICO
if st.button("📊 EFETUAR DIAGNÓSTICO"):
    if salario > 0 and mun_moradia != " ":
        # Cálculos
        custo_m = gasto_transp * dias_mes
        h_m = h_dia * dias_mes
        v_h_nom = salario / 176
        sal_liq = salario - custo_m
        v_h_re = sal_liq / (176 + h_m)
        confi = custo_m + (h_m * v_h_nom)
        depre = (1 - (v_h_re / v_h_nom)) * 100

        # Alerta Vermelho
        st.markdown("""<div style="background-color: #E63946; color: white; padding: 15px; text-align: center; font-weight: bold; border-radius: 5px; margin-bottom: 10px;">🚨 ALERTA DE EXPROPRIAÇÃO MENSAL</div>""", unsafe_allow_html=True)

        # Resultados e Nota Técnica
        st.markdown(f"""
        <div class="report-box">
            <h3 style="margin-top:0;">📋 RESULTADOS</h3>
            <p>• 💹 <b>VALOR DA HORA TRABALHADA:</b> De R$ {v_h_nom:.2f} para <span style="color:#E63946;">R$ {v_h_re:.2f}</span></p>
            <p>• ⏳ <b>TEMPO DE TRABALHO NÃO PAGO:</b> {h_m:.1f}h/mês</p>
            <p>• 💸 <b>VALOR DO CONFISCO (TARIFA + TEMPO):</b> R$ {confi:.2f}</p>
            <p>• 💵 <b>SALÁRIO LÍQUIDO (-TRANSPORTE):</b> R$ {sal_liq:.2f}</p>
            <p>• 📉 <b>DEPRECIAÇÃO REAL DO VALOR/HORA:</b> <span style="color:#E63946; font-weight:900; font-size:1.3rem;">{depre:.1f}%</span></p>
            
            <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">
            
            <h4>📝 NOTA TÉCNICA</h4>
            <div style="color: #333; font-family: serif; font-size: 1rem; text-align: justify; line-height: 1.5;">
                O <b>"Confisco"</b> calculado neste diagnóstico reflete o valor total subtraído do rendimento real do trabalhador. 
                Ele não considera apenas a tarifa, mas o <b>valor monetário do tempo de vida</b> convertido em deslocamento. 
                Na perspectiva da economia política, o trecho é <b>"trabalho não pago"</b>: um tempo obrigatório para a 
                reprodução da força de trabalho que não é remunerado, gerando uma depreciação real de 
                <span style="color: #E63946; font-weight: bold;">{depre:.1f}%</span> no valor da sua hora contratada.
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Download
        st.download_button("📥 BAIXAR NOTA TÉCNICA", f"Diagnóstico do Trecho\nConfisco: R$ {confi:.2f}\nDepreciação: {depre:.1f}%", file_name="diagnostico.txt")
    else:
        st.error("⚠️ Preencha o salário e o município de moradia.")

