from collections import deque
from pathlib import Path

from src.metricas import Medidor


def buscar_todos(raiz, algoritmo="BFS"):
    raiz = Path(raiz).resolve()

    if not raiz.is_dir():
        raise NotADirectoryError(
            f"A pasta informada não existe: {raiz}"
        )

    algoritmo = algoritmo.upper()

    if algoritmo not in ("BFS", "DFS"):
        raise ValueError("O algoritmo deve ser BFS ou DFS.")

    fronteira = deque([raiz])
    arquivos = []
    pastas_abertas = 0
    itens_examinados = 0

    with Medidor() as medidor:
        while fronteira:
            if algoritmo == "BFS":
                pasta = fronteira.popleft()
            else:
                pasta = fronteira.pop()

            pastas_abertas += 1

            try:
                with __import__("os").scandir(pasta) as entradas:
                    itens = sorted(
                        entradas,
                        key=lambda entrada: entrada.name.lower()
                    )
            except OSError:
                continue

            subpastas = []

            for item in itens:
                itens_examinados += 1

                try:
                    if item.is_dir(follow_symlinks=False):
                        subpastas.append(Path(item.path))
                    elif item.is_file(follow_symlinks=False):
                        arquivos.append(
                            str(Path(item.path).relative_to(raiz))
                        )
                except OSError:
                    continue

            if algoritmo == "BFS":
                fronteira.extend(subpastas)
            else:
                fronteira.extend(reversed(subpastas))

    return {
        "algoritmo": algoritmo,
        "arquivos": arquivos,
        "primeiros_10": arquivos[:10],
        "pastas_abertas": pastas_abertas,
        "total_arquivos": len(arquivos),
        "itens_examinados": itens_examinados,
        "tempo_ms": medidor.tempo_ms,
        "memoria_kb": medidor.pico_kb,
    }
