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

# pasta exemplos/ (varia de usuário para usuário, está no da Maria)
PASTA = r"C:\Users\maria\Desktop\LFTCtrab1\lftc-gramatica\exemplos"


def analisar(caminho):
    try:  # tenta ler o arquivo
        producoes, inicial = ler_gramatica(caminho)
    except (OSError, ValueError) as e:  
        print(f"erro: {e}")  # tratamento de erro com mensagem
        return  
    tipos = classificar(producoes, inicial)  # lista dos tipos
    print("Pertence aos tipos:", tipos)
    # o mais restritivo é o maior número da lista
    mais_restrito = max(tipos)  # pega o maior número da lista
    print(f"Tipo definitivo {mais_restrito} - {NOMES[mais_restrito]}")  # busca o nome no dicionário legal ali de cima


def escolher_arquivo():
    os.makedirs(PASTA, exist_ok=True)  # cria a pasta se ela não existir
    arquivos = sorted(f for f in os.listdir(PASTA) if f.endswith(".txt"))  # só os .txt, em ordem


    if arquivos:
        print("\nArquivos em exemplos/:")
        for i, nome in enumerate(arquivos, 1):  # numera a partir de 1
            print(f"  {i}. {nome}")
    else:
        print("\nA pasta exemplos/ está vazia.")

    # aceita o número da lista ou um caminho qualquer
    resp = input("Número ou caminho do arquivo (Enter para voltar): ").strip()  # strip tira espaços das pontas
    if not resp:  
        return None  # nada escolhido, menu volta
    if resp.isdigit() and 1 <= int(resp) <= len(arquivos):  # é um número válido da lista?
        return os.path.join(PASTA, arquivos[int(resp) - 1])  # -1 porque a lista começa na posição 0
    # procura o nome dentro de exemplos/
    nome = resp if resp.endswith(".txt") else resp + ".txt"  # acrescenta .txt se faltou
    candidato = os.path.join(PASTA, nome)  # junta pasta e nome com a barra certa
    if os.path.exists(candidato):  # o arquivo existe lá dentro?
        return candidato

    return resp 


def criar_exemplo():
    nome = input("\nNome do novo arquivo (sem .txt, Enter para cancelar): ").strip()
    if not nome:  # Enter sem digitar cancela
        return None
    if not nome.endswith(".txt"):  # acrescenta .txt se faltou
        nome += ".txt"

    os.makedirs(PASTA, exist_ok=True)  # garante a pasta existindo
    caminho = os.path.join(PASTA, nome)  # caminho completo do novo arquivo

    # não deixa sobrescrever um exemplo sem confirmar
    if os.path.exists(caminho):
        if input("Esse arquivo já existe. Sobrescrever? (s/n): ").strip().lower() != "s":  # lower aceita S e s
            return None  # qualquer resposta diferente de s cancela

    print("Digite uma produção por linha (ex: S -> aSb). Linha em branco para terminar.")
    linhas = []  # aqui as produções
    while True:
        linha = input("> ").strip()
        if not linha:  # Enter sem digitar encerra
            break
        linhas.append(linha)  # guarda produção

    if not linhas:
        print("Nada foi digitado.")
        return None

    with open(caminho, "w", encoding="utf-8") as f:  # "w" cria o arquivo (ou apaga o conteúdo antigo)
        f.write("\n".join(linhas) + "\n")  # uma produção por linha
    print(f"Salvo em {caminho}")
    return caminho  # devolve para o menu analisar


def menu():
    while True:
        print("\n1. Escolher um arquivo")
        print("2. Criar um novo exemplo")
        print("0. Sair")
        op = input("Opção: ").strip() 

        if op == "0":
            break  # sai do menu
        elif op == "1":
            caminho = escolher_arquivo()
        elif op == "2":
            caminho = criar_exemplo()
        else:
            print("Opção inválida.")
            continue  

        if caminho:
            analisar(caminho)


if __name__ == "__main__":
    menu()