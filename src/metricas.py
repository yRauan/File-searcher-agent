import time
import tracemalloc


class Medidor:
    """Mede tempo de execução e pico de memória de uma busca."""

    def __enter__(self):
        self.inicio = time.perf_counter()
        tracemalloc.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.tempo_ms = (time.perf_counter() - self.inicio) * 1000
        _, self.pico_bytes = tracemalloc.get_traced_memory()
        self.pico_kb = self.pico_bytes / 1024
        tracemalloc.stop()
        return False
