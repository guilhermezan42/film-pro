# FilmPro - Agente de Recomendação de Filmes

Agente inteligente baseado em IA que fornece recomendações personalizadas de filmes usando **Agno** e **OpenAI**.

## Setup Rápido

> ⚠️ **Requisitos:** Python 3.12+ e [uv](https://docs.astral.sh/uv/) instalados.

```bash
# Instalar dependências (cria o .venv automaticamente)
uv sync
```

```bash
# Configurar API key (depois edite o .env e coloque sua chave)
cp .env.example .env

# Executar
uv run main.py
```

## Estrutura

```
├── main.py                  # Agente principal
├── prompts/
│   ├── __init__.py
│   └── movie_search.py      # Prompts e instruções
├── .env.example             # Modelo do .env
├── pyproject.toml           # Dependências
└── uv.lock                  # Versões exatas das dependências
```

## Funcionalidades

- 🎬 Recomendações personalizadas de filmes
- 🔍 Busca integrada na web
- 📋 Respostas em Markdown formatado
- 🌍 Suporte a múltiplos critérios (gênero, classificação, idioma)
- 🇧🇷 Respostas em português
