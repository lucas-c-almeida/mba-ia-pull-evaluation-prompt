"""
Testes automatizados para validação de prompts.
"""
import pytest
import yaml
import re
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import validate_prompt_structure

PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "bug_to_user_story_v2.yml"
PROMPT_KEY = "bug_to_user_story_v2"


def load_prompts(file_path: str):
    """Carrega prompts do arquivo YAML."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


class TestPrompts:
    @pytest.fixture(autouse=True)
    def setup(self):
        """Carrega o prompt otimizado (v2) uma vez para todos os testes da classe."""
        data = load_prompts(str(PROMPT_PATH))
        self.prompt_data = data[PROMPT_KEY]
        self.system_prompt = self.prompt_data.get("system_prompt", "")

    def test_prompt_has_system_prompt(self):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        assert "system_prompt" in self.prompt_data
        assert self.system_prompt.strip() != ""

    def test_prompt_has_role_definition(self):
        """Verifica se o prompt define uma persona (ex: "Você é um Product Manager")."""
        assert re.search(r"[Vv]ocê é um[a]?\s", self.system_prompt) is not None

    def test_prompt_mentions_format(self):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        pattern = re.search(
            r"[Mm]arkdown|[Cc]omo um.*eu quero.*para que",
            self.system_prompt,
            re.DOTALL,
        )
        assert pattern is not None

    def test_prompt_has_few_shot_examples(self):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        has_example_keyword = re.search(r"[Ee]xemplo", self.system_prompt) is not None
        has_io_pair = (
            "bug" in self.system_prompt.lower()
            and "user story" in self.system_prompt.lower()
        )
        assert has_example_keyword or has_io_pair

    def test_prompt_no_todos(self):
        """Garante que você não esqueceu nenhum `[TODO]` no texto."""
        assert "[TODO]" not in self.system_prompt
        assert "TODO" not in self.system_prompt

    def test_minimum_techniques(self):
        """Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas."""
        _, errors = validate_prompt_structure(self.prompt_data)
        techniques = self.prompt_data.get("techniques_applied", [])

        assert len(techniques) >= 2
        assert not any("Mínimo de 2 técnicas" in error for error in errors)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])