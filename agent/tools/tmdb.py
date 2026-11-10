import aiohttp

from ..config import Config

TMDB_URL = "https://api.themoviedb.org/3"

def _dedupe(names: list[str]) -> list[str]:
    """Remove 'X Amazon Channel' e 'X with Ads' quando o serviço X já está na lista."""
    return [n for n in names if not any(n != base and n.startswith(base) for base in names)]

async def get_streaming_platforms(imdb_id: str, country: str = "BR") -> list[str] | None:
    """Plataformas de streaming por assinatura onde o filme está disponível no país.

    Retorna None se não foi possível descobrir, e [] se o filme não está em nenhuma.
    """

    if not Config.TMDB_API_KEY:
        return None

    params = {"api_key": Config.TMDB_API_KEY}
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
            # 1. converte o ID do IMDb no ID do TMDB
            async with session.get(f"{TMDB_URL}/find/{imdb_id}",
                                   params={**params, "external_source": "imdb_id"}) as r:
                r.raise_for_status()
                found = (await r.json()).get("movie_results", [])
            if not found:
                return None

            # 2. busca onde assistir
            async with session.get(f"{TMDB_URL}/movie/{found[0]['id']}/watch/providers",
                                   params=params) as r:
                r.raise_for_status()
                providers = (await r.json()).get("results", {}).get(country, {})
    except Exception:
        return None

    return _dedupe([p["provider_name"] for p in providers.get("flatrate", [])])


"""
Para ligar isso no resto:
    - omdb.py: adicione "imdbID" à lista FIELDS.
    - config.py e .env.example: adicione TMDB_API_KEY, inclusive no validate().
    - Schema Movie: volte com streaming_platforms: Optional[List[str]] = None.
    - build_movie: acrescente streaming_platforms=await get_streaming_platforms(data["imdbID"]).

A diferença entre None e [] existe de propósito, e o front vai precisar dela:
- None quer dizer "não sabemos": a busca falhou ou o filme não está no TMDB.
- [] quer dizer "não está em nenhum streaming no Brasil".

Mais dois pontos:
- flatrate é só o que está incluído na assinatura. A resposta também traz rent (aluguel) e buy (compra), se você quiser mostrar depois.
- Os termos do TMDB pedem que a fonte "JustWatch" seja citada quando você exibe esses dados. Anote para o front.

Uma observação para o futuro: com a chave do TMDB em mãos, vale saber que ele também devolve gêneros e sinopse em português (language=pt-BR) e o elenco com os personagens. Talvez um dia ele substitua o OMDb.

Possível feature mostrar o numero de requisições restantes no TMDB por dia
"""