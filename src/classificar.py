def nt(c):
    # True se for maiúscula
    return c.isupper()


def eh_tipo3(producoes):
    # armazena os não terminais que produzem ε
    nt_produz_epsilon = set()

    for esq, dir_ in producoes:
        # esquerda: um único não terminal
        if len(esq) != 1 or not nt(esq):
            return False
        # A -> ε
        if dir_ == "":
            nt_produz_epsilon.add(esq)
            continue
        # A -> a
        if len(dir_) == 1 and not nt(dir_):
            continue
        # A -> aB (linear à direita)
        if len(dir_) == 2 and not nt(dir_[0]) and nt(dir_[1]):
            continue
        # não encaixou em nenhum formato permitido
        return False

    for esq, dir_ in producoes:
        # A -> ε só vale se A não aparece em nenhum lado direito
        if dir_ == "" and esq in nt_produz_epsilon:
            return False
    return True


def eh_tipo2(producoes):
    # só não terminal sozinho na esquerda; a direita pode ser qualquer coisa
    for esq, dir_ in producoes:
        if len(esq) != 1 or not nt(esq):
            return False
    return True


def eh_tipo1(producoes, inicial):
    # descobre se o inicial aparece em algum lado direito
    inicial_na_direita = False
    for esq, dir_ in producoes:
        if inicial in dir_:
            inicial_na_direita = True

    for esq, dir_ in producoes:
        if dir_ == "":
            # exceção do &: só vale pro inicial, e só se ele nunca aparece à direita
            if esq != inicial or inicial_na_direita:
                return False
        elif len(esq) > len(dir_):
            # |α| <= |β|
            return False
    return True


def classificar(producoes, inicial):
    # tipo 0 vale pra toda gramática
    tipos = [0]
    # testo cada um sozinho porque, com a exceção do ε, um tipo 3 pode não ser tipo 1
    if eh_tipo1(producoes, inicial):
        tipos.append(1)
    if eh_tipo2(producoes):
        tipos.append(2)
    if eh_tipo3(producoes):
        tipos.append(3)
    return tipos