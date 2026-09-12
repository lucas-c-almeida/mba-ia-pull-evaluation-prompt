# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## O que é este repositório

Desafio do MBA FullCycle ("Pull, Otimização e Avaliação de Prompts com LangChain e LangSmith"). É um boilerplate parcialmente implementado: o aluno deve completar `src/pull_prompts.py`, `src/push_prompts.py`, `tests/test_prompts.py` e criar `prompts/bug_to_user_story_v2.yml`.

Fluxo do desafio: pull do prompt ruim (`leonanluppi/bug_to_user_story_v1`) → otimizar em v2 com técnicas de prompt engineering → push público para o Hub como `{USERNAME_LANGSMITH_HUB}/bug_to_user_story_v2` → avaliar até todas as métricas ficarem >= 0.9.

**`instrucoes.md` é a especificação autoritativa.** O `README.md` é a versão anterior do enunciado e está defasado (fala em 4 métricas Tone/AC/Format/Completeness e em dataset com ≥20 exemplos). Quando houver conflito, siga `instrucoes.md`.

## Comandos

```bash
python -m venv venv && venv\Scripts\activate   # Windows; source venv/bin/activate no Linux/Mac
pip install -r requirements.txt

python src/pull_prompts.py     # pull do prompt v1 → prompts/bug_to_user_story_v1.yml
python src/push_prompts.py     # push do v2 (público) para o LangSmith Hub
python src/evaluate.py         # cria dataset no LangSmith, roda o prompt e as métricas
python src/metrics.py          # smoke test das 7 métricas (custa chamadas de LLM)

pytest tests/test_prompts.py -v
pytest tests/test_prompts.py::TestPrompts::test_prompt_has_system_prompt -v   # teste único
```

**Sempre execute a partir da raiz do repositório.** Os módulos em `src/` se importam de forma plana (`from utils import ...`), o que só funciona porque `python src/x.py` coloca `src/` no `sys.path` — `python -m src.evaluate` quebra. Além disso `evaluate.py` resolve `datasets/bug_to_user_story.jsonl` como caminho relativo ao cwd. Os testes contornam isso inserindo `src/` no `sys.path` manualmente.

## Arquitetura

**Configuração por ambiente** — copie `.env.example` para `.env`. `LLM_PROVIDER` (`openai` | `google`) decide qual classe de chat é instanciada; `LLM_MODEL` é o modelo que *responde*, `EVAL_MODEL` é o modelo *juiz*. Todo acesso a LLM passa por `utils.get_llm()` / `utils.get_eval_llm()` — não instancie `ChatOpenAI`/`ChatGoogleGenerativeAI` diretamente em código novo.

**`src/metrics.py`** — 7 avaliadores LLM-as-judge, todos com a mesma assinatura `(question|bug_report, answer|user_story, reference) -> {"score": float, ...,"reasoning": str}` e o mesmo contrato: um prompt em português pede JSON puro, `extract_json_from_response()` tolera texto em volta e qualquer exceção degrada para `score: 0.0` em vez de propagar.
- Gerais: `evaluate_f1_score` (pede precision+recall ao juiz e calcula o F1 em Python), `evaluate_clarity`, `evaluate_precision`.
- Específicas de Bug→User Story: `evaluate_tone_score`, `evaluate_acceptance_criteria_score`, `evaluate_user_story_format_score`, `evaluate_completeness_score`.

**`src/evaluate.py`** — orquestra: carrega o `.jsonl`, cria o dataset no LangSmith se não existir (reusa por nome, nunca atualiza), faz `hub.pull` do prompt v2, monta `prompt | llm`, e pontua os exemplos.

Pontos que **precisam ser ajustados** para bater com o critério de aprovação de `instrucoes.md`:
- Só chama F1/Clarity/Precision e deriva "helpfulness"/"correctness" delas; o critério exige F1 + Tone + Acceptance Criteria + User Story Format + Completeness.
- `display_results()` aprova pela **média**; o enunciado exige **cada** métrica >= 0.9.
- Avalia só `examples[:10]` — o dataset tem 15.
- `prompts_to_evaluate` usa `"bug_to_user_story_v2"` sem o prefixo de usuário; o `hub.pull` precisa de `{USERNAME_LANGSMITH_HUB}/bug_to_user_story_v2`.

**Prompts em YAML** (`prompts/*.yml`) — dicionário de topo chaveado pelo nome do prompt, com `description`, `system_prompt` (template com `{bug_report}`), `user_prompt`, `version`, `tags`. O v2 precisa adicionalmente de `techniques_applied` com **pelo menos 2 técnicas**: `utils.validate_prompt_structure()` valida exatamente isso (campos obrigatórios, `system_prompt` não vazio, ausência de `TODO`, >= 2 técnicas) e é o que `tests/test_prompts.py` consome.

**`datasets/bug_to_user_story.jsonl`** — 15 exemplos no formato `{"inputs": {"bug_report": ...}, "outputs": {"reference": ...}, "metadata": {...}}`. O `reference` define o formato-alvo da saída (user story "Como um... eu quero... para que..." + seção "Critérios de Aceitação" em Dado/Quando/Então). **Não altere este arquivo** — é a especificação da avaliação; o prompt é que deve se ajustar a ele.

## Convenções

Código, docstrings e saída de terminal em **português**. Os scripts CLI seguem o padrão: `print_section_header()` → validação de env com `check_env_vars()` → trabalho → resumo com `format_score()`, e `main()` retorna código de saída via `sys.exit(main())`.
