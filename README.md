# File Hunter Agent 🔎

Agente de busca de arquivos em Python que explora diretórios, localiza arquivos pelo nome e pesquisa palavras dentro de documentos PDF. O projeto tem duas partes: na primeira, algoritmos clássicos de busca em espaço de estados; na segunda, um **agente baseado em conhecimento** que usa lógica proposicional e de primeira ordem para decidir o que abrir antes de ler qualquer arquivo.

## 📑 Sumário

1. [Visão geral](#-visão-geral)
2. [Estrutura do projeto](#-estrutura-do-projeto)
3. [Tecnologias](#️-tecnologias)
4. [Instalação](#-instalação)
5. [Como executar](#-como-executar)
6. [Parte 1: algoritmos de busca](#-parte-1-algoritmos-de-busca)
7. [Parte 2: Knowledge-Based File Hunter](#-parte-2-knowledge-based-file-hunter)
8. [Métricas e resultados](#-métricas-e-resultados)
9. [Limitações](#️-limitações)

## 🎯 Visão geral

| Parte | Abordagem | Ponto de entrada |
|---|---|---|
| 1 | Busca em espaço de estados: BFS, DFS, UCS e A* | `main.py` |
| 2 | Agente baseado em conhecimento: `TELL` / `ASK`, lógica proposicional e FOL, poda lógica | `etapa1.py`, `etapa2.py`, `etapa3.py` |

O objetivo é comparar como cada estratégia percorre os diretórios, quanto custa (tempo, memória, arquivos lidos) e o que cada uma entrega.

## 📁 Estrutura do projeto

```text
File-searcher-agent/
├── main.py                  # Parte 1: busca por nome e por conteúdo
├── etapa1.py                # Parte 2, etapa 1: lógica proposicional
├── etapa2.py                # Parte 2, etapa 2: lógica de primeira ordem
├── etapa3.py                # Parte 2, etapa 3: poda lógica e comparativo
├── teste_kb.py              # teste rápido da KnowledgeBase
├── resultado_zzqxw.txt      # exemplo de saída do comparativo (pior caso)
├── requirements.txt
├── README.md
├── .gitignore
├── src/
│   ├── buscas.py            # BFS, DFS, UCS e A* (varredura e busca por nome)
│   ├── busca_conteudo.py    # busca no conteúdo (UCS e A*) e extração de texto
│   ├── metricas.py          # medição de tempo e memória
│   ├── relatorios.py        # exibição dos resultados no terminal
│   ├── kb.py                # KnowledgeBase com tell() e ask()
│   ├── mapeamento.py        # varredura de metadados (etapa 1)
│   ├── mapeamento_fol.py    # fatos e regras de primeira ordem (etapa 2)
│   └── busca_logica.py      # BFS, poda lógica, A* lógico e medição (etapa 3)
├── vendor/                  # aima-python (clonado, não versionado)
└── tests/docencia/fontes/   # PDFs de teste (não versionados)
```

## 🛠️ Tecnologias

- Python 3
- Biblioteca padrão: `collections.deque`, `heapq`, `pathlib`, `tracemalloc`, `difflib`
- `pypdf` para extrair texto de PDF
- `aima-python` (módulo `logic`) como motor de inferência
- `networkx`, `ipython`, `matplotlib`, `sortedcontainers`, `ipywidgets` e `numpy`, exigidos pelo aima-python

## 🚀 Instalação

### 1. Clonar e criar o ambiente virtual

```bash
git clone git@github.com:yRauan/File-searcher-agent.git
cd File-searcher-agent

python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Sem chave SSH cadastrada no GitHub, use o endereço `https://github.com/yRauan/File-searcher-agent.git`.

### 2. Clonar o aima-python em `vendor/` (necessário só para a Parte 2)

O aima-python não é instalável pelo PyPI e fica fora do repositório:

```bash
git clone https://github.com/aimacode/aima-python.git vendor/aima-python
```

### 3. Colocar os documentos de teste

A pasta `tests/` não é versionada. Coloque os PDFs em:

```text
tests/docencia/fontes/<pasta de cada disciplina>/*.pdf
```

## ▶️ Como executar

```bash
python main.py                 # Parte 1
python teste_kb.py             # Parte 2: teste rápido do tell/ask
python etapa1.py               # Parte 2, etapa 1
python etapa2.py               # Parte 2, etapa 2
python etapa3.py algoritmo 5   # Parte 2, etapa 3 (comparativo)
```

Os dois argumentos do `etapa3.py` são opcionais: a **palavra-chave** (padrão `algoritmo`) e o **máximo de páginas lidas por PDF** (padrão 20). O comparativo lê PDFs de verdade e pode levar alguns minutos.

## 🔎 Parte 1: algoritmos de busca

### Varredura completa

Compara **BFS** (busca em largura, por níveis) e **DFS** (busca em profundidade, um caminho por vez). Mostra o total de arquivos encontrados, os dez primeiros, as pastas abertas, os itens examinados, o tempo e a memória.

### Busca por nome de arquivo

O usuário digita uma palavra e o programa compara quatro estratégias:

- **BFS** e **DFS**, como acima.
- **UCS** (Uniform Cost Search): busca de custo uniforme, com fila de prioridade.
- **A\***: usa o custo acumulado mais uma heurística (similaridade entre o nome da pasta e o termo) para priorizar a exploração.

### Busca dentro do conteúdo

Procura a palavra no texto dos documentos compatíveis, comparando **UCS** e **A\***. Mostra o arquivo encontrado, pastas abertas, itens examinados, arquivos lidos, bytes processados, custo, tempo e memória.

## 🧠 Parte 2: Knowledge-Based File Hunter

O agente lê só os **metadados** do sistema de arquivos, popula uma Base de Conhecimento (KB) com fatos e regras e usa `TELL` / `ASK` para decidir o que abrir.

### Base de Conhecimento (`src/kb.py`)

Classe `KnowledgeBase` com `tell(sentence)` e `ask(query)`, sobre o aima-python:

- **Modo `prop`** (lógica proposicional): `ask` retorna `True` ou `False`, por forward chaining.
- **Modo `fol`** (primeira ordem): `ask` retorna a lista de substituições das variáveis, por backward chaining.

### Etapa 1: lógica proposicional (`etapa1.py`)

Varre `tests/docencia/fontes` registrando nome, extensão e ano de modificação, sem abrir nenhum arquivo. Cada arquivo gera símbolos próprios e a regra:

```text
Pasta_<alvo> & Ext_pdf & Mod_<ano> ==> PrioridadeAlta
```

`ASK(PrioridadeAlta)` devolve os arquivos que cumprem a regra.

### Etapa 2: lógica de primeira ordem (`etapa2.py`)

Predicados `Pasta`, `Arquivo`, `Contem`, `TemaPasta`, `AutorPasta`, `Tema` e `Autor`, com regras universais que propagam tema e autor da pasta para os arquivos dentro dela, e a regra `Arquivo(y) & Tema(y, Algoritmos) & Autor(y, ProfPAA) ==> RevisarParaProva(y)`. A consulta `ASK(RevisarParaProva(?y))` retorna o caminho de cada arquivo que satisfaz a regra.

### Etapa 3: busca guiada por lógica (`etapa3.py`, `src/busca_logica.py`)

- **Poda lógica:** antes de abrir uma pasta N, o agente consulta a KB. Como a KB não tem negação, `PastaValida(N)` significa "não é possível provar `Invalida(N)`". Pastas de backup, sem acesso ou de tema irrelevante são descartadas sem listar o conteúdo.
- **Heurística derivada da KB:** `h(n)` é o número de premissas da regra do arquivo alvo (tema e autor) que a KB ainda não consegue provar para a pasta `n`.
- **Comparativo** entre três agentes: BFS (busca cega), A\* tradicional (heurística por nome, de `busca_conteudo.py`) e o agente lógico (KB com `TELL` / `ASK`).

## 📊 Métricas e resultados

Métricas: pastas abertas, arquivos lidos, falsos positivos (arquivos lidos que não continham a palavra), tempo total em ms e pico de memória em KB. Para o agente lógico também aparecem as pastas podadas, o número de `ASK` e o tempo de montagem da KB.

Resultados do `etapa3.py` com 62 PDFs e leitura limitada a 5 páginas por PDF (cada configuração foi executada uma vez):

| Palavra | Agente | Pastas | Lidos | Falsos pos. | Tempo (ms) | Pico (KB) | Achou |
|---|---|---|---|---|---|---|---|
| algoritmo | BFS | 6 | 30 | 29 | 38660 | 61215 | sim |
| algoritmo | A* (nome) | 3 | 5 | 4 | 3438 | 7524 | sim |
| algoritmo | Agente lógico | 2 | 4 | 3 | 23057 | 208033 | sim |
| mineração | BFS | 6 | 29 | 28 | 40666 | 61214 | sim |
| mineração | A* (nome) | 8 | 39 | 38 | 44781 | 50726 | sim |
| mineração | Agente lógico | 2 | 4 | 4 | 25192 | 208032 | não |
| zzqxw | BFS | 11 | 62 | 62 | 99162 | 215026 | não |
| zzqxw | A* (nome) | 11 | 62 | 62 | 103263 | 221524 | não |
| zzqxw | Agente lógico | 2 | 4 | 4 | 24934 | 208032 | não |

No pior caso (palavra inexistente), o agente lógico abre 2 pastas em vez de 11 e lê 4 PDFs em vez de 62. No melhor caso dos agentes cegos, o custo fixo do raciocínio não compensa. Com `mineração`, a poda descartou a pasta onde a palavra estava, e o agente lógico não a encontrou.

## ⚠️ Limitações

- **Tema e autor são definidos à mão.** Os dicionários `TEMAS` e `PROFESSORES` em `src/mapeamento_fol.py` dizem qual é o tema e o professor de cada pasta de primeiro nível. Hoje só `Fontes PAA` está preenchida (tema `Algoritmos`, professor `ProfPAA`); as outras pastas usam o próprio nome como tema.
- **A poda pode descartar resultados válidos.** O agente só enxerga o que a KB sabe.
- **Regras ajustáveis.** `PASTA_ALVO`, `EXT_ALVO` e `ANO_ALVO` (em `src/mapeamento.py`) e a regra `RevisarParaProva` devem ser ajustadas ao conjunto de documentos usado. Neste conjunto todos os arquivos são de 2026, então o ano não distingue nada.
- **Forward chaining em FOL.** O `fol_fc_ask` do aima não terminou em tempo viável com esta KB, por isso a Parte 2 usa backward chaining (`fol_bc_ask`).
- **Tempos.** Os valores absolutos incluem o overhead do `tracemalloc`; só a comparação relativa entre os agentes é confiável. Os custos g também diferem: o A\* tradicional usa o tamanho dos arquivos em KB e o agente lógico usa a profundidade.
- A heurística do A\* tradicional é experimental e não garante o resultado de menor custo.
- PDFs digitalizados como imagem exigem OCR para a busca por conteúdo.

## 📚 Projeto acadêmico

Projeto desenvolvido para estudar algoritmos de busca, agentes baseados em conhecimento e análise comparativa de desempenho em Python.
