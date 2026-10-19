import os
import heapq
import difflib
import time
import tracemalloc
from pathlib import Path

from pypdf import PdfReader


EXTENSOES_TEXTO = {
    ".txt", ".md", ".csv", ".py", ".json",
    ".xml", ".html", ".css", ".js"
}


def extrair_texto(arquivo):
    caminho = Path(arquivo)

    try:
        if caminho.suffix.lower() == ".pdf":
            leitor = PdfReader(str(caminho))
            return "\n".join(
                pagina.extract_text() or ""
                for pagina in leitor.pages
            )

        if caminho.suffix.lower() in EXTENSOES_TEXTO:
            return caminho.read_text(
                encoding="utf-8", errors="ignore"
            )
    except Exception:
        return ""

    return ""


def buscar_conteudo(raiz, termo="algoritmo", algoritmo="UCS"):
    raiz = Path(raiz).resolve()
    termo = termo.casefold()
    algoritmo = algoritmo.upper()

    if not raiz.is_dir():
        raise NotADirectoryError(f"Pasta inexistente: {raiz}")

    if algoritmo not in ("UCS", "ASTAR"):
        raise ValueError("Use UCS ou ASTAR.")

    def custo_pasta(pasta):
        """Estimativa do tamanho dos arquivos diretamente na pasta, em KB."""
        total = 0
        try:
            with os.scandir(pasta) as entradas:
                for entrada in entradas:
                    try:
                        if entrada.is_file(follow_symlinks=False):
                            total += entrada.stat(
                                follow_symlinks=False
                            ).st_size
                    except OSError:
                        continue
        except OSError:
            pass

        return total / 1024

    def heuristica(pasta):
        """Distância experimental entre o nome da pasta e o termo."""
        similaridade = difflib.SequenceMatcher(
            None, pasta.name.casefold(), termo
        ).ratio()
        return (1.0 - similaridade) * 100

    sequencia = 0
    fronteira = [(0.0, sequencia, raiz, 0.0)]
    pastas_abertas = 0
    itens_examinados = 0
    arquivos_lidos = 0
    bytes_lidos = 0
    encontrado = None
    custo_final = None
    prioridade_final = None

    tracemalloc.start()
    inicio = time.perf_counter()

    try:
        while fronteira:
            prioridade, _, pasta, custo_atual = heapq.heappop(
                fronteira
            )
            pastas_abertas += 1

            try:
                with os.scandir(pasta) as entradas:
                    itens = sorted(
                        list(entradas),
                        key=lambda item: item.name.casefold()
                    )
            except OSError:
                continue

            itens_examinados += len(itens)
            subpastas = []

            for item in itens:
                try:
                    if item.is_dir(follow_symlinks=False):
                        subpastas.append(Path(item.path))

                    elif item.is_file(follow_symlinks=False):
                        caminho = Path(item.path)
                        extensao = caminho.suffix.lower()

                        if (
                            extensao != ".pdf"
                            and extensao not in EXTENSOES_TEXTO
                        ):
                            continue

                        try:
                            tamanho = caminho.stat().st_size
                            texto = extrair_texto(caminho)
                        except OSError:
                            continue

                        arquivos_lidos += 1
                        bytes_lidos += tamanho

                        if termo in texto.casefold():
                            encontrado = caminho.relative_to(
                                raiz
                            ).as_posix()
                            custo_final = custo_atual
                            prioridade_final = prioridade
                            break

                except OSError:
                    continue

            if encontrado is not None:
                break

            for subpasta in subpastas:
                novo_custo = custo_atual + custo_pasta(subpasta)
                sequencia += 1
                h = (
                    heuristica(subpasta)
                    if algoritmo == "ASTAR"
                    else 0.0
                )

                heapq.heappush(
                    fronteira,
                    (
                        novo_custo + h,
                        sequencia,
                        subpasta,
                        novo_custo
                    )
                )

    finally:
        tempo_ms = (time.perf_counter() - inicio) * 1000
        _, pico_bytes = tracemalloc.get_traced_memory()
        tracemalloc.stop()

    return {
        "algoritmo": algoritmo,
        "termo": termo,
        "caminho": encontrado,
        "pastas_abertas": pastas_abertas,
        "itens_examinados": itens_examinados,
        "arquivos_lidos": arquivos_lidos,
        "bytes_lidos": bytes_lidos,
        "custo_g_kb": custo_final,
        "prioridade_final": prioridade_final,
        "tempo_ms": tempo_ms,
        "memoria_kb": pico_bytes / 1024,
    }
