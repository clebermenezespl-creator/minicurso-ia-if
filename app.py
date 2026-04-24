import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

# ─────────────────────────────────────────
#  CONFIGURAÇÃO DA PÁGINA
# ─────────────────────────────────────────
st.set_page_config(
    page_title="Calculadora de Notas do IF",
    page_icon="🎓",
    layout="centered"
)

# ─────────────────────────────────────────
#  ESTILO VISUAL
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Lato:wght@300;400;700&display=swap');

.stApp {
    background: linear-gradient(160deg, #1b2838 0%, #0d1b2a 100%);
    font-family: 'Lato', sans-serif;
}
.titulo {
    font-family: 'Playfair Display', serif;
    font-size: 2.5rem;
    font-weight: 900;
    color: #f0c040;
    text-align: center;
    margin-bottom: 0.1rem;
}
.subtitulo {
    text-align: center;
    color: #7a90a4;
    font-size: 0.9rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 2rem;
}
.card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1.6rem 2rem;
    margin-bottom: 1.2rem;
}
.stTextInput > label {
    color: #a0b4c8 !important;
    font-size: 0.82rem !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
}
.stTextInput > div > div > input {
    background: #0d1b2a !important;
    border: 1px solid #2a3f55 !important;
    border-radius: 10px !important;
    color: #e8f0f7 !important;
    font-size: 1.05rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: #f0c040 !important;
    box-shadow: 0 0 0 2px rgba(240,192,64,0.2) !important;
}
.stButton > button {
    font-family: 'Playfair Display', serif !important;
    font-weight: 700 !important;
    border-radius: 10px !important;
    border: none !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
}
.res-aprovado {
    background: linear-gradient(135deg, #0a2e1a, #0d3d20);
    border: 1px solid #22c55e;
    border-radius: 16px;
    padding: 1.6rem;
    text-align: center;
}
.res-recuperacao {
    background: linear-gradient(135deg, #2e1f00, #3d2a00);
    border: 1px solid #f59e0b;
    border-radius: 16px;
    padding: 1.6rem;
    text-align: center;
}
.res-reprovado {
    background: linear-gradient(135deg, #2e0a0a, #3d0d0d);
    border: 1px solid #ef4444;
    border-radius: 16px;
    padding: 1.6rem;
    text-align: center;
}
.nome-aluno {
    font-family: 'Playfair Display', serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #e8f0f7;
    margin-bottom: 0.3rem;
}
.media-num {
    font-family: 'Playfair Display', serif;
    font-size: 4rem;
    font-weight: 900;
    line-height: 1;
}
.situacao {
    font-size: 1.1rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 0.3rem;
}
.detalhe {
    font-size: 0.82rem;
    color: #7a90a4;
    margin-top: 0.7rem;
}
.criterio {
    display: flex;
    gap: 0.6rem;
    padding: 0.5rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    font-size: 0.88rem;
    color: #a0b4c8;
}
.divisor {
    border: none;
    border-top: 1px solid rgba(255,255,255,0.07);
    margin: 1rem 0;
}
.grafico-titulo {
    color: #7a90a4;
    font-size: 0.78rem;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
#  CONFIGURAÇÃO PADRÃO DOS GRÁFICOS PLOTLY
# ─────────────────────────────────────────
PLOT_BG   = "rgba(0,0,0,0)"
PAPER_BG  = "rgba(0,0,0,0)"
FONT_COLOR = "#a0b4c8"
GRID_COLOR = "rgba(255,255,255,0.06)"


# ─────────────────────────────────────────
#  FUNÇÕES AUXILIARES
# ─────────────────────────────────────────

def validar_nome(nome):
    """Valida o nome do estudante."""
    if not nome.strip():
        return "⚠️ Por favor, informe o nome do estudante."
    if len(nome.strip()) < 3:
        return "❌ O nome deve ter pelo menos 3 caracteres."
    return None


def validar_nota(texto, numero):
    """Valida uma nota digitada. Retorna (valor_float, erro)."""
    if not texto.strip():
        return None, f"⚠️ Nota {numero} está vazia."
    try:
        valor = float(texto.replace(",", "."))
    except ValueError:
        return None, f"❌ Nota {numero}: '{texto}' não é um número válido."
    if not (0 <= valor <= 10):
        return None, f"❌ Nota {numero}: deve estar entre 0 e 10."
    return valor, None


def classificar_media(media):
    """Retorna (classe_css, emoji, situacao, cor_hex)."""
    if media >= 6.0:
        return "res-aprovado", "✅", "APROVADO", "#22c55e"
    elif media >= 4.0:
        return "res-recuperacao", "⚠️", "RECUPERAÇÃO", "#f59e0b"
    else:
        return "res-reprovado", "❌", "REPROVADO", "#ef4444"


def cor_por_nota(v):
    """Retorna a cor de uma barra conforme o valor da nota."""
    if v >= 6.0:
        return "#22c55e"
    elif v >= 4.0:
        return "#f59e0b"
    return "#ef4444"


# ─────────────────────────────────────────
#  FUNÇÕES DE GRÁFICO
# ─────────────────────────────────────────

def grafico_barras(valores):
    """Gráfico de barras com uma barra por nota, colorida pela situação."""
    labels = [f"Nota {i+1}" for i in range(len(valores))]
    cores  = [cor_por_nota(v) for v in valores]

    fig = go.Figure(go.Bar(
        x=labels,
        y=valores,
        marker_color=cores,
        marker_line_color="rgba(255,255,255,0.1)",
        marker_line_width=1,
        text=[f"{v:.1f}" for v in valores],
        textposition="outside",
        textfont=dict(color="#e8f0f7", size=13),
    ))

    # Linha de aprovação (6.0) e recuperação (4.0)
    fig.add_hline(y=6.0, line_dash="dash", line_color="#22c55e",
                  annotation_text="Aprovação (6.0)", annotation_font_color="#22c55e",
                  annotation_position="top right")
    fig.add_hline(y=4.0, line_dash="dash", line_color="#f59e0b",
                  annotation_text="Recuperação (4.0)", annotation_font_color="#f59e0b",
                  annotation_position="bottom right")

    fig.update_layout(
        plot_bgcolor=PLOT_BG, paper_bgcolor=PAPER_BG,
        font=dict(color=FONT_COLOR, family="Lato"),
        margin=dict(t=20, b=10, l=10, r=10),
        yaxis=dict(range=[0, 11], gridcolor=GRID_COLOR, tickfont=dict(color=FONT_COLOR)),
        xaxis=dict(tickfont=dict(color=FONT_COLOR)),
        showlegend=False,
        height=300,
    )
    return fig


def grafico_gauge(media, cor):
    """Velocímetro mostrando a média do aluno de 0 a 10."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=media,
        number=dict(font=dict(color=cor, size=40, family="Playfair Display"), suffix=""),
        gauge=dict(
            axis=dict(
                range=[0, 10],
                tickwidth=1,
                tickcolor=FONT_COLOR,
                tickfont=dict(color=FONT_COLOR),
            ),
            bar=dict(color=cor, thickness=0.25),
            bgcolor="rgba(255,255,255,0.03)",
            borderwidth=0,
            steps=[
                dict(range=[0,   4.0], color="rgba(239,68,68,0.15)"),
                dict(range=[4.0, 6.0], color="rgba(245,158,11,0.15)"),
                dict(range=[6.0, 10],  color="rgba(34,197,94,0.15)"),
            ],
            threshold=dict(
                line=dict(color=cor, width=3),
                thickness=0.75,
                value=media,
            ),
        ),
    ))
    fig.update_layout(
        plot_bgcolor=PLOT_BG, paper_bgcolor=PAPER_BG,
        font=dict(color=FONT_COLOR, family="Lato"),
        margin=dict(t=20, b=10, l=20, r=20),
        height=230,
    )
    return fig


def grafico_linha(valores):
    """Gráfico de linha mostrando a evolução das notas ao longo das avaliações."""
    labels = [f"Nota {i+1}" for i in range(len(valores))]
    media  = sum(valores) / len(valores)

    fig = go.Figure()

    # Área sombreada abaixo da linha
    fig.add_trace(go.Scatter(
        x=labels, y=valores,
        fill="tozeroy",
        fillcolor="rgba(240,192,64,0.07)",
        line=dict(color="#f0c040", width=2.5),
        mode="lines+markers",
        marker=dict(size=9, color=[cor_por_nota(v) for v in valores],
                    line=dict(color="#0d1b2a", width=2)),
        text=[f"{v:.1f}" for v in valores],
        textposition="top center",
        textfont=dict(color="#e8f0f7"),
    ))

    # Linha da média
    fig.add_hline(y=media, line_dash="dot", line_color="#f0c040", line_width=1.5,
                  annotation_text=f"Média: {media:.2f}",
                  annotation_font_color="#f0c040",
                  annotation_position="top left")

    fig.update_layout(
        plot_bgcolor=PLOT_BG, paper_bgcolor=PAPER_BG,
        font=dict(color=FONT_COLOR, family="Lato"),
        margin=dict(t=20, b=10, l=10, r=10),
        yaxis=dict(range=[0, 11], gridcolor=GRID_COLOR, tickfont=dict(color=FONT_COLOR)),
        xaxis=dict(tickfont=dict(color=FONT_COLOR), gridcolor=GRID_COLOR),
        showlegend=False,
        height=270,
    )
    return fig


# ─────────────────────────────────────────
#  ESTADO DA SESSÃO
# ─────────────────────────────────────────

if "num_notas" not in st.session_state:
    st.session_state.num_notas = 2


# ─────────────────────────────────────────
#  CABEÇALHO
# ─────────────────────────────────────────

st.markdown("<div class='titulo'>🎓 Calculadora de Notas</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitulo'>Instituto Federal · Avaliação de Desempenho</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────
#  CARD DE ENTRADA
# ─────────────────────────────────────────

st.markdown("<div class='card'>", unsafe_allow_html=True)

st.markdown("##### 👤 Dados do Estudante")
nome = st.text_input(
    "Nome completo",
    placeholder="Ex: João da Silva",
    key="nome_estudante"
)

st.markdown("<hr class='divisor'>", unsafe_allow_html=True)
st.markdown("##### 📝 Notas")

notas_input = []
for i in range(st.session_state.num_notas):
    v = st.text_input(
        f"Nota {i + 1}",
        placeholder="Ex: 7.5",
        key=f"nota_{i}"
    )
    notas_input.append(v)

if st.button("➕ Adicionar nota"):
    st.session_state.num_notas += 1
    st.rerun()

st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────
#  BOTÕES CALCULAR e LIMPAR
# ─────────────────────────────────────────

col1, col2 = st.columns([4, 1])
with col1:
    calcular = st.button("🎯 Calcular Média")
with col2:
    if st.button("🗑️"):
        st.session_state.pop("nome_estudante", None)
        for i in range(st.session_state.num_notas + 5):
            st.session_state.pop(f"nota_{i}", None)
        st.session_state.num_notas = 2
        st.rerun()


# ─────────────────────────────────────────
#  LÓGICA DE CÁLCULO E EXIBIÇÃO
# ─────────────────────────────────────────

if calcular:
    erros  = []
    valores = []

    erro_nome = validar_nome(nome)
    if erro_nome:
        erros.append(erro_nome)

    for i, entrada in enumerate(notas_input):
        valor, erro = validar_nota(entrada, i + 1)
        if erro:
            erros.append(erro)
        else:
            valores.append(valor)

    if erros:
        for msg in erros:
            st.error(msg)

    elif valores:
        media = sum(valores) / len(valores)
        classe, emoji, situacao, cor = classificar_media(media)
        detalhe = "  ·  ".join([f"N{i+1}: {v:.1f}" for i, v in enumerate(valores)])
        nome_fmt = nome.strip().title()

        # ── Card de resultado ──
        st.markdown(f"""
        <div class='{classe}'>
            <div class='nome-aluno'>👤 {nome_fmt}</div>
            <div class='media-num' style='color:{cor}'>{media:.2f}</div>
            <div class='situacao' style='color:{cor}'>{emoji} {situacao}</div>
            <div class='detalhe'>{detalhe}</div>
            <div class='detalhe'>{len(valores)} nota(s) considerada(s)</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Gráfico Gauge (velocímetro da média) ──
        st.markdown("<p class='grafico-titulo'>🎯 Velocímetro da Média</p>", unsafe_allow_html=True)
        st.plotly_chart(grafico_gauge(media, cor), use_container_width=True)

        # ── Gráficos lado a lado: Barras + Linha ──
        col_bar, col_lin = st.columns(2)

        with col_bar:
            st.markdown("<p class='grafico-titulo'>📊 Notas por Avaliação</p>", unsafe_allow_html=True)
            st.plotly_chart(grafico_barras(valores), use_container_width=True)

        with col_lin:
            st.markdown("<p class='grafico-titulo'>📈 Evolução das Notas</p>", unsafe_allow_html=True)
            st.plotly_chart(grafico_linha(valores), use_container_width=True)

        # ── Barra de progresso ──
        st.markdown("<br>", unsafe_allow_html=True)
        st.progress(media / 10, text=f"{nome_fmt} · Média {media:.2f} / 10.0")


# ─────────────────────────────────────────
#  TABELA DE CRITÉRIOS
# ─────────────────────────────────────────

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div class='card'>
    <p style='color:#7a90a4;font-size:0.78rem;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:0.8rem'>
        📋 Critérios de avaliação
    </p>
    <div class='criterio'>
        <span>✅</span>
        <span><strong style='color:#22c55e'>Aprovado</strong> — Média ≥ 6.0</span>
    </div>
    <div class='criterio'>
        <span>⚠️</span>
        <span><strong style='color:#f59e0b'>Recuperação</strong> — 4.0 ≤ Média &lt; 6.0</span>
    </div>
    <div class='criterio' style='border-bottom:none'>
        <span>❌</span>
        <span><strong style='color:#ef4444'>Reprovado</strong> — Média &lt; 4.0</span>
    </div>
</div>
<p style='text-align:center;color:#2a3f55;font-size:0.75rem;margin-top:1rem'>
    Calculadora de Notas · Instituto Federal
</p>
""", unsafe_allow_html=True)
