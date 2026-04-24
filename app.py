import streamlit as st

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

.stApp { background: linear-gradient(160deg,#1b2838 0%,#0d1b2a 100%); font-family:'Lato',sans-serif; }

.titulo { font-family:'Playfair Display',serif; font-size:2.5rem; font-weight:900; color:#f0c040; text-align:center; margin-bottom:.1rem; }
.subtitulo { text-align:center; color:#7a90a4; font-size:.9rem; letter-spacing:2px; text-transform:uppercase; margin-bottom:2rem; }

.card { background:rgba(255,255,255,.04); border:1px solid rgba(255,255,255,.08); border-radius:16px; padding:1.6rem 2rem; margin-bottom:1.2rem; }

.stTextInput>label { color:#a0b4c8!important; font-size:.82rem!important; font-weight:700!important; letter-spacing:1px!important; text-transform:uppercase!important; }
.stTextInput>div>div>input { background:#0d1b2a!important; border:1px solid #2a3f55!important; border-radius:10px!important; color:#e8f0f7!important; font-size:1.05rem!important; }
.stTextInput>div>div>input:focus { border-color:#f0c040!important; box-shadow:0 0 0 2px rgba(240,192,64,.2)!important; }

.stButton>button { font-family:'Playfair Display',serif!important; font-weight:700!important; border-radius:10px!important; border:none!important; width:100%!important; transition:all .2s ease!important; }

.res-aprovado   { background:linear-gradient(135deg,#0a2e1a,#0d3d20); border:1px solid #22c55e; border-radius:16px; padding:1.6rem; text-align:center; }
.res-recuperacao{ background:linear-gradient(135deg,#2e1f00,#3d2a00); border:1px solid #f59e0b; border-radius:16px; padding:1.6rem; text-align:center; }
.res-reprovado  { background:linear-gradient(135deg,#2e0a0a,#3d0d0d); border:1px solid #ef4444; border-radius:16px; padding:1.6rem; text-align:center; }

.nome-aluno { font-family:'Playfair Display',serif; font-size:1.1rem; font-weight:700; color:#e8f0f7; margin-bottom:.3rem; }
.media-num  { font-family:'Playfair Display',serif; font-size:4rem; font-weight:900; line-height:1; }
.situacao   { font-size:1.1rem; font-weight:700; letter-spacing:2px; text-transform:uppercase; margin-top:.3rem; }
.detalhe    { font-size:.82rem; color:#7a90a4; margin-top:.7rem; }

.criterio   { display:flex; gap:.6rem; padding:.5rem 0; border-bottom:1px solid rgba(255,255,255,.05); font-size:.88rem; color:#a0b4c8; }
.divisor    { border:none; border-top:1px solid rgba(255,255,255,.07); margin:1rem 0; }

/* ── Gráficos HTML ── */
.chart-wrap { background:rgba(255,255,255,.03); border:1px solid rgba(255,255,255,.07); border-radius:14px; padding:1.2rem 1.4rem; margin-top:.8rem; }
.chart-title{ color:#7a90a4; font-size:.75rem; letter-spacing:1.5px; text-transform:uppercase; margin-bottom:1rem; }

/* Barras */
.bar-row    { display:flex; align-items:flex-end; gap:10px; height:140px; padding-bottom:4px; }
.bar-col    { display:flex; flex-direction:column; align-items:center; flex:1; height:100%; justify-content:flex-end; }
.bar        { width:100%; border-radius:6px 6px 0 0; transition:height .5s ease; position:relative; min-height:4px; }
.bar-val    { font-size:.8rem; font-weight:700; color:#e8f0f7; margin-bottom:4px; }
.bar-label  { font-size:.72rem; color:#7a90a4; margin-top:6px; }
.bar-axis   { border-top:1px solid rgba(255,255,255,.1); margin-top:4px; }

/* Linha de referência */
.ref-lines  { position:relative; }

/* Gauge */
.gauge-wrap { display:flex; flex-direction:column; align-items:center; }
.gauge-bar  { width:100%; height:22px; border-radius:11px; background:linear-gradient(to right,#ef4444 0%,#ef4444 40%,#f59e0b 40%,#f59e0b 60%,#22c55e 60%,#22c55e 100%); position:relative; margin:8px 0; }
.gauge-ptr  { position:absolute; top:-6px; width:4px; height:34px; background:#fff; border-radius:2px; transform:translateX(-50%); box-shadow:0 0 8px rgba(255,255,255,.5); transition:left .6s ease; }
.gauge-labels { display:flex; justify-content:space-between; font-size:.72rem; color:#7a90a4; width:100%; }
.gauge-val  { font-family:'Playfair Display',serif; font-size:2.8rem; font-weight:900; margin-top:.4rem; }

/* Linha/evolução */
.linechart  { position:relative; height:120px; width:100%; }
.lc-svg     { width:100%; height:100%; overflow:visible; }

footer { visibility:hidden; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
#  FUNÇÕES AUXILIARES
# ─────────────────────────────────────────

def validar_nome(nome):
    if not nome.strip():
        return "⚠️ Por favor, informe o nome do estudante."
    if len(nome.strip()) < 3:
        return "❌ O nome deve ter pelo menos 3 caracteres."
    return None


def validar_nota(texto, numero):
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
    if media >= 6.0:
        return "res-aprovado", "✅", "APROVADO", "#22c55e"
    elif media >= 4.0:
        return "res-recuperacao", "⚠️", "RECUPERAÇÃO", "#f59e0b"
    else:
        return "res-reprovado", "❌", "REPROVADO", "#ef4444"


def cor_nota(v):
    if v >= 6.0: return "#22c55e"
    if v >= 4.0: return "#f59e0b"
    return "#ef4444"


# ─────────────────────────────────────────
#  FUNÇÕES DE GRÁFICO (HTML puro)
# ─────────────────────────────────────────

def html_barras(valores):
    """Gráfico de barras em HTML/CSS — sem dependências."""
    max_val = 10
    colunas = ""
    for i, v in enumerate(valores):
        h_pct = (v / max_val) * 100
        cor   = cor_nota(v)
        colunas += f"""
        <div class="bar-col">
            <div class="bar-val">{v:.1f}</div>
            <div class="bar" style="height:{h_pct}%;background:{cor};opacity:.85;"></div>
            <div class="bar-label">N{i+1}</div>
        </div>"""

    # linhas de referência como sobreposição
    linha_apr = (6 / max_val) * 100
    linha_rec = (4 / max_val) * 100

    return f"""
    <div class="chart-wrap">
        <div class="chart-title">📊 Notas por Avaliação</div>
        <div style="position:relative;">
            <div style="position:absolute;bottom:{linha_apr}%;left:0;right:0;
                        border-top:1px dashed #22c55e;opacity:.7;z-index:1;">
                <span style="font-size:.65rem;color:#22c55e;padding-left:4px;">6.0</span>
            </div>
            <div style="position:absolute;bottom:{linha_rec}%;left:0;right:0;
                        border-top:1px dashed #f59e0b;opacity:.7;z-index:1;">
                <span style="font-size:.65rem;color:#f59e0b;padding-left:4px;">4.0</span>
            </div>
            <div class="bar-row">{colunas}</div>
        </div>
        <div class="bar-axis"></div>
    </div>"""


def html_gauge(media, cor):
    """Barra de progresso estilizada como gauge."""
    pct = (media / 10) * 100
    return f"""
    <div class="chart-wrap">
        <div class="chart-title">🎯 Velocímetro da Média</div>
        <div class="gauge-wrap">
            <div style="position:relative;width:100%;">
                <div class="gauge-bar"></div>
                <div class="gauge-ptr" style="left:{pct}%;"></div>
            </div>
            <div class="gauge-labels">
                <span>0 — Reprovado</span>
                <span>4 — Recuperação</span>
                <span>6 — Aprovado</span>
                <span>10</span>
            </div>
            <div class="gauge-val" style="color:{cor};">{media:.2f}</div>
        </div>
    </div>"""


def html_linha(valores, media):
    """Gráfico de linha com SVG inline."""
    n   = len(valores)
    W, H = 400, 120
    pad  = 20

    # Coordenadas dos pontos
    def px(i): return pad + i * (W - 2*pad) / max(n - 1, 1)
    def py(v): return H - pad - (v / 10) * (H - 2*pad)

    # Linha principal
    pontos = " ".join(f"{px(i):.1f},{py(v):.1f}" for i, v in enumerate(valores))

    # Área preenchida (polygon)
    area = (f"{px(0):.1f},{H-pad} " + pontos +
            f" {px(n-1):.1f},{H-pad}")

    # Linha da média
    y_med = py(media)

    # Pontos coloridos
    circles = ""
    labels  = ""
    for i, v in enumerate(valores):
        cx, cy = px(i), py(v)
        circles += f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="5" fill="{cor_nota(v)}" stroke="#0d1b2a" stroke-width="2"/>'
        labels  += f'<text x="{cx:.1f}" y="{cy-10:.1f}" text-anchor="middle" fill="#e8f0f7" font-size="10" font-weight="bold">{v:.1f}</text>'
        labels  += f'<text x="{cx:.1f}" y="{H-4:.1f}" text-anchor="middle" fill="#7a90a4" font-size="9">N{i+1}</text>'

    svg = f"""
    <svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;">
        <!-- Área -->
        <polygon points="{area}" fill="#f0c040" fill-opacity=".08"/>
        <!-- Linha média -->
        <line x1="{pad}" y1="{y_med:.1f}" x2="{W-pad}" y2="{y_med:.1f}"
              stroke="#f0c040" stroke-width="1.2" stroke-dasharray="4,3" opacity=".7"/>
        <text x="{W-pad+2}" y="{y_med:.1f}" fill="#f0c040" font-size="9" dominant-baseline="middle">
            {media:.2f}
        </text>
        <!-- Linha principal -->
        <polyline points="{pontos}" fill="none" stroke="#f0c040" stroke-width="2.2"
                  stroke-linejoin="round" stroke-linecap="round"/>
        {circles}
        {labels}
    </svg>"""

    return f"""
    <div class="chart-wrap">
        <div class="chart-title">📈 Evolução das Notas</div>
        {svg}
    </div>"""


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
    erros   = []
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
        media    = sum(valores) / len(valores)
        classe, emoji, situacao, cor = classificar_media(media)
        detalhe  = "  ·  ".join([f"N{i+1}: {v:.1f}" for i, v in enumerate(valores)])
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

        # ── Gauge ──
        st.markdown(html_gauge(media, cor), unsafe_allow_html=True)

        # ── Barras + Linha lado a lado ──
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(html_barras(valores), unsafe_allow_html=True)
        with col_b:
            st.markdown(html_linha(valores, media), unsafe_allow_html=True)

        # ── Barra de progresso nativa ──
        st.markdown("<br>", unsafe_allow_html=True)
        st.progress(media / 10, text=f"{nome_fmt} · Média {media:.2f} / 10.0")


# ─────────────────────────────────────────
#  TABELA DE CRITÉRIOS
# ─────────────────────────────────────────

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div class='card'>
    <p style='color:#7a90a4;font-size:.78rem;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:.8rem'>
        📋 Critérios de avaliação
    </p>
    <div class='criterio'><span>✅</span><span><strong style='color:#22c55e'>Aprovado</strong> — Média ≥ 6.0</span></div>
    <div class='criterio'><span>⚠️</span><span><strong style='color:#f59e0b'>Recuperação</strong> — 4.0 ≤ Média &lt; 6.0</span></div>
    <div class='criterio' style='border-bottom:none'><span>❌</span><span><strong style='color:#ef4444'>Reprovado</strong> — Média &lt; 4.0</span></div>
</div>
<p style='text-align:center;color:#2a3f55;font-size:.75rem;margin-top:1rem'>
    Calculadora de Notas · Instituto Federal
</p>
""", unsafe_allow_html=True)
