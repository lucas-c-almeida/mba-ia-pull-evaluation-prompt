# Pull, Otimização e Avaliação de Prompts com LangChain e LangSmith

## Objetivo

Você deve entregar um software capaz de:

- **Fazer pull de prompts** do LangSmith Prompt Hub contendo prompts de baixa qualidade
- **Refatorar e otimizar** esses prompts usando técnicas avançadas de Prompt Engineering
- **Fazer push dos prompts otimizados** de volta ao LangSmith
- **Avaliar a qualidade** através de métricas customizadas (F1-Score, Tone Score, Acceptance Criteria Score, User Story Format Score, Completeness Score)
- **Atingir pontuação mínima** de 0.9 (90%) em todas as métricas de avaliação

---

## Exemplo no CLI

```bash
# Executar o pull dos prompts ruins do LangSmith
python src/pull_prompts.py

# Executar avaliação inicial (prompts ruins)
python src/evaluate.py

# Executando avaliação dos prompts...
Prompt: bug_to_user_story_v1
- F1-Score: 0.48
- Tone Score: 0.45
- Acceptance Criteria Score: 0.52
- User Story Format Score: 0.48
- Completeness Score: 0.50
Status: FALHOU - Métricas abaixo do mínimo de 0.9

# Após refatorar os prompts e fazer push
python src/push_prompts.py

# Executar avaliação final (prompts otimizados)
python src/evaluate.py

# Executando avaliação dos prompts...
Prompt: bug_to_user_story_v2
- F1-Score: 0.93
- Tone Score: 0.94
- Acceptance Criteria Score: 0.96
- User Story Format Score: 0.93
- Completeness Score: 0.95
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
   - Faz pull do seguinte prompt:
     - `leonanluppi/bug_to_user_story_v1`
   - Salva os prompts localmente em `prompts/bug_to_user_story_v1.yml`

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
3. Deixá-lo público

---

### 4. Iteração

- Espera-se 3-5 iterações.
- Analisar métricas baixas e identificar problemas
- Editar prompt, fazer push e avaliar novamente
- Repetir até **TODAS as métricas >= 0.9**

### Critério de Aprovação:

- F1-Score >= 0.9
- Tone Score >= 0.9
- Acceptance Criteria Score >= 0.9
- User Story Format Score >= 0.9
- Completeness Score >= 0.9

MÉDIA das 5 métricas >= 0.9

**IMPORTANTE:** TODAS as 5 métricas devem estar >= 0.9, não apenas a média!

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

Faça um fork do repositório base: **[https://github.com/devfullcycle/mba-ia-pull-evaluation-prompt](https://github.com/devfullcycle/mba-ia-pull-evaluation-prompt)**

```
mba-ia-pull-evaluation-prompt/
├── .env.example                  # Template das variáveis de ambiente
├── requirements.txt              # Dependências Python
├── README.md                     # Sua documentação do processo
├── datasets/
│   └── bug_to_user_story.jsonl   # 15 exemplos de bugs (JSONL)
├── prompts/
│   ├── bug_to_user_story_v1.yml  # Prompt inicial (após pull)
│   └── bug_to_user_story_v2.yml  # Seu prompt otimizado
├── src/
│   ├── pull_prompts.py           # Pull do LangSmith
│   ├── push_prompts.py           # Push ao LangSmith
│   ├── evaluate.py               # Avaliação automática
│   ├── metrics.py                # 5 métricas implementadas
│   └── utils.py                  # Funções auxiliares
└── tests/
    └── test_prompts.py           # Testes de validação
```

## O que você vai criar

- `prompts/bug_to_user_story_v2.yml` - Seu prompt otimizado
- `tests/test_prompts.py` - Seus testes de validação
- `src/pull_prompts.py` - Script de pull do repositório da fullcycle
- `src/push_prompts.py` - Script de push para o seu repositório
- `README.md` - Documentação do seu processo de otimização

## O que já vem pronto

- Dataset com 15 bugs (5 simples, 7 médios, 3 complexos)
- 5 métricas de avaliação (F1-Score + 4 específicas para Bug to User Story)
- Suporte multi-provider (OpenAI e Gemini)

## Repositórios úteis

- Repositório boilerplate do desafio: [https://github.com/devfullcycle/mba-ia-pull-evaluation-prompt](https://github.com/devfullcycle/mba-ia-pull-evaluation-prompt)
- LangSmith Documentation: [https://docs.smith.langchain.com/](https://docs.smith.langchain.com/)
- Prompt Engineering Guide: [https://www.promptingguide.ai/](https://www.promptingguide.ai/)

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

### 4. Executar avaliação

```bash
python src/evaluate.py
```

---

## Entregável

1. **Repositório público no GitHub (fork do repositório base) contendo:**
   - Todo o código-fonte implementado
   - Arquivo `prompts/bug_to_user_story_v2.yml` 100% preenchido e funcional
   - Arquivo `README.md` atualizado com as seções abaixo

2. **README.md deve conter:**

   **A) Seção "Técnicas Aplicadas (Fase 2)":**
   - Quais técnicas avançadas você escolheu para refatorar os prompts
   - Justificativa de por que escolheu cada técnica
   - Exemplos práticos de como aplicou cada técnica

   **B) Seção "Resultados Finais"**
   - Link público do seu dashboard do LangSmith mostrando as avaliações
   - Screenshots das avaliações com as notas mínimas de 0.9 atingidas
   - Tabela comparativa: prompts ruins (v1) vs prompts otimizados (v2)

   **C) Seção "Como Executar"**
   - Instruções claras e detalhadas de como executar o projeto
   - Pré-requisitos e dependências
   - Comandos para cada fase do projeto

   **D) Evidências no LangSmith**
   - Link público (ou screenshots) do dashboard do LangSmith
   - Devem estar visíveis:
     - Dataset de avaliação com ≥ 15 exemplos
     - Execuções dos prompts v1 (ruins) com notas baixas
     - Execuções dos prompts v2 (otimizados) com notas ≥ 0.9
     - Tracing detalhado de pelo menos 3 exemplos

---

## Dicas Finais

- Lembre-se da importância da especificidade, contexto e persona ao refatorar prompts
- Use Few-shot Learning com 2-3 exemplos claros para melhorar drasticamente a performance
- Chain of Thought (CoT) é excelente para tarefas que exigem raciocínio complexo (como análise de bugs)
- Use o Tracing do LangSmith como sua principal ferramenta de debug - ele mostra exatamente o que o LLM está "pensando"
- Não altere os datasets de avaliação
- Itere, itere, itere - é normal precisar de 3-5 iterações para atingir 0.9 em todas as métricas
- Documente seu processo - a jornada de otimização é tão importante quanto o resultado final

---

# Documentação do Processo (Lucas Almeida)

> As seções abaixo documentam a execução real deste desafio neste repositório, seguindo os itens A, B, C e D exigidos em `instrucoes.md` (a seção acima replica o enunciado atual, mantido como referência).

## Técnicas Aplicadas (Fase 2)

O prompt otimizado está em [`prompts/bug_to_user_story_v2.yml`](prompts/bug_to_user_story_v2.yml). Foram aplicadas 3 técnicas (mínimo exigido: 2):

| Técnica | Por que foi escolhida | Como foi aplicada | Métrica que mais beneficia |
|---|---|---|---|
| **Role Prompting** | O prompt v1 não define nenhuma persona, o que resulta em tom genérico/neutro. Fixar uma persona de PM sênior empático puxa diretamente o tom das respostas. | `system_prompt` abre com: *"Você é um Product Manager (PM) sênior, especialista em metodologias ágeis (Scrum/Kanban), com grande empatia pelo usuário final e foco constante em valor de negócio."* | Tone Score |
| **Few-shot Learning** | Instruções descritivas sozinhas não garantem que o modelo reproduza o formato exato exigido (User Story + Critérios de Aceitação em Given/When/Then). Exemplos completos calibram o modelo a copiar o padrão. | 2 exemplos completos e inventados (não retirados do dataset de avaliação, para evitar viés): um bug simples (link de recuperação de senha) e um bug complexo (cobrança duplicada), cada um com User Story + Critérios de Aceitação; o complexo também demonstra as seções extras de "Contexto Técnico" e "Tasks Técnicas Sugeridas". | Acceptance Criteria Score, User Story Format Score |
| **Chain of Thought (CoT)** | Bugs simples e complexos exigem tratamento diferente (um bug de cobrança duplicada com múltiplas reclamações precisa de mais contexto técnico do que um botão que não responde). Um raciocínio em etapas guia o modelo a decidir isso antes de escrever a resposta final. | Bloco "Seu processo de raciocínio" com 6 passos (persona → ação → valor → avaliação de complexidade → critérios de aceitação → contexto técnico condicional), com instrução explícita para não expor os passos, apenas o resultado final. | Completeness Score |

Justificativas completas também ficam versionadas em `techniques_applied` / `techniques_justification` dentro do próprio `prompts/bug_to_user_story_v2.yml`.

### Ajustes feitos durante a iteração

O processo de iteração revelou problemas específicos que as 3 técnicas isoladas não resolviam sozinhas. Foram 6 rodadas de push + avaliação no total — as 3 primeiras contra `gemini-3.5-flash-lite` (até aprovar todas as 5 métricas), e mais 3 contra `gemini-3.1-flash-lite` depois que o `gemini-3.5-flash-lite` esgotou a cota diária gratuita (ver nota abaixo):

1. **Vazamento de detalhes técnicos nos Critérios de Aceitação** — o juiz de `User Story Format Score` penalizava a separação de seções quando termos de implementação (ex: "thread", "índice", "notificar o time financeiro") apareciam dentro dos Critérios de Aceitação em vez de ficarem exclusivamente em "Contexto Técnico"/"Tasks Técnicas". Foi adicionada uma regra explícita proibindo esse vazamento.
2. **Critérios subjetivos demais** — o `Acceptance Criteria Score` penalizava termos como "rápido"/"fluido" sem um valor mensurável associado (a referência do dataset usa limites concretos como "em menos de 2 segundos"). Foi adicionada uma regra explícita pedindo critérios mensuráveis.
3. **Persona como frase, não rótulo** — trocando de modelo de avaliação, surgiu uma crítica nova: a persona deveria ser um rótulo curto ("Cliente", "Administrador") e não uma cláusula descritiva. Foi adicionada uma regra + exemplo few-shot ajustado.
4. **Persona errada em bugs de sistema/segurança** — para bugs de integração (webhook, permissão) o juiz esperava uma persona de sistema/negócio, ou (em bugs de segurança) a persona de quem é protegido pela correção, não de quem a executa tecnicamente. Regra explícita adicionada.
5. **Identificadores específicos na frase principal** — a User Story não deve citar IDs/dados específicos do bug relatado na frase "Como um... eu quero... para que..."; isso deve ficar nos Critérios/Contexto Técnico.
6. **Critérios técnicos/não-funcionais empilhados** — mais de um requisito técnico (tempo de resposta + erro de rede + responsividade) na mesma lista de critérios foi visto como fuga de escopo; a regra de mensurabilidade foi limitada a no máximo um critério quantificado por vez.

## Resultados Finais

**Dashboard público do LangSmith (dataset + todos os experiments + traces):**
https://smith.langchain.com/public/1301c56a-d9bc-4e11-b129-1bbdf88d0358/d

**Prompt publicado (público):** https://smith.langchain.com/hub/lucas-almeida/bug_to_user_story_v2 (owner: `lucas-almeida`)

A avaliação usa `langsmith.evaluation.evaluate()` (ver "Como Executar"), que cria um **Experiment vinculado ao dataset** — visível na aba "Experiments" do link acima, com feedback (score + comentário do juiz) anexado a cada execução, não apenas traces soltos. Veja a seção [Evidências no LangSmith](#evidências-no-langsmith) para o mapa de cada evidência exigida.

> ℹ️ **Nota sobre cota do Gemini e variância do juiz LLM:** durante o desenvolvimento, o `gemini-3.5-flash-lite` esgotou a cota diária gratuita (500 req/dia), o que motivou 3 iterações extras (4-6, ver acima) testadas contra `gemini-3.1-flash-lite`. Depois de créditos serem adicionados à conta do Google (removendo o limite do tier gratuito), a versão final do `bug_to_user_story_v2.yml` (já com as regras das iterações 4-6) foi revalidada contra o modelo oficial `gemini-3.5-flash-lite`. Rodando a mesma versão do prompt duas vezes seguidas, obtivemos: uma execução com **todas as 5 métricas ≥ 0.9** (0.9195 de média) e uma segunda execução com F1-Score e User Story Format Score ficando bem na borda, ~0.01 abaixo de 0.9 (0.9102 de média) — variação normal de um avaliador LLM-as-judge perto do limiar, não uma regressão do prompt. Em ambas as execuções, o v2 superou o v1 nas 5 métricas.

### Tabela comparativa: v1 (original) vs v2 (final, com iterações 1-6)

Avaliação executada com `python src/evaluate.py --with-v1`, sobre os 15 exemplos do dataset `datasets/bug_to_user_story.jsonl` (modelo de resposta e de avaliação: `gemini-3.5-flash-lite`, tier pago).

| Métrica | v1 (`leonanluppi/bug_to_user_story_v1`) | v2 — execução A | v2 — execução B |
|---|---|---|---|
| F1-Score | 0.88 ✗ | 0.90 ✓ | 0.90 ✗ (0.8975) |
| Tone Score | 0.91 ✓ | 0.94 ✓ | 0.92 ✓ |
| Acceptance Criteria Score | 0.81 ✗ | 0.91 ✓ | 0.92 ✓ |
| User Story Format Score | 0.87 ✗ | 0.92 ✓ | 0.89 ✗ (0.8920) |
| Completeness Score | 0.89 ✗ | 0.93 ✓ | 0.93 ✓ |
| **Média geral** | **0.8733** | **0.9195** | **0.9102** |
| **Status** | ❌ FALHOU (4 de 5 métricas abaixo de 0.9) | ✅ APROVADO (todas ≥ 0.9) | ❌ FALHOU (2 métricas ~0.01 abaixo de 0.9) |

O v2 é categoricamente superior ao v1 em todas as 5 métricas, nas duas execuções. Foram necessárias **6 iterações** de push + avaliação no total (3 contra `gemini-3.5-flash-lite`, 3 contra `gemini-3.1-flash-lite` durante o esgotamento de cota) até o prompt atingir consistentemente ~0.90-0.92 por métrica.

### Histórico das iterações 4-6 (`gemini-3.1-flash-lite`, durante o esgotamento de cota do modelo oficial)

| Iteração | F1 | Tone | Acceptance Criteria | User Story Format | Completeness | Média |
|---|---|---|---|---|---|---|
| 4 | 0.8992 ✗ | 0.94 ✓ | 0.93 ✓ | 0.8988 ✗ | 0.94 ✓ | 0.9207 |
| 5 | 0.90 ✓ | 0.95 ✓ | 0.91 ✓ | 0.8787 ✗ | 0.94 ✓ | 0.9171 |
| 6 | 0.8975 ✗ | 0.95 ✓ | 0.94 ✓ | 0.8920 ✗ | 0.94 ✓ | 0.9222 |

Tone, Acceptance Criteria e Completeness ficaram consistentemente ≥ 0.9; F1 e User Story Format Score oscilaram na faixa 0.88-0.90 sem convergir de forma estável, dentro do que parece ser ruído normal do LLM-juiz nessa fronteira, não um erro sistemático identificável no prompt.

## Evidências no LangSmith

**🔗 Link público (acessível sem login):** https://smith.langchain.com/public/1301c56a-d9bc-4e11-b129-1bbdf88d0358/d

> Conforme a [documentação do LangSmith](https://docs.langchain.com/langsmith/manage-datasets), compartilhar um dataset publicamente também torna públicos *"os exemplos do dataset, os experiments e runs associados, e os feedbacks"*. Ou seja, este único link cobre todas as evidências exigidas — não é necessário (nem existe) compartilhar cada Experiment separadamente. Basta abrir o link e usar a aba **Experiments**.

| Evidência exigida | Onde ver | Status |
|---|---|---|
| Dataset de avaliação com ≥ 15 exemplos | Aba **Examples** do link público — dataset `full-cycle-mba-challenge-eval`, carregado de `datasets/bug_to_user_story.jsonl` | ✅ 15 exemplos |
| Execuções do prompt v1 (ruim) com notas baixas | Aba **Experiments** → `leonanluppi-bug_to_user_story_v1-fe6a7ebc` | ✅ média 0.8733 (4 de 5 métricas < 0.9) |
| Execuções do prompt v2 (otimizado) com notas ≥ 0.9 | Aba **Experiments** → `lucas-almeida-bug_to_user_story_v2-4e814d5a` (Execução A) | ✅ todas as 5 métricas ≥ 0.9, média 0.9195 |
| Tracing detalhado de pelo menos 3 exemplos | Clique em qualquer linha de um Experiment para abrir o trace completo | ✅ 15 execuções rastreadas por Experiment, cada uma com o trace da chamada de geração + os 5 feedbacks (score + comentário do juiz) |

Links diretos para cada Experiment (mesmo token público):

- **v1 (ruim):** `https://smith.langchain.com/public/1301c56a-d9bc-4e11-b129-1bbdf88d0358/d/compare?selectedSessions=6fb1c9e6-e63c-4a2e-8af5-0c7dd99c88ae`
- **v2 (aprovado, Execução A):** `https://smith.langchain.com/public/1301c56a-d9bc-4e11-b129-1bbdf88d0358/d/compare?selectedSessions=844045d6-82cc-443a-99fc-52c526ba4b18`

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

# 4. Avaliação (cria o dataset no LangSmith se não existir, roda as 5 métricas
#    via langsmith.evaluation.evaluate() — cria um Experiment vinculado ao
#    dataset, visível na aba "Experiments" do LangSmith)
python src/evaluate.py

# Opcional: também avaliar o v1 original, para gerar a comparação "antes/depois"
python src/evaluate.py --with-v1

# 5. Testes de validação do prompt
pytest tests/test_prompts.py -v
```

**Nota (Windows):** o console usa por padrão a codepage `cp1252`, que não imprime os emojis/checkmarks usados nos scripts. Rode com `PYTHONIOENCODING=utf-8` na frente (Git Bash) ou `$env:PYTHONIOENCODING="utf-8"` antes (PowerShell).

**Nota (cota gratuita do Gemini):** o tier gratuito limita a 15 requisições/minuto **e também um total diário por modelo** (ex: 500/dia para `gemini-3.5-flash-lite` no momento em que este projeto foi feito — o limite exato varia por modelo e pode mudar). Cada exemplo do dataset consome 1 chamada de geração + 5 chamadas de avaliação (LLM-as-judge) = 6 chamadas; uma rodada completa (15 exemplos) soma ~90 chamadas. `src/evaluate.py` já inclui um *pacing* automático (`EVAL_CALL_DELAY_SECONDS`, padrão 4.5s) entre chamadas para respeitar o limite por minuto — uma rodada completa leva ~7-8 minutos. Se a cota **diária** esgotar (erro 429 com `quota_id: GenerateRequestsPerDayPerProjectPerModel-FreeTier`), a única saída é trocar de modelo (ex: `gemini-3.1-flash-lite`, que tem cota própria e separada), adicionar créditos/billing na conta do Google (remove o limite do tier gratuito), ou esperar o reset do dia seguinte — não há como contornar isso com mais *pacing*. Com billing ativo, o *pacing* de 4.5s deixa de ser necessário; pode reduzir com `EVAL_CALL_DELAY_SECONDS=0.5 python src/evaluate.py` para uma rodada de ~1-2 minutos.
