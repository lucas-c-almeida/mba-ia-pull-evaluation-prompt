# Pull, Otimização e Avaliação de Prompts com LangChain e LangSmith

## Objetivo

Você deve entregar um software capaz de:

1. **Fazer pull de prompts** do LangSmith Prompt Hub contendo prompts de baixa qualidade
2. **Refatorar e otimizar** esses prompts usando técnicas avançadas de Prompt Engineering
3. **Fazer push dos prompts otimizados** de volta ao LangSmith
4. **Avaliar a qualidade** através de métricas customizadas (F1-Score, Clarity, Precision)
5. **Atingir pontuação mínima** de 0.9 (90%) em todas as métricas de avaliação

---

## Exemplo no CLI

```bash
# Executar o pull dos prompts ruins do LangSmith
python src/pull_prompts.py

# Executar avaliação inicial (prompts ruins)
python src/evaluate.py

Executando avaliação dos prompts...
================================
Prompt: support_bot_v1a
- Helpfulness: 0.45
- Correctness: 0.52
- F1-Score: 0.48
- Clarity: 0.50
- Precision: 0.46
================================
Status: FALHOU - Métricas abaixo do mínimo de 0.9

# Após refatorar os prompts e fazer push
python src/push_prompts.py

# Executar avaliação final (prompts otimizados)
python src/evaluate.py

Executando avaliação dos prompts...
================================
Prompt: support_bot_v2_optimized
- Helpfulness: 0.94
- Correctness: 0.96
- F1-Score: 0.93
- Clarity: 0.95
- Precision: 0.92
================================
Status: APROVADO ✓ - Todas as métricas atingiram o mínimo de 0.9
```
---

## Tecnologias obrigatórias

- **Linguagem:** Python 3.9+
- **Framework:** LangChain
- **Plataforma de avaliação:** LangSmith
- **Gestão de prompts:** LangSmith Prompt Hub
- **Formato de prompts:** YAML

---

## Pacotes recomendados

```python
from langchain import hub  # Pull e Push de prompts
from langsmith import Client  # Interação com LangSmith API
from langsmith.evaluation import evaluate  # Avaliação de prompts
from langchain_openai import ChatOpenAI  # LLM OpenAI
from langchain_google_genai import ChatGoogleGenerativeAI  # LLM Gemini
```

---

## OpenAI

- Crie uma **API Key** da OpenAI: https://platform.openai.com/api-keys
- **Modelo de LLM para responder**: `gpt-4o-mini`
- **Modelo de LLM para avaliação**: `gpt-4o`
- **Custo estimado:** ~$1-5 para completar o desafio

## Gemini (modelo free)

- Crie uma **API Key** da Google: https://aistudio.google.com/app/apikey
- **Modelo de LLM para responder**: `gemini-2.5-flash`
- **Modelo de LLM para avaliação**: `gemini-2.5-flash`
- **Limite:** 15 req/min, 1500 req/dia

---

## Requisitos

### 1. Pull dos Prompt inicial do LangSmith

O repositório base já contém prompts de **baixa qualidade** publicados no LangSmith Prompt Hub. Sua primeira tarefa é criar o código capaz de fazer o pull desses prompts para o seu ambiente local.

**Tarefas:**

1. Configurar suas credenciais do LangSmith no arquivo `.env` (conforme instruções no `README.md` do repositório base)
2. Acessar o script `src/pull_prompts.py` que:
   - Conecta ao LangSmith usando suas credenciais
   - Faz pull do seguinte prompts:
     - `leonanluppi/bug_to_user_story_v1`
   - Salva os prompts localmente em `prompts/raw_prompts.yml`

---

### 2. Otimização do Prompt

Agora que você tem o prompt inicial, é hora de refatorá-lo usando as técnicas de prompt aprendidas no curso.

**Tarefas:**

1. Analisar o prompt em `prompts/bug_to_user_story_v1.yml`
2. Criar um novo arquivo `prompts/bug_to_user_story_v2.yml` com suas versões otimizadas
3. Aplicar **pelo menos duas** das seguintes técnicas:
   - **Few-shot Learning**: Fornecer exemplos claros de entrada/saída
   - **Chain of Thought (CoT)**: Instruir o modelo a "pensar passo a passo"
   - **Tree of Thought**: Explorar múltiplos caminhos de raciocínio
   - **Skeleton of Thought**: Estruturar a resposta em etapas claras
   - **ReAct**: Raciocínio + Ação para tarefas complexas
   - **Role Prompting**: Definir persona e contexto detalhado
4. Documentar no `README.md` quais técnicas você escolheu e por quê

**Requisitos do prompt otimizado:**

- Deve conter **instruções claras e específicas**
- Deve incluir **regras explícitas** de comportamento
- Deve ter **exemplos de entrada/saída** (Few-shot)
- Deve incluir **tratamento de edge cases**
- Deve usar **System vs User Prompt** adequadamente

---

### 3. Push e Avaliação

Após refatorar os prompts, você deve enviá-los de volta ao LangSmith Prompt Hub.

**Tarefas:**

1. Criar o script `src/push_prompts.py` que:
   - Lê os prompts otimizados de `prompts/bug_to_user_story_v2.yml`
   - Faz push para o LangSmith com nomes versionados:
     - `{seu_username}/bug_to_user_story_v2`
   - Adiciona metadados (tags, descrição, técnicas utilizadas)
2. Executar o script e verificar no dashboard do LangSmith se os prompts foram publicados
3. Deixa-lo público

---

### 4. Iteração

- Espera-se 3-5 iterações.
- Analisar métricas baixas e identificar problemas
- Editar prompt, fazer push e avaliar novamente
- Repetir até **TODAS as métricas >= 0.9**

### Critério de Aprovação:

```
- Tone Score >= 0.9
- Acceptance Criteria Score >= 0.9
- User Story Format Score >= 0.9
- Completeness Score >= 0.9

MÉDIA das 4 métricas >= 0.9
```

**IMPORTANTE:** TODAS as 4 métricas devem estar >= 0.9, não apenas a média!

### 5. Testes de Validação

**O que você deve fazer:** Edite o arquivo `tests/test_prompts.py` e implemente, no mínimo, os 6 testes abaixo usando `pytest`:

- `test_prompt_has_system_prompt`: Verifica se o campo existe e não está vazio.
- `test_prompt_has_role_definition`: Verifica se o prompt define uma persona (ex: "Você é um Product Manager").
- `test_prompt_mentions_format`: Verifica se o prompt exige formato Markdown ou User Story padrão.
- `test_prompt_has_few_shot_examples`: Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot).
- `test_prompt_no_todos`: Garante que você não esqueceu nenhum `[TODO]` no texto.
- `test_minimum_techniques`: Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas.

**Como validar:**

```bash
pytest tests/test_prompts.py
```

---

## Estrutura obrigatória do projeto

Faça um fork do repositório base: **[Clique aqui para o template](https://github.com/devfullcycle/mba-ia-pull-evaluation-prompt)**

```
desafio-prompt-engineer/
├── .env.example              # Template das variáveis de ambiente
├── requirements.txt          # Dependências Python
├── README.md                 # Sua documentação do processo
│
├── prompts/
│   ├── bug_to_user_story_v1.yml       # Prompt inicial (após pull)
│   └── bug_to_user_story_v2.yml # Seu prompt otimizado
│
├── src/
│   ├── pull_prompts.py       # Pull do LangSmith
│   ├── push_prompts.py       # Push ao LangSmith
│   ├── evaluate.py           # Avaliação automática
│   ├── metrics.py            # 4 métricas implementadas
│   ├── dataset.py            # 15 exemplos de bugs
│   └── utils.py              # Funções auxiliares
│
├── tests/
│   └── test_prompts.py       # Testes de validação
│
```

**O que você vai criar:**

- `prompts/bug_to_user_story_v2.yml` - Seu prompt otimizado
- `tests/test_prompts.py` - Seus testes de validação
- `src/pull_prompt.py` Script de pull do repositório da fullcycle
- `src/push_prompt.py` Script de push para o seu repositório
- `README.md` - Documentação do seu processo de otimização

**O que já vem pronto:**

- Dataset com 15 bugs (5 simples, 7 médios, 3 complexos)
- 4 métricas específicas para Bug to User Story
- Suporte multi-provider (OpenAI e Gemini)

## Repositórios úteis

- [Repositório boilerplate do desafio](https://github.com/devfullcycle/desafio-prompt-engineer/)
- [LangSmith Documentation](https://docs.smith.langchain.com/)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)

## VirtualEnv para Python

Crie e ative um ambiente virtual antes de instalar dependências:

```bash
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## Ordem de execução

### 1. Executar pull dos prompts ruins

```bash
python src/pull_prompts.py
```

### 2. Refatorar prompts

Edite manualmente o arquivo `prompts/bug_to_user_story_v2.yml` aplicando as técnicas aprendidas no curso.

### 3. Fazer push dos prompts otimizados

```bash
python src/push_prompts.py
```

### 5. Executar avaliação

```bash
python src/evaluate.py
```

---

## Entregável

1. **Repositório público no GitHub** (fork do repositório base) contendo:

   - Todo o código-fonte implementado
   - Arquivo `prompts/bug_to_user_story_v2.yml` 100% preenchido e funcional
   - Arquivo `README.md` atualizado com:

2. **README.md deve conter:**

   A) **Seção "Técnicas Aplicadas (Fase 2)"**:

   - Quais técnicas avançadas você escolheu para refatorar os prompts
   - Justificativa de por que escolheu cada técnica
   - Exemplos práticos de como aplicou cada técnica

   B) **Seção "Resultados Finais"**:

   - Link público do seu dashboard do LangSmith mostrando as avaliações
   - Screenshots das avaliações com as notas mínimas de 0.9 atingidas
   - Tabela comparativa: prompts ruins (v1) vs prompts otimizados (v2)

   C) **Seção "Como Executar"**:

   - Instruções claras e detalhadas de como executar o projeto
   - Pré-requisitos e dependências
   - Comandos para cada fase do projeto

3. **Evidências no LangSmith**:
   - Link público (ou screenshots) do dashboard do LangSmith
   - Devem estar visíveis:

     - Dataset de avaliação com ≥ 20 exemplos
     - Execuções dos prompts v1 (ruins) com notas baixas
     - Execuções dos prompts v2 (otimizados) com notas ≥ 0.9
     - Tracing detalhado de pelo menos 3 exemplos

---

## Dicas Finais

- **Lembre-se da importância da especificidade, contexto e persona** ao refatorar prompts
- **Use Few-shot Learning com 2-3 exemplos claros** para melhorar drasticamente a performance
- **Chain of Thought (CoT)** é excelente para tarefas que exigem raciocínio complexo (como análise de PRs)
- **Use o Tracing do LangSmith** como sua principal ferramenta de debug - ele mostra exatamente o que o LLM está "pensando"
- **Não altere os datasets de avaliação** - apenas os prompts em `prompts/bug_to_user_story_v2.yml`
- **Itere, itere, itere** - é normal precisar de 3-5 iterações para atingir 0.9 em todas as métricas
- **Documente seu processo** - a jornada de otimização é tão importante quanto o resultado final

---

# Documentação do Processo (Lucas Almeida)

> As seções abaixo documentam a execução real deste desafio neste repositório. As seções acima são o enunciado original do desafio (mantidas como referência).

## Técnicas Aplicadas (Fase 2)

O prompt otimizado está em [`prompts/bug_to_user_story_v2.yml`](prompts/bug_to_user_story_v2.yml). Foram aplicadas 3 técnicas (mínimo exigido: 2):

| Técnica | Por que foi escolhida | Como foi aplicada | Métrica que mais beneficia |
|---|---|---|---|
| **Role Prompting** | O prompt v1 não define nenhuma persona, o que resulta em tom genérico/neutro. Fixar uma persona de PM sênior empático puxa diretamente o tom das respostas. | `system_prompt` abre com: *"Você é um Product Manager (PM) sênior, especialista em metodologias ágeis (Scrum/Kanban), com grande empatia pelo usuário final e foco constante em valor de negócio."* | Tone Score |
| **Few-shot Learning** | Instruções descritivas sozinhas não garantem que o modelo reproduza o formato exato exigido (User Story + Critérios de Aceitação em Given/When/Then). Exemplos completos calibram o modelo a copiar o padrão. | 2 exemplos completos e inventados (não retirados do dataset de avaliação, para evitar viés): um bug simples (link de recuperação de senha) e um bug complexo (cobrança duplicada), cada um com User Story + Critérios de Aceitação; o complexo também demonstra as seções extras de "Contexto Técnico" e "Tasks Técnicas Sugeridas". | Acceptance Criteria Score, User Story Format Score |
| **Chain of Thought (CoT)** | Bugs simples e complexos exigem tratamento diferente (um bug de cobrança duplicada com múltiplas reclamações precisa de mais contexto técnico do que um botão que não responde). Um raciocínio em etapas guia o modelo a decidir isso antes de escrever a resposta final. | Bloco "Seu processo de raciocínio" com 6 passos (persona → ação → valor → avaliação de complexidade → critérios de aceitação → contexto técnico condicional), com instrução explícita para não expor os passos, apenas o resultado final. | Completeness Score |

Justificativas completas também ficam versionadas em `techniques_applied` / `techniques_justification` dentro do próprio `prompts/bug_to_user_story_v2.yml`.

### Ajustes feitos durante a iteração

O processo de iteração (3 rodadas) revelou dois problemas específicos que técnicas isoladas não resolviam sozinhas:

1. **Vazamento de detalhes técnicos nos Critérios de Aceitação** — o juiz de `User Story Format Score` penalizava a separação de seções quando termos de implementação (ex: "thread", "índice", "notificar o time financeiro") apareciam dentro dos Critérios de Aceitação em vez de ficarem exclusivamente em "Contexto Técnico"/"Tasks Técnicas". Foi adicionada uma regra explícita proibindo esse vazamento.
2. **Critérios subjetivos demais** — o `Acceptance Criteria Score` penalizava termos como "rápido"/"fluido" sem um valor mensurável associado (a referência do dataset usa limites concretos como "em menos de 2 segundos"). Foi adicionada uma regra explícita pedindo critérios mensuráveis sempre que o relato permitir inferir uma expectativa razoável.

## Resultados Finais

**Dashboard do LangSmith:** projeto `full-cycle-mba-challenge` — `https://smith.langchain.com/projects/full-cycle-mba-challenge` (link visível para quem tiver acesso ao workspace; capturar screenshots do dashboard antes de tornar o repositório público, se aplicável).

**Prompt publicado (público):** `https://smith.langchain.com/prompts/bug_to_user_story_v2` (owner: `lucas-almeida`)

<!-- Screenshots das avaliações (v1 com notas baixas e v2 com notas >= 0.9) devem ser capturadas do dashboard do LangSmith e anexadas aqui, ex: ![resultado v2](docs/screenshot-v2.png) -->

### Tabela comparativa: v1 (original) vs v2 (otimizado)

Avaliação executada com `python src/evaluate.py --with-v1`, sobre os 15 exemplos do dataset `datasets/bug_to_user_story.jsonl` (modelo de resposta e de avaliação: `gemini-3.5-flash-lite`).

| Métrica | v1 (`leonanluppi/bug_to_user_story_v1`) | v2 (`lucas-almeida/bug_to_user_story_v2`) |
|---|---|---|
| F1-Score | 0.89 ✗ | 0.91 ✓ |
| Tone Score | 0.90 ✓ | 0.92 ✓ |
| Acceptance Criteria Score | 0.80 ✗ | 0.90 ✓ |
| User Story Format Score | 0.90 ✓ | 0.90 ✓ |
| Completeness Score | 0.90 ✓ | 0.92 ✓ |
| **Média geral** | **0.8791** | **0.9121** |
| **Status** | ❌ FALHOU (2 de 5 métricas abaixo de 0.9) | ✅ APROVADO (todas as 5 métricas ≥ 0.9) |

Foram necessárias **3 iterações** de push + avaliação até todas as 5 métricas atingirem 0.9 simultaneamente (dentro do intervalo de 3-5 iterações esperado pelo desafio).

## Como Executar

### Pré-requisitos

- Python 3.9+
- Conta no [LangSmith](https://smith.langchain.com) com uma API key
- Uma API key de LLM (Google Gemini ou OpenAI)
- Um handle público no LangSmith Hub (crie publicando manualmente um prompt qualquer em `smith.langchain.com/prompts` — é a única etapa que a API não permite automatizar)

### Instalação

```bash
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env           # preencha as credenciais (LangSmith, LLM, USERNAME_LANGSMITH_HUB)
```

### Sequência de comandos

```bash
# 1. Pull do prompt ruim original
python src/pull_prompts.py

# 2. Editar prompts/bug_to_user_story_v2.yml aplicando as técnicas de otimização

# 3. Push do prompt otimizado (público) para o LangSmith Hub
python src/push_prompts.py

# 4. Avaliação (cria o dataset no LangSmith se não existir, roda as 5 métricas)
python src/evaluate.py

# Opcional: também avaliar o v1 original, para gerar a comparação "antes/depois"
python src/evaluate.py --with-v1

# 5. Testes de validação do prompt
pytest tests/test_prompts.py -v
```

**Nota (Windows):** o console usa por padrão a codepage `cp1252`, que não imprime os emojis/checkmarks usados nos scripts. Rode com `PYTHONIOENCODING=utf-8` na frente (Git Bash) ou `$env:PYTHONIOENCODING="utf-8"` antes (PowerShell).

**Nota (cota gratuita do Gemini):** o tier gratuito limita a 15 requisições/minuto por modelo. Cada exemplo do dataset consome 1 chamada de geração + 5 chamadas de avaliação (LLM-as-judge) = 6 chamadas; uma rodada completa (15 exemplos) soma ~90 chamadas. `src/evaluate.py` já inclui um *pacing* automático (`EVAL_CALL_DELAY_SECONDS`, padrão 4.5s) entre chamadas para respeitar essa cota — uma rodada completa leva ~7-8 minutos.
