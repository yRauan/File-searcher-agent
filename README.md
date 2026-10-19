# File Hunter Agent 🔎

Agente de busca de arquivos desenvolvido em Python para explorar diretórios, localizar arquivos pelo nome e pesquisar palavras dentro de documentos. O projeto compara diferentes algoritmos de busca considerando tempo de execução, memória utilizada e quantidade de elementos explorados.

## 🎯 Objetivo

Implementar e comparar estratégias de busca em sistemas de arquivos, observando como cada algoritmo percorre os diretórios e encontra resultados.

## ⚙️ Funcionalidades

### Etapa 1 — Varredura completa

Compara dois algoritmos:

- **BFS (Breadth-First Search):** busca em largura, explorando os diretórios por níveis.
- **DFS (Depth-First Search):** busca em profundidade, explorando um caminho por vez.

Apresenta o total de arquivos encontrados, os dez primeiros arquivos, as pastas abertas, os itens examinados, o tempo de execução e a memória utilizada.

### Etapa 2 — Busca por nome de arquivo

Permite que o usuário digite uma palavra para pesquisar nos nomes dos arquivos.

Compara quatro estratégias:

- **BFS:** busca em largura.
- **DFS:** busca em profundidade.
- **UCS (Uniform Cost Search):** busca de custo uniforme, utilizando uma fila de prioridade.
- **A* (A-Star):** utiliza o custo acumulado e uma heurística para definir a prioridade de exploração.

Os resultados incluem o arquivo encontrado, as pastas abertas, os itens examinados, os arquivos verificados, os custos, o tempo e a memória.

### Etapa 3 — Busca dentro do conteúdo

Permite digitar uma palavra para procurar dentro do conteúdo dos documentos compatíveis.

Compara UCS e A*, apresentando o arquivo encontrado, as pastas abertas, os itens examinados, os arquivos lidos, os bytes processados, o custo estimado, o tempo de execução e a memória utilizada.

A extração de texto de arquivos PDF é feita com a biblioteca `pypdf`.

## 🛠️ Tecnologias utilizadas

- Python 3
- `collections.deque`
- `heapq`
- `pathlib`
- `tracemalloc`
- `pypdf`
- `fontTools`

## 📁 Estrutura do projeto

```text
File_Hunter_Agent/
├── main.py
├── README.md
├── requirements.txt
├── .gitignore
├── src/
│   ├── buscas.py
│   ├── busca_conteudo.py
│   └── metricas.py
└── tests/
    └── docencia/
        └── fontes/
```

## 🚀 Como executar

### 1. Pré-requisitos

- Python 3 instalado.
- Git, caso queira clonar o repositório.

### 2. Clonar o repositório

```bash
git clone git@github.com:yRauan/File-searcher-agent.git
cd File-searcher-agent
```

Se estiver usando HTTPS ou já tiver o projeto localmente, adapte os comandos conforme necessário.

### 3. Criar o ambiente virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Instalar as dependências

```bash
python -m pip install -r requirements.txt
```

### 5. Executar

```bash
python main.py
```

O programa executa a varredura completa e, depois, solicita os termos para a busca por nome e para a busca dentro do conteúdo.

## 📊 Métricas avaliadas

- Total de arquivos encontrados.
- Pastas abertas.
- Itens examinados.
- Arquivos verificados ou lidos.
- Bytes processados na busca por conteúdo.
- Custo acumulado e prioridade de busca, conforme o algoritmo.
- Tempo de execução em milissegundos.
- Pico de memória rastreada pelo Python em KB.

## ⚠️ Observações

- Os tempos e os valores de memória variam conforme o computador e os arquivos analisados.
- A heurística do A* é experimental e não garante, na implementação atual, a obtenção do resultado de menor custo.
- A busca no conteúdo depende da capacidade de extração de texto. PDFs digitalizados como imagens podem exigir OCR.
- O conjunto de documentos utilizado nos testes deve estar no caminho esperado pelo programa: `tests/docencia/fontes`.

## 📚 Projeto acadêmico

Projeto desenvolvido para estudar algoritmos de busca, exploração de diretórios e análise comparativa de desempenho em Python.
