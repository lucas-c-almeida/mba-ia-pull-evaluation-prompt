"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml

SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.
"""

import sys
from datetime import date
from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()

PROMPT_ID = "leonanluppi/bug_to_user_story_v1"
OUTPUT_PATH = "prompts/bug_to_user_story_v1.yml"


def _extract_system_and_user_prompt(prompt_template) -> tuple[str, str]:
    """
    Extrai o texto de system_prompt e user_prompt de um ChatPromptTemplate,
    preservando os placeholders (ex: {bug_report}).

    Args:
        prompt_template: ChatPromptTemplate retornado pelo hub.pull

    Returns:
        (system_prompt, user_prompt)
    """
    system_prompt = None
    user_prompt = None

    messages = getattr(prompt_template, "messages", [])

    for message in messages:
        template_text = getattr(getattr(message, "prompt", None), "template", None)
        if template_text is None:
            continue

        if isinstance(message, SystemMessagePromptTemplate) and system_prompt is None:
            system_prompt = template_text
        elif isinstance(message, HumanMessagePromptTemplate) and user_prompt is None:
            user_prompt = template_text

    # Fallback: prompt com uma única mensagem (sem separação System/Human)
    if system_prompt is None and messages:
        first_template = getattr(getattr(messages[0], "prompt", None), "template", None)
        system_prompt = first_template

    system_prompt = system_prompt or ""
    user_prompt = user_prompt or "{bug_report}"

    return system_prompt, user_prompt


def pull_prompts_from_langsmith():
    """
    Faz pull do prompt inicial (baixa qualidade) do LangSmith Prompt Hub.

    Returns:
        Dicionário com os dados do prompt no formato usado pelo projeto,
        ou None em caso de erro.
    """
    print(f"Puxando prompt do LangSmith Hub: {PROMPT_ID}")

    try:
        prompt_template = hub.pull(PROMPT_ID)
    except Exception as e:
        print(f"❌ Erro ao puxar prompt '{PROMPT_ID}': {e}")
        return None

    system_prompt, user_prompt = _extract_system_and_user_prompt(prompt_template)

    print("✓ Prompt carregado com sucesso")

    return {
        "bug_to_user_story_v1": {
            "description": "Prompt para converter relatos de bugs em User Stories",
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "version": "v1",
            "created_at": date.today().isoformat(),
            "tags": ["bug-analysis", "user-story", "product-management"],
        }
    }


def main():
    """Função principal"""
    print_section_header("PULL DE PROMPTS DO LANGSMITH HUB")

    if not check_env_vars(["LANGSMITH_API_KEY"]):
        return 1

    prompt_data = pull_prompts_from_langsmith()
    if prompt_data is None:
        return 1

    if not save_yaml(prompt_data, OUTPUT_PATH):
        return 1

    print(f"✓ Prompt salvo em {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
