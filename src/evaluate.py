"""
Script COMPLETO para avaliar prompts otimizados.

Este script:
1. Carrega dataset de avaliação de arquivo .jsonl (datasets/bug_to_user_story.jsonl)
2. Cria/atualiza dataset no LangSmith
3. Puxa prompts otimizados do LangSmith Hub (fonte única de verdade)
4. Executa prompts contra o dataset
5. Calcula 5 métricas (Helpfulness, Correctness, F1-Score, Clarity, Precision)
6. Publica resultados no dashboard do LangSmith
7. Exibe resumo no terminal

Suporta múltiplos providers de LLM:
- OpenAI (gpt-4o, gpt-4o-mini)
- Google Gemini (gemini-1.5-flash, gemini-1.5-pro)

Configure o provider no arquivo .env através da variável LLM_PROVIDER.
"""

import os
import sys
import json
import time
from typing import List, Dict, Any
from pathlib import Path
from dotenv import load_dotenv
from langsmith import Client
from langsmith.evaluation import evaluate as ls_evaluate
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from utils import check_env_vars, format_score, print_section_header, get_llm as get_configured_llm
from metrics import (
    evaluate_f1_score,
    evaluate_tone_score,
    evaluate_acceptance_criteria_score,
    evaluate_user_story_format_score,
    evaluate_completeness_score,
)

load_dotenv()

# Pausa entre chamadas de LLM para respeitar a cota gratuita do Gemini
# (free tier: 15 requisições/minuto por modelo). Cada exemplo faz 1 chamada de
# geração + 5 chamadas de avaliação (LLM-as-judge), então sem essa pausa uma
# rodada completa (15 exemplos = 90 chamadas) estoura a cota e falha em silêncio.
EVAL_CALL_DELAY_SECONDS = float(os.getenv("EVAL_CALL_DELAY_SECONDS", "4.5"))


def get_llm():
    return get_configured_llm(temperature=0)


def load_dataset_from_jsonl(jsonl_path: str) -> List[Dict[str, Any]]:
    examples = []

    try:
        with open(jsonl_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:  # Ignorar linhas vazias
                    example = json.loads(line)
                    examples.append(example)

        return examples

    except FileNotFoundError:
        print(f"❌ Arquivo não encontrado: {jsonl_path}")
        print("\nCertifique-se de que o arquivo datasets/bug_to_user_story.jsonl existe.")
        return []
    except json.JSONDecodeError as e:
        print(f"❌ Erro ao parsear JSONL: {e}")
        return []
    except Exception as e:
        print(f"❌ Erro ao carregar dataset: {e}")
        return []


def create_evaluation_dataset(client: Client, dataset_name: str, jsonl_path: str) -> str:
    print(f"Criando dataset de avaliação: {dataset_name}...")

    examples = load_dataset_from_jsonl(jsonl_path)

    if not examples:
        print("❌ Nenhum exemplo carregado do arquivo .jsonl")
        return dataset_name

    print(f"   ✓ Carregados {len(examples)} exemplos do arquivo {jsonl_path}")

    try:
        datasets = client.list_datasets(dataset_name=dataset_name)
        existing_dataset = None

        for ds in datasets:
            if ds.name == dataset_name:
                existing_dataset = ds
                break

        if existing_dataset:
            print(f"   ✓ Dataset '{dataset_name}' já existe, usando existente")
            return dataset_name
        else:
            dataset = client.create_dataset(dataset_name=dataset_name)

            for example in examples:
                client.create_example(
                    dataset_id=dataset.id,
                    inputs=example["inputs"],
                    outputs=example["outputs"]
                )

            print(f"   ✓ Dataset criado com {len(examples)} exemplos")
            return dataset_name

    except Exception as e:
        print(f"   ⚠️  Erro ao criar dataset: {e}")
        return dataset_name


def pull_prompt_from_langsmith(prompt_name: str) -> ChatPromptTemplate:
    try:
        print(f"   Puxando prompt do LangSmith Hub: {prompt_name}")
        prompt = hub.pull(prompt_name)
        print(f"   ✓ Prompt carregado com sucesso")
        return prompt

    except Exception as e:
        error_msg = str(e).lower()

        print(f"\n{'=' * 70}")
        print(f"❌ ERRO: Não foi possível carregar o prompt '{prompt_name}'")
        print(f"{'=' * 70}\n")

        if "not found" in error_msg or "404" in error_msg:
            print("⚠️  O prompt não foi encontrado no LangSmith Hub.\n")
            print("AÇÕES NECESSÁRIAS:")
            print("1. Verifique se você já fez push do prompt otimizado:")
            print(f"   python src/push_prompts.py")
            print()
            print("2. Confirme se o prompt foi publicado com sucesso em:")
            print(f"   https://smith.langchain.com/prompts")
            print()
            print(f"3. Certifique-se de que o nome do prompt está correto: '{prompt_name}'")
            print()
            print("4. Se você alterou o prompt no YAML, refaça o push:")
            print(f"   python src/push_prompts.py")
        else:
            print(f"Erro técnico: {e}\n")
            print("Verifique:")
            print("- LANGSMITH_API_KEY está configurada corretamente no .env")
            print("- Você tem acesso ao workspace do LangSmith")
            print("- Sua conexão com a internet está funcionando")

        print(f"\n{'=' * 70}\n")
        raise


METRIC_LABELS = {
    "f1_score": "F1-Score",
    "tone_score": "Tone Score",
    "acceptance_criteria_score": "Acceptance Criteria Score",
    "user_story_format_score": "User Story Format Score",
    "completeness_score": "Completeness Score",
}


def _build_target(chain):
    """
    Constrói a função `target` exigida por `langsmith.evaluation.evaluate()`:
    recebe `example.inputs` (nunca a referência) e retorna um dict.
    """
    def predict(inputs: dict) -> dict:
        response = chain.invoke(inputs)
        time.sleep(EVAL_CALL_DELAY_SECONDS)
        return {"answer": response.content}

    return predict


def _make_evaluator(key: str, metric_fn, question_field: str = "bug_report"):
    """
    Embrulha uma função de métrica de metrics.py no formato de evaluator
    esperado por `evaluate()`: `(inputs, outputs, reference_outputs) -> dict`.
    `outputs` é o que o `target` retornou; `reference_outputs` é `example.outputs`.
    """
    def evaluator(inputs: dict, outputs: dict, reference_outputs: dict) -> dict:
        result = metric_fn(
            inputs.get(question_field, ""),
            outputs.get("answer", ""),
            reference_outputs.get("reference", ""),
        )
        time.sleep(EVAL_CALL_DELAY_SECONDS)
        return {"key": key, "score": result["score"], "comment": result["reasoning"]}

    evaluator.__name__ = key
    return evaluator


EVALUATORS = [
    _make_evaluator("f1_score", evaluate_f1_score),
    _make_evaluator("tone_score", evaluate_tone_score),
    _make_evaluator("acceptance_criteria_score", evaluate_acceptance_criteria_score),
    _make_evaluator("user_story_format_score", evaluate_user_story_format_score),
    _make_evaluator("completeness_score", evaluate_completeness_score),
]


def run_experiment(
    prompt_name: str,
    dataset_name: str,
    client: Client
) -> Dict[str, float]:
    """
    Avalia um prompt do LangSmith Hub contra o dataset usando
    `langsmith.evaluation.evaluate()`. Isso cria um Experiment vinculado ao
    dataset (visível na aba "Experiments" do LangSmith), em vez de apenas
    traces soltos, permitindo comparar visualmente as execuções de v1 e v2.
    """
    print(f"\n🔍 Avaliando: {prompt_name}")

    try:
        prompt_template = pull_prompt_from_langsmith(prompt_name)
        llm = get_llm()
        chain = prompt_template | llm

        experiment_prefix = prompt_name.replace("/", "-")

        results = ls_evaluate(
            _build_target(chain),
            data=dataset_name,
            evaluators=EVALUATORS,
            experiment_prefix=experiment_prefix,
            client=client,
            # 0 = sem concorrência (sequencial) — respeita a cota gratuita do
            # Gemini (15 req/min) junto com EVAL_CALL_DELAY_SECONDS.
            max_concurrency=0,
        )

        print(f"   🔗 Experiment: {results.url}")

        scores: Dict[str, list] = {key: [] for key in METRIC_LABELS}

        for row in results:
            eval_results = row["evaluation_results"]["results"]
            for eval_result in eval_results:
                key = getattr(eval_result, "key", None)
                if key is None and isinstance(eval_result, dict):
                    key = eval_result.get("key")

                score = getattr(eval_result, "score", None)
                if score is None and isinstance(eval_result, dict):
                    score = eval_result.get("score")

                if key in scores and score is not None:
                    scores[key].append(score)

        def _avg(values):
            return round(sum(values) / len(values), 4) if values else 0.0

        return {key: _avg(values) for key, values in scores.items()}

    except Exception as e:
        print(f"   ❌ Erro na avaliação: {e}")
        return {key: 0.0 for key in METRIC_LABELS}


def display_results(prompt_name: str, scores: Dict[str, float]) -> bool:
    print("\n" + "=" * 50)
    print(f"Prompt: {prompt_name}")
    print("=" * 50)

    print("\nMétricas:")
    for key, label in METRIC_LABELS.items():
        print(f"  - {label}: {format_score(scores[key], threshold=0.9)}")

    average_score = sum(scores.values()) / len(scores)

    print("\n" + "-" * 50)
    print(f"📊 MÉDIA GERAL: {average_score:.4f}")
    print("-" * 50)

    # Critério de aprovação: TODAS as métricas devem ser >= 0.9, não apenas a média
    passed = all(value >= 0.9 for value in scores.values())

    if passed:
        print(f"\n✅ STATUS: APROVADO - Todas as métricas atingiram o mínimo de 0.9")
    else:
        print(f"\n❌ STATUS: FALHOU - Métricas abaixo do mínimo de 0.9")
        for key, label in METRIC_LABELS.items():
            if scores[key] < 0.9:
                print(f"   ⚠️  {label} abaixo do mínimo: {scores[key]:.4f}")

    return passed


def main():
    print_section_header("AVALIAÇÃO DE PROMPTS OTIMIZADOS")

    provider = os.getenv("LLM_PROVIDER", "openai")
    llm_model = os.getenv("LLM_MODEL", "gpt-4o-mini")
    eval_model = os.getenv("EVAL_MODEL", "gpt-4o")

    print(f"Provider: {provider}")
    print(f"Modelo Principal: {llm_model}")
    print(f"Modelo de Avaliação: {eval_model}\n")

    required_vars = ["LANGSMITH_API_KEY", "LLM_PROVIDER", "USERNAME_LANGSMITH_HUB"]
    if provider == "openai":
        required_vars.append("OPENAI_API_KEY")
    elif provider in ["google", "gemini"]:
        required_vars.append("GOOGLE_API_KEY")

    if not check_env_vars(required_vars):
        return 1

    client = Client()
    project_name = os.getenv("LANGSMITH_PROJECT", "prompt-optimization-challenge-resolved")

    jsonl_path = "datasets/bug_to_user_story.jsonl"

    if not Path(jsonl_path).exists():
        print(f"❌ Arquivo de dataset não encontrado: {jsonl_path}")
        print("\nCertifique-se de que o arquivo existe antes de continuar.")
        return 1

    dataset_name = f"{project_name}-eval"
    create_evaluation_dataset(client, dataset_name, jsonl_path)

    print("\n" + "=" * 70)
    print("PROMPTS PARA AVALIAR")
    print("=" * 70)
    print("\nEste script irá puxar prompts do LangSmith Hub.")
    print("Certifique-se de ter feito push dos prompts antes de avaliar:")
    print("  python src/push_prompts.py\n")

    username = os.getenv("USERNAME_LANGSMITH_HUB")
    prompts_to_evaluate = [
        f"{username}/bug_to_user_story_v2",
    ]

    # Passe --with-v1 para também avaliar o prompt original (ruim), gerando no
    # LangSmith as execuções "antes" usadas como evidência comparativa no README.
    if "--with-v1" in sys.argv:
        prompts_to_evaluate.insert(0, "leonanluppi/bug_to_user_story_v1")

    all_passed = True
    evaluated_count = 0
    results_summary = []

    for prompt_name in prompts_to_evaluate:
        evaluated_count += 1

        try:
            scores = run_experiment(prompt_name, dataset_name, client)

            passed = display_results(prompt_name, scores)
            all_passed = all_passed and passed

            results_summary.append({
                "prompt": prompt_name,
                "scores": scores,
                "passed": passed
            })

        except Exception as e:
            print(f"\n❌ Falha ao avaliar '{prompt_name}': {e}")
            all_passed = False

            results_summary.append({
                "prompt": prompt_name,
                "scores": {key: 0.0 for key in METRIC_LABELS},
                "passed": False
            })

    print("\n" + "=" * 50)
    print("RESUMO FINAL")
    print("=" * 50 + "\n")

    if evaluated_count == 0:
        print("⚠️  Nenhum prompt foi avaliado")
        return 1

    print(f"Prompts avaliados: {evaluated_count}")
    print(f"Aprovados: {sum(1 for r in results_summary if r['passed'])}")
    print(f"Reprovados: {sum(1 for r in results_summary if not r['passed'])}\n")

    if all_passed:
        print("✅ Todos os prompts atingiram >= 0.9 em TODAS as métricas!")
        print(f"\n✓ Confira os resultados em:")
        print(f"  https://smith.langchain.com/projects/{project_name}")
        print("\nPróximos passos:")
        print("1. Documente o processo no README.md")
        print("2. Capture screenshots das avaliações")
        print("3. Faça commit e push para o GitHub")
        return 0
    else:
        print("⚠️  Alguns prompts não atingiram 0.9 em todas as métricas")
        print("\nPróximos passos:")
        print("1. Refatore os prompts com score baixo")
        print("2. Faça push novamente: python src/push_prompts.py")
        print("3. Execute: python src/evaluate.py novamente")
        return 1

if __name__ == "__main__":
    sys.exit(main())
