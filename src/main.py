import os  # mexer com pastas e arquivos

from gramatica import ler_gramatica  # lê o arquivo e devolve as produções
from classificar import classificar  # testa os tipos 

# número do tipo relacionado ao nome, só para imprimir e deixar legal
NOMES = {
    0: "Sem restrição",
    1: "Sensível ao contexto",
    2: "Livre de contexto",
    3: "Regular",
}

# pasta exemplos/ (o r antes das aspas deixa a \ valer como barra comum)
PASTA = r"C:\Users\maria\Desktop\LFTCtrab1\lftc-gramatica\exemplos"


def analisar(caminho):
    try:  # tenta ler o arquivo
        producoes, inicial = ler_gramatica(caminho)
    except (OSError, ValueError) as e:  # arquivo não achado ou gramática mal escrita
        print(f"erro: {e}")  # mostra a mensagem em vez de quebrar o programa
        return  # sai sem classificar
    tipos = classificar(producoes, inicial)  # lista dos tipos, ex: [0, 2]
    print("Pertence aos tipos:", tipos)
    # o mais restritivo é o maior número da lista
    mais_restrito = max(tipos)  # pega o maior número da lista
    print(f"Tipo definitivo {mais_restrito} - {NOMES[mais_restrito]}")  # busca o nome no dicionário


def escolher_arquivo():
    os.makedirs(PASTA, exist_ok=True)  # cria a pasta se ela não existir
    arquivos = sorted(f for f in os.listdir(PASTA) if f.endswith(".txt"))  # só os .txt, em ordem


    if arquivos:  # verdadeiro se a lista não está vazia
        print("\nArquivos em exemplos/:")
        for i, nome in enumerate(arquivos, 1):  # numera a partir de 1
            print(f"  {i}. {nome}")
    else:
        print("\nA pasta exemplos/ está vazia.")

    # aceita o número da lista ou um caminho qualquer
    resp = input("Número ou caminho do arquivo (Enter para voltar): ").strip()  # strip tira espaços das pontas
    if not resp:  # não digitou nada
        return None  # nada escolhido, o menu volta
    if resp.isdigit() and 1 <= int(resp) <= len(arquivos):  # é um número válido da lista?
        return os.path.join(PASTA, arquivos[int(resp) - 1])  # -1 porque a lista começa na posição 0
    # procura o nome dentro de exemplos/ (com ou sem .txt)
    nome = resp if resp.endswith(".txt") else resp + ".txt"  # acrescenta .txt se faltou
    candidato = os.path.join(PASTA, nome)  # junta pasta e nome com a barra certa
    if os.path.exists(candidato):  # o arquivo existe lá dentro?
        return candidato

    return resp  # senão, trata como caminho completo


def criar_exemplo():
    nome = input("\nNome do novo arquivo (sem .txt, Enter para cancelar): ").strip()
    if not nome:  # Enter sem digitar cancela
        return None
    if not nome.endswith(".txt"):  # acrescenta .txt se faltou
        nome += ".txt"

    os.makedirs(PASTA, exist_ok=True)  # garante que a pasta existe
    caminho = os.path.join(PASTA, nome)  # caminho completo do novo arquivo

    # não deixa sobrescrever um exemplo sem confirmar
    if os.path.exists(caminho):
        if input("Esse arquivo já existe. Sobrescrever? (s/n): ").strip().lower() != "s":  # lower aceita S e s
            return None  # qualquer resposta diferente de s cancela

    print("Digite uma produção por linha (ex: S -> aSb). Linha em branco para terminar.")
    linhas = []  # aqui vão as produções digitadas
    while True:  # repete até o break
        linha = input("> ").strip()
        if not linha:  # Enter sem digitar encerra a digitação
            break
        linhas.append(linha)  # guarda a produção

    if not linhas:  # não digitou nenhuma
        print("Nada foi digitado.")
        return None

    with open(caminho, "w", encoding="utf-8") as f:  # "w" cria o arquivo (ou apaga o conteúdo antigo)
        f.write("\n".join(linhas) + "\n")  # uma produção por linha
    print(f"Salvo em {caminho}")
    return caminho  # devolve para o menu analisar na hora


def menu():
    while True:  # repete até escolher sair
        print("\n1. Escolher um arquivo")
        print("2. Criar um novo exemplo")
        print("0. Sair")
        op = input("Opção: ").strip()  # opção digitada

        if op == "0":
            break  # sai do menu
        elif op == "1":
            caminho = escolher_arquivo()  # devolve um caminho ou None
        elif op == "2":
            caminho = criar_exemplo()  # devolve um caminho ou None
        else:
            print("Opção inválida.")
            continue  # volta ao início do menu sem analisar

        if caminho:  # só analisa se escolheu ou criou algo (None conta como falso)
            analisar(caminho)


if __name__ == "__main__":  # só roda o menu se este arquivo for executado diretamente
    menu()