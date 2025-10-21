# ...existing code...
import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
import os

# Mover set_page_config antes de qualquer chamada st.*
st.set_page_config(page_title="Heineken Productivity Tracker", page_icon="🍺", layout="centered")

# --- Login simples ---
st.sidebar.title("👤 Login")
usuario = st.sidebar.text_input("Digite seu nome", value="Alline").strip()

if not usuario:
    st.warning("Por favor, digite seu nome para continuar.")
    st.stop()

ARQUIVO = f"registro_{usuario.lower()}.csv"

# --- Função para registrar evento ---
def registrar_evento(tipo):
    agora = datetime.datetime.now()
    novo = pd.DataFrame([[agora, tipo]], columns=["DataHora", "Evento"])
    if os.path.exists(ARQUIVO):
        novo.to_csv(ARQUIVO, mode="a", header=False, index=False)
    else:
        novo.to_csv(ARQUIVO, mode="w", header=True, index=False)

# --- Carregar dados (robusto) ---
if os.path.exists(ARQUIVO):
    try:
        df = pd.read_csv(ARQUIVO, header=0)
    except Exception:
        df = pd.DataFrame(columns=["DataHora", "Evento"])
else:
    df = pd.DataFrame(columns=["DataHora", "Evento"])

# Garantir colunas mínimas
for col in ["DataHora", "Evento"]:
    if col not in df.columns:
        df[col] = pd.NA

# Converter DataHora com coercion (valores inválidos -> NaT)
df["DataHora"] = pd.to_datetime(df["DataHora"], errors="coerce")

# Criar versão válida para operações que exigem DataHora
df_valid = df.dropna(subset=["DataHora"]).reset_index(drop=True)

# --- Interface ---
st.markdown(
    """
    <style>
    .main {
        background-color: #f0f3f5;
    }
    h1, h2, h3 {
        color: #046c3c;
        font-family: 'Segoe UI', sans-serif;
    }
    .stButton>button {
        background-color: #046c3c;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5em 1em;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #059e5c;
        color: #f0f3f5;
    }
    .stSidebar {
        background-color: #e6f2ec;
    }
    .css-1d391kg {
        background-color: #e6f2ec;
    }
    .stMarkdown {
        font-family: 'Segoe UI', sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🍺 Heineken Productivity Tracker")
st.subheader(f"Bem-vindo, {usuario}! Sua rotina com estilo e eficiência.")

# --- Botões de registro ---
col1, col2 = st.columns(2)
with col1:
    if st.button("✅ Tarefa concluída"):
        registrar_evento("Tarefa")
with col2:
    if st.button("💧 Pausa para água"):
        registrar_evento("Água")

col3, col4 = st.columns(2)
with col3:
    if st.button("🍽️ Pausa para almoço"):
        registrar_evento("Almoço")
with col4:
    if st.button("🧘 Pausa para descanso"):
        registrar_evento("Descanso")

# --- Resumo do dia ---
hoje = datetime.date.today()
df_hoje = df_valid[df_valid["DataHora"].dt.date == hoje]
resumo = df_hoje["Evento"].value_counts()

st.markdown("### 📊 Resumo de hoje")
for evento in ["Tarefa", "Água", "Almoço", "Descanso"]:
    st.write(f"- {evento}: {resumo.get(evento, 0)}")

# --- Gráfico diário ---
if not df_hoje.empty:
    fig = px.histogram(df_hoje, x="Evento", color="Evento", title="Eventos registrados hoje")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Nenhum evento registrado hoje ainda.")

# --- Frase motivacional ---
if resumo.get("Tarefa", 0) >= 5:
    st.success("🚀 Você está voando hoje! Produtividade no talo.")
elif resumo.get("Tarefa", 0) >= 2:
    st.info("💪 Bom ritmo! Continue assim.")
else:
    st.warning("⏳ Bora focar! Ainda dá tempo de fazer acontecer.")

# --- Histórico semanal ---
st.markdown("### 📅 Histórico dos últimos 7 dias")
if not df_valid.empty:
    ultima_semana = df_valid[df_valid["DataHora"] >= (datetime.datetime.now() - datetime.timedelta(days=7))].copy()
else:
    ultima_semana = pd.DataFrame(columns=df_valid.columns)

if not ultima_semana.empty:
    ultima_semana["Dia"] = ultima_semana["DataHora"].dt.date
    fig2 = px.histogram(
        ultima_semana,
        x="Dia",
        color="Evento",
        title=f"Eventos por dia - {usuario}"
    )
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("Ainda não há registros suficientes para mostrar o histórico.")

# --- Bloco de estudo: exemplo de código C# ---
st.markdown("### 🧠 Estudo: Diferença entre métodos Get/Set e propriedades")
codigo_csharp = """
// Versão com métodos Get/Set
class Student {
    private int id;
    public int GetId() { return id; }
    public void SetId(int i) { id = i; }
}

// Versão com propriedade automática
class Student {
    public int Id { get; set; }
}

// Teste com múltiplas instâncias
class Test {
    public static void Main() {
        Student s = new Student();
        s.Id = 5;
        Student t = new Student();
        t.Id = 6;
        Console.WriteLine(s.Id + " " + t.Id);
    }
}
"""
st.code(codigo_csharp, language="csharp")

# --- Alertas automáticos ---
ultima_agua = df_valid[df_valid["Evento"] == "Água"]["DataHora"].max()
tempo_desde_agua = (datetime.datetime.now() - ultima_agua).total_seconds() / 60 if not pd.isna(ultima_agua) else None

if tempo_desde_agua and tempo_desde_agua > 60:
    st.warning("🚨 Já faz mais de 1 hora desde sua última pausa para água. Hidrate-se!")

ultima_tarefa = df_valid[df_valid["Evento"] == "Tarefa"]["DataHora"].max()
tempo_desde_tarefa = (datetime.datetime.now() - ultima_tarefa).total_seconds() / 60 if not pd.isna(ultima_tarefa) else None

if tempo_desde_tarefa and tempo_desde_tarefa > 90:
    st.warning("⏰ Está na hora de revisar suas tarefas. Que tal concluir mais uma?")