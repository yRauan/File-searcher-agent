from src.kb import KnowledgeBase
from src.mapeamento_fol import popular_kb_fol

RAIZ = "tests/docencia/fontes"

kb = KnowledgeBase("fol")
caminhos = popular_kb_fol(kb, RAIZ)

print("ASK(RevisarParaProva(?y)):")
for binding in kb.ask("RevisarParaProva(y)"):
    for var, valor in binding.items():
        print(f"  ?{var} = {caminhos[str(valor)]}")
