"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

SIMPLIFICADO: Código mais limpo e direto ao ponto.
"""

import os
import sys
from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from utils import load_yaml, check_env_vars, print_section_header, validate_prompt_structure

load_dotenv()

PROMPT_KEY = "bug_to_user_story_v2"
YAML_PATH = "prompts/bug_to_user_story_v2.yml"


def push_prompt_to_langsmith(
    prompt_name: str,
    prompt_data: dict,
    is_public: bool = True,
) -> bool:
    """
    Faz push de um prompt para o LangSmith Hub.

    Args:
        prompt_name: Nome completo do repo no Hub. Aceita "owner/prompt_name"
            ou apenas "prompt_name" (nesse caso o LangSmith resolve o dono
            automaticamente pela API key usada).
        prompt_data: Dados do prompt (mesmo formato dos arquivos YAML do projeto)
        is_public: Se o prompt deve ser publicado como público (default: True)

    Returns:
        True se sucesso, False caso contrário
    """
    system_prompt = prompt_data["system_prompt"]
    user_prompt = prompt_data.get("user_prompt", "{bug_report}")

    template = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", user_prompt),
        ]
    )

    techniques = prompt_data.get("techniques_applied", [])
    tags = list(prompt_data.get("tags", [])) + [f"technique:{t}" for t in techniques]

    description = prompt_data.get("description", "")
    if techniques:
        description = f"{description} | Técnicas aplicadas: {', '.join(techniques)}"

    try:
        url = hub.push(
            prompt_name,
            template,
            new_repo_is_public=is_public,
            new_repo_description=description,
            tags=tags,
        )
        print(f"✓ Prompt publicado em: {url}")
        return True
    except Exception as e:
        print(f"❌ Erro ao publicar prompt '{prompt_name}': {e}")
        return False


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt (reusa a validação de utils.py).

    Args:
        prompt_data: Dados do prompt

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros
    """
    return validate_prompt_structure(prompt_data)


def main():
    """Função principal"""
    print_section_header("PUSH DE PROMPT OTIMIZADO PARA O LANGSMITH HUB")

    if not check_env_vars(["LANGSMITH_API_KEY", "USERNAME_LANGSMITH_HUB"]):
        return 1

    all_prompts = load_yaml(YAML_PATH)
    if all_prompts is None:
        return 1

    prompt_data = all_prompts.get(PROMPT_KEY)
    if prompt_data is None:
        print(f"❌ Chave '{PROMPT_KEY}' não encontrada em {YAML_PATH}")
        return 1

    is_valid, errors = validate_prompt(prompt_data)
    if not is_valid:
        print("❌ Prompt inválido:")
        for error in errors:
            print(f"   - {error}")
        return 1

    username = os.getenv("USERNAME_LANGSMITH_HUB")
    repo_full_name = f"{username}/{PROMPT_KEY}"

    print(f"Publicando '{repo_full_name}' como público no LangSmith Hub...")
    if not push_prompt_to_langsmith(repo_full_name, prompt_data, is_public=True):
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
