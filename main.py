from pathlib import Path

from src.buscas import buscar_todos, buscar_por_nome


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


def main():
    projeto = Path(__file__).resolve().parent
    raiz = projeto / "tests" / "docencia" / "fontes"

    print(f"Pasta de busca: {raiz}")
    print(f"A pasta existe? {raiz.is_dir()}")

    if not raiz.is_dir():
        print("ERRO: pasta de fontes não encontrada.")
        return

    print("\n######## ETAPA 1: VARREDURA COMPLETA ########")
    for algoritmo in ("BFS", "DFS"):
        resultado = buscar_todos(raiz, algoritmo)
        exibir_resultado_completo(resultado)

    print("\n######## ETAPA 2: BUSCA POR NOME ########")
    for algoritmo in ("BFS", "DFS", "UCS", "ASTAR"):
        resultado = buscar_por_nome(raiz, "livro", algoritmo)
        exibir_busca_por_nome(resultado)


if __name__ == "__main__":
    main()
