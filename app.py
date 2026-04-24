import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

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
footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


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
    """Retorna cor conforme situação da nota."""
    if v >= 6.0:
        return "#22c55e"
    elif v >= 4.0:
        return "#f59e0b"
    return "#ef4444"


# ─────────────────────────────────────────
#  FUNÇÕES DE GRÁFICO (Matplotlib)
# ─────────────────────────────────────────

BG = "#0d1b2a"
TEXT_COLOR = "#a0b4c8"


def grafico_barras(valores):
    """Gráfico de barras com uma barra por nota."""
    labels = [f"Nota {i+1}" for i in range(len(valores))]
    cores  = [cor_por_nota(v) for v in valores]

    fig, ax = plt.subplots(figsize=(5, 3.2))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    bars = ax.bar(labels, valores, color=cores, width=0.5,
                  edgecolor="rgba(255,255,255,0.1)", linewidth=0.8)

    # Valor em cima de cada barra
    for bar, v in zip(bars, valores):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.2,
                f"{v:.1f}", ha="center", va="bottom",
                color="#e8f0f7", fontsize=10, fontweight="bold")

    # Linhas de referência
    ax.axhline(6.0, color="#22c55e", linestyle="--", linewidth=1.2, alpha=0.7)
    ax.axhline(4.0, color="#f59e0b", linestyle="--", linewidth=1.2, alpha=0.7)
    ax.text(len(valores) - 0.5, 6.15, "Aprovação", color="#22c55e", fontsize=7.5, ha="right")
    ax.text(len(valores) - 0.5, 4.15, "Recuperação", color="#f59e0b", fontsize=7.5, ha="right")

    ax.set_ylim(0, 11.5)
    ax.set_yticks(range(0, 11))
    ax.tick_params(colors=TEXT_COLOR, labelsize=9)
    ax.spines[:].set_visible(False)
    ax.yaxis.grid(True, color="rgba(255,255,255,0.06)", linewidth=0.7)
    ax.set_axisbelow(True)
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_color(TEXT_COLOR)

    plt.tight_layout()
    return fig


def grafico_linha(valores, media):
    """Gráfico de linha mostrando a evolução das notas."""
    labels = [f"Nota {i+1}" for i in range(len(valores))]
    xs = range(len(valores))

    fig, ax = plt.subplots(figsize=(5, 3.2))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    # Área preenchida
    ax.fill_between(xs, valores, alpha=0.12, color="#f0c040")

    # Linha principal
    ax.plot(xs, valores, color="#f0c040", linewidth=2.2, zorder=3)

    # Pontos coloridos por situação
    for i, v in enumerate(valores):
        ax.scatter(i, v, color=cor_por_nota(v), s=70, zorder=4,
                   edgecolors="#0d1b2a", linewidths=1.5)
        ax.text(i, v + 0.35, f"{v:.1f}", ha="center", va="bottom",
                color="#e8f0f7", fontsize=9, fontweight="bold")

    # Linha da média
    ax.axhline(media, color="#f0c040", linestyle=":", linewidth=1.4, alpha=0.8)
    ax.text(len(valores) - 1, media + 0.3, f"Média {media:.2f}",
            ha="right", color="#f0c040", fontsize=8)

    ax.set_xticks(list(xs))
    ax.set_xticklabels(labels)
    ax.set_ylim(0, 11.5)
    ax.set_yticks(range(0, 11))
    ax.spines[:].set_visible(False)
    ax.yaxis.grid(True, color="rgba(255,255,255,0.06)", linewidth=0.7)
    ax.set_axisbelow(True)
    ax.tick_params(colors=TEXT_COLOR, labelsize=9)
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_color(TEXT_COLOR)

    plt.tight_layout()
    return fig


def grafico_gauge(media, cor_hex):
    """Velocímetro semicircular mostrando a média."""
    fig, ax = plt.subplots(figsize=(5, 2.8),
                           subplot_kw=dict(polar=True))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    # Ângulos: π (esquerda=0) → 0 (direita=10)
    theta_min, theta_max = np.pi, 0
    zonas = [
        (0,   4.0, "#ef4444"),
        (4.0, 6.0, "#f59e0b"),
        (6.0, 10,  "#22c55e"),
    ]

    for v_ini, v_fim, cor in zonas:
        t0 = theta_max + (theta_min - theta_max) * (1 - v_ini / 10)
        t1 = theta_max + (theta_min - theta_max) * (1 - v_fim / 10)
        theta = np.linspace(t1, t0, 60)
        # Faixa externa (anel)
        ax.bar(x=theta, height=0.3, width=(t0 - t1) / 60,
               bottom=0.65, color=cor, alpha=0.35, linewidth=0)
        ax.bar(x=np.mean(theta), height=0.02, width=(t0 - t1),
               bottom=0.93, color=cor, alpha=0.8, linewidth=0)

    # Agulha
    angulo_media = theta_max + (theta_min - theta_max) * (1 - media / 10)
    ax.annotate("", xy=(angulo_media, 0.75),
                xytext=(angulo_media + np.pi, 0.08),
                arrowprops=dict(arrowstyle="-|>",
                                color=cor_hex, lw=2.2,
                                mutation_scale=14))

    # Ponto central
    ax.scatter([0], [0], s=60, color=cor_hex, zorder=5)

    # Texto da média no centro
    ax.text(0, -0.25, f"{media:.2f}", ha="center", va="center",
            fontsize=22, fontweight="bold", color=cor_hex,
            transform=ax.transData)
    ax.text(0, -0.5, "média", ha="center", va="center",
            fontsize=9, color=TEXT_COLOR, transform=ax.transData)

    # Rótulos 0, 5, 10
    for val, label in [(0, "0"), (5, "5"), (10, "10")]:
        ang = theta_max + (theta_min - theta_max) * (1 - val / 10)
        ax.text(ang, 1.08, label, ha="center", va="center",
                fontsize=8, color=TEXT_COLOR)

    ax.set_ylim(-0.6, 1.2)
    ax.set_xlim(0, np.pi)
    ax.set_theta_direction(-1)
    ax.set_theta_offset(0)
    ax.axis("off")
    plt.tight_layout()
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
nome = st.text_input("Nome completo", placeholder="Ex: João da Silva", key="nome_estudante")

st.markdown("<hr class='divisor'>", unsafe_allow_html=True)
st.markdown("##### 📝 Notas")

notas_input = []
for i in range(st.session_state.num_notas):
    v = st.text_input(f"Nota {i + 1}", placeholder="Ex: 7.5", key=f"nota_{i}")
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

        # ── Velocímetro centralizado ──
        st.markdown("**🎯 Velocímetro da Média**")
        st.pyplot(grafico_gauge(media, cor), use_container_width=True)

        # ── Barras + Linha lado a lado ──
        col_bar, col_lin = st.columns(2)
        with col_bar:
            st.markdown("**📊 Notas por Avaliação**")
            st.pyplot(grafico_barras(valores), use_container_width=True)
        with col_lin:
            st.markdown("**📈 Evolução das Notas**")
            st.pyplot(grafico_linha(valores, media), use_container_width=True)

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
