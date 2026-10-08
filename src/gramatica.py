# formas aceitas de escrever epsilon no arquivo
EPSILON = ["&", "ε", "epsilon"]


def ler_gramatica(caminho):
    producoes = []

    with open(caminho, encoding="utf-8") as f:
        # enumerate só serve pra saber o número da linha nas mensagens de erro
        for n, linha in enumerate(f, 1):
            # tira o comentário (tudo depois do #) e troca → por ->
            linha = linha.split("#")[0].strip().replace("→", "->")

            # linha em branco ou só comentário: pula
            if linha == "":
                continue

            if "->" not in linha:
                raise ValueError(f"linha {n}: faltou '->'")

            # separa em lado esquerdo e lado direito
            esq, dir_ = linha.split("->", 1)
            esq = esq.replace(" ", "")

            # o lado esquerdo precisa ter pelo menos um não terminal
            tem_nt = False
            for c in esq:
                if c.isupper():
                    tem_nt = True
            if not tem_nt:
                raise ValueError(f"linha {n}: lado esquerdo sem não terminal")

            # cada alternativa separada por | vira uma produção
            for alt in dir_.split("|"):
                alt = alt.replace(" ", "")
                if alt in EPSILON:
                    alt = ""  # epsilon guardado como texto vazio
                elif alt == "":
                    raise ValueError(f"linha {n}: alternativa vazia (use ε ou & para epsilon)")
                producoes.append((esq, alt))

    if len(producoes) == 0:
        raise ValueError("arquivo sem produções")

    # símbolo inicial: primeiro não terminal da primeira regra
    inicial = ""
    for c in producoes[0][0]:
        if c.isupper():
            inicial = c
            break

    return producoes, inicial