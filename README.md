# lftc-gramatica
O projeto consiste em um programa capaz de ler uma gramática a partir de um arquivo, analisar a gramática e identificar o seu tipo.

# Tecnologias
- Python

# Objetivos do nosso trabalho

O Objetivo principal é poder receber um arquivo do tipo .txt e avaliar a gramática contida nesse arquivo, de acordo com os tipos que ela representa e o tipo mais restritivo, no caso o tipo definitivo dessa gramática. 
O nosso programa contém um pequeno Menu de opções, das quais uma delas você testar e criar um arquivo da gramática desse teste específico de uma vez. Eles ficam na pasta /exemplos do nosso programa, enquanto os códigos(incluindo a main) ficam na pasta /src


# Como a gramática de LFTC foi representada no código

- Uma produção é um par de textos: ("S", "aSb") para S -> aSb. O primeiro é o lado esquerdo e o segundo é o direito.
- A gramática é uma lista de produções: [("S", "aSb"), ("S", "")].
- Epsilon é o texto vazio "". Assim "essa produção vai para epsilon" vira dir_ == "", e o tamanho do lado direito já é 0, o que facilita a regra do tipo 1.
- Maiúscula é não terminal, o resto é terminal. Cada símbolo tem 1 caractere, então "aSb" são 3 símbolos e dá para acessar cada um por posição (dir_[0], dir_[1]).


# Estrutura

/src
/exemplos
README.md

## ARQUIVOS DE CÓDIGO

# gramatica.py:

Começa com uma lista citando as formas que a gramática digitada pode representar o epsilon

Depois há uma função que recebe o caminho do arquivo como texto e cria a lista producoes = [], onde iremos guardar os "agrupamentos" da gramática

Depois vamos abrir o arquivo para leitura. O with garante que o arquivo é fechado sozinho quando o bloco acaba. O encoding="utf-8" é necessário para o Python ler o ε e o → corretamente (sem isso, no Windows ele pode usar outra codificação e embaralhar esses caracteres). f será o nome que damos ao arquivo aberto.

Já, percorrendo o f, o enumerate(f,1) faz um contador que começa em um pra gente fazer algumas voltas e teremos n como o número da linha e "linha" o texto. O n é para identificar a linha com erro, por exemplo

 Esse código: linha = linha.split("#")[0].strip().replace("→", "->") tem 3 partes:
 - split("#") quebra o texto em pedaços sempre que acha um # e devolve uma lista. Isso é retirável, tinha colocado por causa de possíveis comentários no arquivo
- strip() tira espaços e o \n (quebra de linha) das pontas.
- replace("→", "->") troca a seta incomum pela seta de teclado, para o resto do código lidar com um formato só. ( caso precise !!!)

Se sobrou texto vazio (linha em branco ou só comentário), o continue pula para a próxima volta do for sem fazer o resto.

Se não tem seta, a linha é inválida. O ValueError  interrompe a função na hora e lança um erro com a mensagem. Quem chamou a função (o analisar, no main.py) captura isso com except e mostra a mensagem sem o programa quebrar. 

split("->", 1) quebra no -> uma única vez (o 1 limita) e devolve 2 pedaços. A atribuição esq, dir_ = ... entrega o primeiro para esq e o segundo para dir_. Usamos dir_ com underline porque dir já é uma função do Python. Depois tiramos os espaços do lado esquerdo: "C B" vira "CB".

Percorre cada caractere c do lado esquerdo. Se achar alguma maiúscula (isupper()), marca tem_nt = True. No fim, se nenhuma foi encontrada, é erro: toda produção precisa de um não terminal à esquerda até então.

O lado direito pode ter alternativas separadas por |. split("|") devolve uma lista com cada alternativa, e o for trata uma por vez, já sem espaços. (Em arquivo de uma produção por linha, só há uma alternativa e o for roda uma vez.) Isso é retirável pois não usamos muitos exemplos assim.

Se a alternativa é uma das formas de epsilon, trocamos por " " (vazio)
Se está vazia por outro motivo, é um possível erro.

Depois adiciona o agrupamento à lista de producoes. (com tupla)

Já fora do with: se o arquivo não tinha nenhuma produção, avisa.

O símbolo inicial é o primeiro não terminal da primeira regra. producoes[0] é o primeiro agrupamento e [0] dentro dela é o lado esquerdo, daí producoes[0][0]. O for procura a primeira maiúscula, guarda em inicial e o break sai do for na hora, para não pegar as seguintes.

Por fim, devolve os dois valores juntos.