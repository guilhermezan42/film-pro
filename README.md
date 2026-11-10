# FilmPro - Agente de Recomendação de Filmes

API de recomendações personalizadas de filmes com IA, construída com **Agno**, **OpenAI** e **FastAPI**.

O usuário descreve o que gosta (ex.: "filmes como Velozes e Furiosos 5, gosto de ação e comédia") e recebe uma lista de filmes com sinopse, motivo da recomendação, nota do IMDb, elenco, pôster e onde assistir.

## Como funciona

```
pedido do usuário
   ↓
Agente (LLM + ferramenta search_movie)   → escolhe os filmes e escreve os textos em português
   ↓  para cada filme, em paralelo
OMDb + TMDB                              → o código preenche os fatos: nota, duração, elenco, pôster, streaming
   ↓
resposta JSON da API
```

O LLM cuida do que exige julgamento (quais filmes recomendar e por quê). Os dados factuais são copiados das APIs pelo código, o que evita erros como URLs de pôster quebradas.

## Requisitos

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)

## Setup

```bash
# Instalar dependências (cria o .venv automaticamente)
uv sync

# Criar o arquivo de variáveis de ambiente e preencher as chaves
cp .env.example .env
```

| Variável | Obrigatória | Onde conseguir |
|---|---|---|
| `OPENAI_API_KEY` | Sim | https://platform.openai.com/api-keys |
| `OMDB_API_KEY` | Sim | https://www.omdbapi.com/apikey.aspx (gratuita, 1.000 requisições/dia) |
| `TMDB_API_KEY` | Não | https://www.themoviedb.org/settings/api (sem ela, `streaming_platforms` vem `null`) |

## Executar

```bash
# Subir a API
uv run main.py
```

A documentação interativa fica em **http://127.0.0.1:8001/docs**.

Para testar partes isoladas:

```bash
# Rodar só o agente, no terminal
uv run python -m agent.core

# Testar só a busca no OMDb
uv run python -m agent.tools.omdb
```

## Endpoints

| Método | Rota | Descrição |
|---|---|---|
| GET | `/` | Informações da API |
| GET | `/health` | Verifica se a API está online |
| POST | `/recommendations` | Gera recomendações a partir das preferências |

### Exemplo

```bash
curl -X POST http://127.0.0.1:8001/recommendations \
  -H "Content-Type: application/json" \
  -d '{"preferences": "Quero filmes como Velozes e Furiosos 5. Gosto de ação e comédia"}'
```

`preferences` deve ter entre 10 e 500 caracteres. A resposta leva de 10 a 20 segundos.

```json
{
  "success": true,
  "data": {
    "movies": [
      {
        "title": "Bad Boys II",
        "release_year": 2003,
        "director": "Michael Bay",
        "genres": ["Ação", "Comédia", "Crime"],
        "imdb_rating": 6.6,
        "duration_minutes": 147,
        "age_rating": "R",
        "cast": ["Will Smith", "Martin Lawrence", "Gabrielle Union"],
        "poster_url": "https://m.media-amazon.com/images/M/...jpg",
        "streaming_platforms": null,
        "primary_language": "Inglês",
        "synopsis": "Dois detetives de Miami investigam um cartel de drogas...",
        "content_warnings": ["Violência", "Linguagem forte"],
        "recommendation_reason": "Ação grandiosa, perseguições e uma dupla com muito humor."
      }
    ],
    "total_recommendations": 1
  },
  "message": "Recomendações geradas com sucesso"
}
```

### De onde vem cada campo

| Campos | Fonte | Observações |
|---|---|---|
| `title`, `release_year`, `director`, `imdb_rating`, `duration_minutes`, `cast`, `poster_url` | OMDb | Copiados pelo código |
| `genres` | OMDb | Traduzidos para português |
| `age_rating` | OMDb | Padrão americano: `G`, `PG`, `PG-13`, `R`, `NC-17`, ou `null` |
| `streaming_platforms` | TMDB (dados do JustWatch) | Streaming por assinatura no Brasil. `null` = não foi possível consultar; `[]` = não está em nenhum |
| `primary_language`, `synopsis`, `content_warnings`, `recommendation_reason` | LLM | Em português |
| `total_recommendations` | Calculado | Quantidade de filmes |

## Estrutura

```
├── main.py                     # Sobe a API (uvicorn, porta 8001)
├── api/
│   ├── app.py                  # App FastAPI, CORS e endpoints de sistema
│   └── routers.py              # POST /recommendations
├── agent/
│   ├── config.py               # Variáveis de ambiente (classe Config)
│   ├── core.py                 # Agente FilmPro e função recommendations()
│   ├── enrichment.py           # Junta a escolha do LLM com os dados do OMDb e do TMDB
│   ├── models/movies.py        # Schemas Pydantic (saída do agente e resposta da API)
│   ├── prompts/movie_search.py # Prompt do agente
│   └── tools/
│       ├── omdb.py             # Busca de filmes no OMDb, com cache em memória
│       └── tmdb.py             # Onde assistir, via TMDB
├── .env.example                # Modelo do .env
├── pyproject.toml              # Dependências
└── uv.lock                     # Versões exatas das dependências
```

## Observações

- Os dados de streaming vêm do **JustWatch**, via TMDB. Os termos de uso do TMDB exigem citar o JustWatch onde esses dados forem exibidos.
- O cache do OMDb fica em memória e é apagado quando o servidor reinicia.

## Próximos passos

- [ ] Front-end
- [ ] Mostrar também aluguel e compra (`rent`/`buy` do TMDB), além da assinatura
- [ ] Avaliar o TMDB como fonte principal: gêneros e sinopse em português (`language=pt-BR`) e elenco com personagens
- [ ] Mostrar quantas requisições do OMDb ainda restam no dia