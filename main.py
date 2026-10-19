
from pathlib import Path

from src.buscas import buscar_todos, buscar_por_nome
from src.busca_conteudo import buscar_conteudo


def exibir_resultado_completo(resultado):
    print(f"\n===== {resultado['algoritmo']} =====")
    print(f"Total de arquivos: {resultado['total_arquivos']}")

    print("Primeiros 10 arquivos encontrados:")
    for caminho in resultado["primeiros_10"]:
        print(f" - {caminho}")

    print(f"Pastas abertas: {resultado['pastas_abertas']}")
    print(f"Itens examinados: {resultado['itens_examinados']}")
    print(f"Tempo: {resultado['tempo_ms']:.3f} ms")
    print(f"Memória: {resultado['memoria_kb']:.2f} KB")


def exibir_busca_por_nome(resultado):
    print(f"\n===== Busca por nome: {resultado['algoritmo']} =====")
    print(f"Termo pesquisado: {resultado['alvo']}")
    print(f"Arquivo encontrado: {resultado['caminho'] or 'Nenhum'}")
    print(f"Pastas abertas: {resultado['pastas_abertas']}")
    print(f"Itens examinados: {resultado['itens_examinados']}")
    print(f"Arquivos verificados: {resultado['arquivos_verificados']}")
    print(f"Custo g: {resultado['custo_g']}")
    print(f"Custo f: {resultado['custo_f']}")
    print(f"Tempo: {resultado['tempo_ms']:.3f} ms")
    print(f"Memória: {resultado['memoria_kb']:.2f} KB")


def exibir_busca_conteudo(resultado):
    print(f"\n===== Busca no conteúdo: {resultado['algoritmo']} =====")
    print(f"Termo pesquisado: {resultado['termo']}")
    print(f"Arquivo encontrado: {resultado['caminho'] or 'Nenhum'}")
    print(f"Pastas abertas: {resultado['pastas_abertas']}")
    print(f"Itens examinados: {resultado['itens_examinados']}")
    print(f"Arquivos lidos: {resultado['arquivos_lidos']}")
    print(f"Bytes lidos: {resultado['bytes_lidos']}")
    print(f"Custo g (KB): {resultado['custo_g_kb']}")
    print(f"Prioridade final: {resultado['prioridade_final']}")
    print(f"Tempo: {resultado['tempo_ms']:.3f} ms")
    print(f"Memória: {resultado['memoria_kb']:.2f} KB")


def executar_etapa3(raiz):
    print("\n######## ETAPA 3: BUSCA NO CONTEÚDO ########")

    termo = input(
        "Digite a palavra para procurar dentro dos arquivos: "
    ).strip()

    if not termo:
        print("Termo vazio. Etapa 3 ignorada.")
        return

    for algoritmo in ("UCS", "ASTAR"):
        resultado = buscar_conteudo(
            raiz,
            termo=termo,
            algoritmo=algoritmo
        )
        exibir_busca_conteudo(resultado)


def main():
    projeto = Path(__file__).resolve().parent
    raiz = projeto / "tests" / "docencia" / "fontes"

    print(f"Pasta de busca: {raiz}")
    print(f"A pasta existe? {raiz.is_dir()}")

    if not raiz.is_dir():
        print("ERRO: pasta de fontes não encontrada.")
        return

    # ETAPA 1
    print("\n######## ETAPA 1: VARREDURA COMPLETA ########")

    for algoritmo in ("BFS", "DFS"):
        resultado = buscar_todos(raiz, algoritmo)
        exibir_resultado_completo(resultado)

    # ETAPA 2
    print("\n######## ETAPA 2: BUSCA POR NOME ########")

    nome = input(
        "Digite uma palavra do nome do arquivo que deseja buscar: "
    ).strip()

    if nome:
        for algoritmo in ("BFS", "DFS", "UCS", "ASTAR"):
            resultado = buscar_por_nome(
                raiz,
                alvo=nome,
                algoritmo=algoritmo
            )
            exibir_busca_por_nome(resultado)
    else:
        print("Termo vazio. Etapa 2 ignorada.")

    # ETAPA 3
    executar_etapa3(raiz)


if __name__ == "__main__":
    main()
