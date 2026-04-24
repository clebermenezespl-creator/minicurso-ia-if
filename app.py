import os

# ─────────────────────────────────────────
#  UTILITÁRIOS
# ─────────────────────────────────────────

def limpar_tela():
    """Limpa o terminal em qualquer sistema operacional."""
    os.system('cls' if os.name == 'nt' else 'clear')


def cabecalho():
    """Exibe o cabeçalho do programa."""
    print("=" * 50)
    print("        🎓  CALCULADORA DE NOTAS DO IF")
    print("=" * 50)


def criterios():
    """Exibe os critérios de avaliação."""
    print()
    print("  📋 Critérios de avaliação:")
    print("  ✅  Aprovado      →  Média ≥ 6.0")
    print("  ⚠️   Recuperação  →  4.0 ≤ Média < 6.0")
    print("  ❌  Reprovado     →  Média < 4.0")
    print()


# ─────────────────────────────────────────
#  LEITURA E VALIDAÇÃO DE NOTAS
# ─────────────────────────────────────────

def ler_nota(numero):
    """
    Solicita uma nota ao usuário com validação completa.
    Aceita vírgula ou ponto como separador decimal.
    Retorna um float entre 0 e 10.
    """
    while True:
        entrada = input(f"  Nota {numero}: ").strip().replace(",", ".")

        # Validação: campo vazio
        if not entrada:
            print("  ❌ Erro: campo vazio. Digite um valor.\n")
            continue

        # Validação: valor numérico
        try:
            valor = float(entrada)
        except ValueError:
            print(f"  ❌ Erro: '{entrada}' não é um número válido. Ex: 7.5\n")
            continue

        # Validação: intervalo 0–10
        if not (0 <= valor <= 10):
            print("  ❌ Erro: a nota deve estar entre 0 e 10.\n")
            continue

        return valor


def ler_quantidade_notas():
    """
    Pergunta ao usuário quantas notas deseja inserir.
    Aceita apenas inteiros ≥ 2.
    """
    while True:
        entrada = input("  Quantas notas deseja inserir? (mínimo 2): ").strip()
        try:
            qtd = int(entrada)
            if qtd >= 2:
                return qtd
            else:
                print("  ❌ Erro: insira pelo menos 2 notas.\n")
        except ValueError:
            print(f"  ❌ Erro: '{entrada}' não é um número inteiro válido.\n")


# ─────────────────────────────────────────
#  EXIBIÇÃO DO RESULTADO
# ─────────────────────────────────────────

def barra_progresso(media):
    """Gera uma barra de progresso visual no terminal."""
    blocos = int(media)
    barra = "█" * blocos + "░" * (10 - blocos)
    return f"[{barra}] {media:.2f}/10.0"


def exibir_resultado(notas, media):
    """Exibe o resultado completo com notas, média, barra e situação."""
    print()
    print("-" * 50)
    print("              📊  RESULTADO FINAL")
    print("-" * 50)

    # Lista de notas inseridas
    for i, n in enumerate(notas, start=1):
        print(f"  Nota {i:<5}: {n:.1f}")

    print()
    print(f"  Média     : {media:.2f}")
    print(f"  Notas     : {len(notas)} inserida(s)")
    print()

    # Barra de progresso
    print(f"  {barra_progresso(media)}")
    print()

    # Situação do aluno
    if media >= 6.0:
        print("  ✅  SITUAÇÃO: APROVADO")
    elif media >= 4.0:
        print("  ⚠️   SITUAÇÃO: RECUPERAÇÃO")
    else:
        print("  ❌  SITUAÇÃO: REPROVADO")

    print("-" * 50)


# ─────────────────────────────────────────
#  FLUXO PRINCIPAL
# ─────────────────────────────────────────

def main():
    while True:
        limpar_tela()
        cabecalho()
        criterios()

        # Pergunta quantas notas o usuário quer inserir
        qtd = ler_quantidade_notas()
        print()

        # Coleta todas as notas
        notas = []
        for i in range(1, qtd + 1):
            nota = ler_nota(i)
            notas.append(nota)

        # Calcula a média aritmética simples
        media = sum(notas) / len(notas)

        # Exibe o resultado
        exibir_resultado(notas, media)

        # Pergunta se deseja calcular novamente
        print()
        opcao = input("  Deseja calcular novamente? (s/n): ").strip().lower()
        if opcao != 's':
            print()
            print("  👋 Até logo!")
            print("=" * 50)
            print()
            break


if __name__ == "__main__":
    main()
