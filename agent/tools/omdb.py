
import aiohttp
from typing import Any
from ..config import Config

OMDB_URL = "https://www.omdbapi.com/"
FIELDS = ["Title", "Year", "Director", "Actors", "Runtime", "imdbRating",
          "Rated", "Genre", "Language", "Plot", "Poster", "imdbID"]

_cache: dict[tuple[str, int | None], dict[str, Any]] = {}



async def _fetch(session: aiohttp.ClientSession, params: dict) -> dict:
    """Faz uma requisição ao OMDb e devolve o JSON."""
    async with session.get(OMDB_URL, params=params,
                           timeout=aiohttp.ClientTimeout(total=10)) as response:
        response.raise_for_status()          # status diferente de 200 vira exceção
        return await response.json()


def _is_real_movie(data: dict, year: int | None) -> bool:
    """Recusa resultado vazio, registro lixo (sem duração) e ano que não bate."""
    if data.get("Response") != "True" or data.get("Runtime") in (None, "N/A"):
        return False
    found_year = (data.get("Year") or "")[:4]
    return year is None or (found_year.isdigit() and abs(int(found_year) - year) <= 1)


async def search_movie(title: str, year: int | None = None) -> dict[str, Any] | str:
    """Busca dados de um filme no OMDb: nota IMDb, duração, diretor, elenco e pôster.

    Args:
        title: Título original em inglês, SEM o ano. Ex: "Fast Five", não "Fast Five (2011)".
        year: Ano de lançamento. Opcional, ajuda a diferenciar remakes.

    Returns:
        Dados do filme. A URL do pôster vem no campo "Poster".
    """

    key = (title.lower(), year)  # Early return se filme está no cache 
    if key in _cache:
        return _cache[key]

    params = {
        "apikey": Config.OMDB_API_KEY, 
        "t": title, 
        "type": "movie", 
        "plot": "short"
        }
    if year:
        params["y"] = str(year)

    try:
        async with aiohttp.ClientSession() as session:
            data = await _fetch(session, params)
            if year and not _is_real_movie(data, year):
                params.pop("y")                  # tenta de novo sem o ano
                data = await _fetch(session, params)
    except Exception as e:
        return f"Erro na busca do filme: {title} ({e})"

    if not _is_real_movie(data, year):
        return f"Filme não encontrado: {title}"
    result = {k: None if data.get(k) == "N/A" else data.get(k) for k in FIELDS} # gera o dicionário de resposta dinamicamente usando os FIELDS
    _cache[key] = result          # só guarda no cache quando a busca deu certo
    return result




if __name__ == "__main__":
    import asyncio
    from dotenv import load_dotenv

    load_dotenv()
    print(asyncio.run(search_movie("Fast Five", 2011)))