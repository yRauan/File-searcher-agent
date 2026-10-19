import os
import heapq
import difflib
from collections import deque
from pathlib import Path

from src.metricas import Medidor


def buscar_todos(raiz, algoritmo="BFS"):
    raiz = Path(raiz).resolve()

    if not raiz.is_dir():
        raise NotADirectoryError(f"Pasta inexistente: {raiz}")

    algoritmo = algoritmo.upper()
    if algoritmo not in ("BFS", "DFS"):
        raise ValueError("Use BFS ou DFS.")

    fronteira = deque([raiz])
    arquivos = []
    pastas_abertas = 0
    itens_examinados = 0

    with Medidor() as medidor:
        while fronteira:
            pasta = (
                fronteira.popleft()
                if algoritmo == "BFS"
                else fronteira.pop()
            )
            pastas_abertas += 1

            try:
                with os.scandir(pasta) as entradas:
                    itens = sorted(
                        list(entradas),
                        key=lambda item: item.name.lower()
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
                        relativo = Path(item.path).relative_to(raiz)
                        arquivos.append(relativo.as_posix())
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


def buscar_por_nome(raiz, alvo="livro", algoritmo="BFS"):
    raiz = Path(raiz).resolve()
    alvo = alvo.lower()
    algoritmo = algoritmo.upper()

    if not raiz.is_dir():
        raise NotADirectoryError(f"Pasta inexistente: {raiz}")

    if algoritmo not in ("BFS", "DFS", "UCS", "ASTAR"):
        raise ValueError("Use BFS, DFS, UCS ou ASTAR.")

    fronteira = deque([raiz])
    heap = []
    sequencia = 0

    if algoritmo in ("UCS", "ASTAR"):
        heapq.heappush(heap, (0, sequencia, raiz, 0))

    pastas_abertas = 0
    itens_examinados = 0
    arquivos_verificados = 0
    encontrado = None
    custo_final = None
    prioridade_final = None

    def heuristica(pasta):
        similaridade = difflib.SequenceMatcher(
            None, pasta.name.lower(), alvo
        ).ratio()
        return 1.0 - similaridade

    with Medidor() as medidor:
        while (
            bool(fronteira)
            if algoritmo in ("BFS", "DFS")
            else bool(heap)
        ):
            if algoritmo == "BFS":
                pasta = fronteira.popleft()
                custo_atual = 0
            elif algoritmo == "DFS":
                pasta = fronteira.pop()
                custo_atual = 0
            else:
                prioridade, _, pasta, custo_atual = heapq.heappop(heap)

            pastas_abertas += 1

            try:
                with os.scandir(pasta) as entradas:
                    itens = sorted(
                        list(entradas),
                        key=lambda item: item.name.lower()
                    )
            except OSError:
                continue

            itens_examinados += len(itens)
            subpastas = []

            for item in itens:
                try:
                    if item.is_file(follow_symlinks=False):
                        arquivos_verificados += 1

                        if alvo in item.name.lower():
                            encontrado = Path(item.path).relative_to(
                                raiz
                            ).as_posix()
                            custo_final = custo_atual

                            if algoritmo == "ASTAR":
                                prioridade_final = (
                                    custo_atual + heuristica(pasta)
                                )
                            elif algoritmo == "UCS":
                                prioridade_final = custo_atual
                            break

                    elif item.is_dir(follow_symlinks=False):
                        subpastas.append(Path(item.path))

                except OSError:
                    continue

            if encontrado is not None:
                break

            if algoritmo == "BFS":
                fronteira.extend(subpastas)
            elif algoritmo == "DFS":
                fronteira.extend(reversed(subpastas))
            else:
                for subpasta in subpastas:
                    try:
                        custo_aresta = len(os.listdir(subpasta))
                    except OSError:
                        continue

                    novo_custo = custo_atual + custo_aresta
                    sequencia += 1
                    h = heuristica(subpasta) if algoritmo == "ASTAR" else 0

                    heapq.heappush(
                        heap,
                        (
                            novo_custo + h,
                            sequencia,
                            subpasta,
                            novo_custo
                        )
                    )

    return {
        "algoritmo": algoritmo,
        "alvo": alvo,
        "caminho": encontrado,
        "pastas_abertas": pastas_abertas,
        "itens_examinados": itens_examinados,
        "arquivos_verificados": arquivos_verificados,
        "custo_g": custo_final,
        "custo_f": prioridade_final,
        "tempo_ms": medidor.tempo_ms,
        "memoria_kb": medidor.pico_kb,
    }
