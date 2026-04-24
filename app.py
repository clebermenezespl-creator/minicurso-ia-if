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
    """Valida o nome do estudante. Retorna mensagem de erro ou None."""
    if not nome.strip():
        return "⚠️ Por favor, informe o nome do estudante."
    if len(nome.strip()) < 3:
        return "❌ O nome deve ter pelo menos 3 caracteres."
    return None


def validar_nota(texto, numero):
    """
    Valida uma nota digitada.
    Retorna (valor_float, mensagem_erro).
    Se válida, mensagem_erro será None.
    """
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
    """
    Retorna (classe_css, emoji, texto_situacao, cor_hex)
    com base na média calculada.
    """
    if media >= 6.0:
        return "res-aprovado", "✅", "APROVADO", "#22c55e"
    elif media >= 4.0:
        return "res-recuperacao", "⚠️", "RECUPERAÇÃO", "#f59e0b"
    else:
        return "res-reprovado", "❌", "REPROVADO", "#ef4444"


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

# ── Nome do estudante ──
st.markdown("##### 👤 Dados do Estudante")
nome = st.text_input(
    "Nome completo",
    placeholder="Ex: João da Silva",
    key="nome_estudante"
)

st.markdown("<hr class='divisor'>", unsafe_allow_html=True)

# ── Notas ──
st.markdown("##### 📝 Notas")

notas_input = []
for i in range(st.session_state.num_notas):
    valor = st.text_input(
        f"Nota {i + 1}",
        placeholder="Ex: 7.5",
        key=f"nota_{i}"
    )
    notas_input.append(valor)

# Botão para adicionar mais notas
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
        # Limpa nome, notas e reinicia contagem
        st.session_state.pop("nome_estudante", None)
        for i in range(st.session_state.num_notas + 5):
            st.session_state.pop(f"nota_{i}", None)
        st.session_state.num_notas = 2
        st.rerun()


# ─────────────────────────────────────────
#  LÓGICA DE CÁLCULO E EXIBIÇÃO
# ─────────────────────────────────────────

if calcular:
    erros = []
    valores = []

    # Valida o nome
    erro_nome = validar_nome(nome)
    if erro_nome:
        erros.append(erro_nome)

    # Valida cada nota individualmente
    for i, entrada in enumerate(notas_input):
        valor, erro = validar_nota(entrada, i + 1)
        if erro:
            erros.append(erro)
        else:
            valores.append(valor)

    # Exibe erros encontrados
    if erros:
        for msg in erros:
            st.error(msg)

    # Se tudo válido, calcula e exibe o resultado
    elif valores:
        media = sum(valores) / len(valores)
        classe, emoji, situacao, cor = classificar_media(media)
        detalhe = "  ·  ".join([f"N{i+1}: {v:.1f}" for i, v in enumerate(valores)])
        nome_formatado = nome.strip().title()

        # Card de resultado com nome do aluno em destaque
        st.markdown(f"""
        <div class='{classe}'>
            <div class='nome-aluno'>👤 {nome_formatado}</div>
            <div class='media-num' style='color:{cor}'>{media:.2f}</div>
            <div class='situacao' style='color:{cor}'>{emoji} {situacao}</div>
            <div class='detalhe'>{detalhe}</div>
            <div class='detalhe'>{len(valores)} nota(s) considerada(s)</div>
        </div>
        """, unsafe_allow_html=True)

        # Barra de progresso
        st.markdown("<br>", unsafe_allow_html=True)
        st.progress(media / 10, text=f"{nome_formatado} · Média {media:.2f} / 10.0")


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
