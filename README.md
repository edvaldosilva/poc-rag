# POC de RAG para Suporte de Procedimentos

## Visao geral
Esta POC demonstra um fluxo de atendimento automatizado usando RAG (Retrieval-Augmented Generation) com Google GenAI.

Objetivo principal:
- reduzir a necessidade de atendentes humanos para responder duvidas operacionais;
- responder perguntas com base em procedimentos documentados em manuais;
- quando a informacao nao estiver nos manuais, orientar o cliente de forma educada para escalonamento humano.

Em outras palavras, a POC valida se um assistente de IA consegue atuar como primeira camada de suporte para perguntas recorrentes de processo.

## O que esta POC demonstra
- Upload automatico de todos os arquivos de uma pasta de manuais para a API.
- Uso dos manuais como contexto para responder perguntas em linguagem natural.
- Conversa interativa no terminal com historico de perguntas e respostas.
- Comportamento de fallback orientado por instrucao de sistema quando a resposta nao estiver no material.

## Arquitetura simplificada
1. O script carrega a chave de API do arquivo `.env`.
2. O script le a pasta de manuais e envia todos os arquivos para a API com upload.
3. A cada pergunta do usuario, o script envia:
   - todos os arquivos enviados;
   - o historico da conversa;
   - a pergunta atual.
4. O modelo gera a resposta com base nesse contexto.

## Estrutura do projeto
- `main.py`: script principal da POC.
- `manuais/`: pasta com os arquivos que serao carregados automaticamente como contexto.
- `requirements.txt`: dependencias Python.
- `.env`: configuracoes sensiveis (nao versionado).
- `.gitignore`: protecao de arquivos locais e segredos.

## Pre-requisitos
- Python 3.10+ (recomendado 3.11+).
- Conta e chave de API do Google AI Studio/Google GenAI.
- Acesso a internet para upload e inferencia na API.

## Configuracao
### 1) Criar e ativar ambiente virtual (PowerShell)
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2) Instalar dependencias
```powershell
python -m pip install -r requirements.txt
```

### 3) Configurar a chave no .env
Edite o arquivo `.env` e defina:
```env
GOOGLE_API_KEY=SUA_CHAVE_AQUI
```

## Como executar
1. Coloque seus arquivos de manual dentro da pasta `manuais/`.
2. Confirme a chamada da funcao em `main.py` apontando para a pasta `manuais`.
3. Execute:
```powershell
py .\main.py
```
4. Digite perguntas no terminal.
5. Para encerrar, digite `sair`.

## Exemplo de uso
No final de `main.py`, a chamada usa a pasta de manuais:
```python
executar_poc_suporte("manuais")
```

Todos os arquivos presentes na pasta serao carregados. Se a pasta estiver vazia, a execucao exibira erro informando que nao ha arquivos para carregar.

## Limites e observacoes importantes
- Esta POC envia todos os documentos e historico em todas as perguntas. Em bases grandes, isso pode aumentar custo e latencia.
- Existe limite de contexto do modelo e limites de upload da API.
- Nao ha persistencia de sessao entre execucoes.
- Nao ha integracao direta com WhatsApp nesta etapa; a interface atual e terminal.

## Seguranca
- Nunca versionar `.env`.
- Nunca expor `GOOGLE_API_KEY` em codigo fonte.
- Se uma chave for exposta, revogue e gere outra imediatamente.

## Proximos passos para evolucao
- Implementar RAG com chunking + embeddings + busca vetorial (top-k), em vez de reenviar tudo.
- Adicionar observabilidade (logs, metricas de latencia, taxa de fallback).
- Criar camada de API e integrar com canal real (ex.: WhatsApp/CRM).
- Implementar guardrails e validacoes de resposta.
- Incluir testes automatizados.

## Resumo do valor de negocio
Esta POC comprova a viabilidade de usar IA para atendimento de duvidas de procedimento com base em manuais, reduzindo carga operacional do time humano e acelerando tempo de resposta ao cliente.
