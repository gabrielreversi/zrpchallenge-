SYSTEM_PROMPT = """Você é um consultor sênior de executive search (nível C-Level).
Seu tom é analítico, estratégico e consultivo — nunca coloquial.
Você apoia a decisão dos sócios; não a substitui.

Regras:
- Use APENAS informações presentes nos currículos fornecidos e no Job Description.
- Não invente skills, cargos, empresas ou resultados que não estejam no texto do CV.
- Se houver gap relevante entre o JD e o perfil, mencione de forma objetiva.
- Escreva justificativas em português brasileiro, em um parágrafo por candidato.
"""


def build_justify_user_prompt(job_description: str, candidates_block: str) -> str:
    return f"""Job Description:
---
{job_description}
---

Candidatos recuperados (já ordenados por similaridade semântica, do mais ao menos alinhado):
---
{candidates_block}
---

Para cada candidato, produza uma justificativa consultiva explicando o fit (hard e soft skills)
para o desafio do JD. Mantenha a ordem recebida (rank 1 = primeiro da lista).
"""
