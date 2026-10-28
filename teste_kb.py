from src.kb import KnowledgeBase

# Proposicional
p = KnowledgeBase("prop")
p.tell("Pasta_Planos & Ext_PDF ==> PrioridadeAlta")
p.tell("Pasta_Planos")
p.tell("Ext_PDF")
print("PrioridadeAlta:", p.ask("PrioridadeAlta"))   # esperado: True
print("Backup:", p.ask("Backup"))                   # esperado: False

# Primeira ordem
f = KnowledgeBase("fol")
f.tell("Arquivo(Ex2)")
f.tell("Tema(Ex2, Algoritmos)")
f.tell("Tema(y, Algoritmos) ==> RevisarParaProva(y)")
print("RevisarParaProva:", f.ask("RevisarParaProva(x)"))  # esperado: [{x: Ex2}]
