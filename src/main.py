import os
import sys

from gramatica import ler_gramatica
from classificar import classificar

NOMES = {
    0: "Sem restrição",
    1: "Sensível ao contexto",
    2: "Livre de contexto",
    3: "Regular",
}

# pasta exemplos/
PASTA = r"C:\Users\maria\Desktop\LFTCtrab1\lftc-gramatica\exemplos"


def analisar(caminho):
    try:
        producoes, inicial = ler_gramatica(caminho)
    except (OSError, ValueError) as e:
        print(f"erro: {e}")
        return
    tipos = classificar(producoes, inicial)
    print("Pertence aos tipos:", tipos)
    # o mais restritivo é o maior número da lista
    mais_restrito = max(tipos)
    print(f"Tipo definitivo {mais_restrito} - {NOMES[mais_restrito]}")


def escolher_arquivo():
    os.makedirs(PASTA, exist_ok=True)
    arquivos = sorted(f for f in os.listdir(PASTA) if f.endswith(".txt"))


    if arquivos:
        print("\nArquivos em exemplos/:")
        for i, nome in enumerate(arquivos, 1):
            print(f"  {i}. {nome}")
    else:
        print("\nA pasta exemplos/ está vazia.")

    # aceita o número da lista ou um caminho qualquer
    resp = input("Número ou caminho do arquivo (Enter para voltar): ").strip()
    if not resp:
        return None
    if resp.isdigit() and 1 <= int(resp) <= len(arquivos):
        return os.path.join(PASTA, arquivos[int(resp) - 1])    
    # procura o nome dentro de exemplos/ (com ou sem .txt)
    nome = resp if resp.endswith(".txt") else resp + ".txt"
    candidato = os.path.join(PASTA, nome)
    if os.path.exists(candidato):
        return candidato

    return resp


def criar_exemplo():
    nome = input("\nNome do novo arquivo (sem .txt, Enter para cancelar): ").strip()
    if not nome:
        return None
    if not nome.endswith(".txt"):
        nome += ".txt"

    os.makedirs(PASTA, exist_ok=True)
    caminho = os.path.join(PASTA, nome)

    # não deixa sobrescrever um exemplo sem confirmar
    if os.path.exists(caminho):
        if input("Esse arquivo já existe. Sobrescrever? (s/n): ").strip().lower() != "s":
            return None

    print("Digite uma produção por linha (ex: S -> aSb). Linha em branco para terminar.")
    linhas = []
    while True:
        linha = input("> ").strip()
        if not linha:
            break
        linhas.append(linha)

    if not linhas:
        print("Nada foi digitado.")
        return None

    with open(caminho, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas) + "\n")
    print(f"Salvo em {caminho}")
    return caminho


def menu():
    while True:
        print("\n1. Escolher um arquivo")
        print("2. Criar um novo exemplo")
        print("0. Sair")
        op = input("Opção: ").strip()

        if op == "0":
            break
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