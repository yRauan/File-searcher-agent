
from pathlib import Path

from src.buscas import buscar_todos


def main():
    projeto = Path(__file__).resolve().parent
    raiz = projeto / "tests" / "docencia" / "fontes"

    print(f"Pasta de busca: {raiz}")
    print(f"A pasta existe? {raiz.is_dir()}")

    if not raiz.is_dir():
        print("ERRO: pasta de fontes não encontrada.")
        return

    for algoritmo in ("BFS", "DFS"):
        resultado = buscar_todos(raiz, algoritmo)

        print(f"\n===== {algoritmo} =====")
        print(f"Total de arquivos: {resultado['total_arquivos']}")
        print("Primeiros arquivos encontrados:")

        for caminho in resultado["primeiros_10"]:
            print(f" - {caminho}")

        print(f"Pastas abertas: {resultado['pastas_abertas']}")
        print(f"Itens examinados: {resultado['itens_examinados']}")
        print(f"Tempo: {resultado['tempo_ms']:.3f} ms")
        print(f"Memória: {resultado['memoria_kb']:.2f} KB")


if __name__ == "__main__":
    main()
