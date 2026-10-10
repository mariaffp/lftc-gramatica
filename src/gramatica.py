EPSILON = ["&", "ε", "epsilon"]


def ler_gramatica(caminho):
    producoes = []

    with open(caminho, encoding="utf-8") as f:
        # enumerate pra saber o número da linha nas mensagens de erro
        for n, linha in enumerate(f, 1):
            linha = linha.strip()

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

            # cada linha é uma produção então o lado direito não precisa ser dividido ou processado de forma diferente
            dir_ = dir_.replace(" ", "")
            if dir_ in EPSILON:
                dir_ = ""  # epsilon guardado como texto vazio
            elif dir_ == "":
                raise ValueError(f"linha {n}: lado direito vazio (use ε ou & para epsilon)")
            producoes.append((esq, dir_))

    if len(producoes) == 0:
        raise ValueError("arquivo sem produções")

    # símbolo inicial: primeiro não terminal 
    inicial = ""
    for c in producoes[0][0]:
        if c.isupper():
            inicial = c
            break

    return producoes, inicial