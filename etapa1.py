from src.kb import KnowledgeBase
from src.mapeamento import varrer, popular_kb

RAIZ = "tests/docencia/fontes"

kb = KnowledgeBase("prop")
itens = varrer(RAIZ)
arquivos = popular_kb(kb, itens)

print(f"{len(arquivos)} arquivos mapeados.")
print("Arquivos com ASK(PrioridadeAlta) verdadeiro:")
for i, caminho in arquivos.items():
    if kb.ask(f"PrioridadeAlta_f{i}"):
        print("  ", caminho)
