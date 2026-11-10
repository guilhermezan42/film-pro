
import aiohttp
from typing import Any
from ..config import Config

async def search_movie(title:str,  year: int | None = None ) -> dict[str, Any] | str:
    """Busca dados de um filme no OMDb: nota IMDb, duração, diretor, elenco e pôster.

    Args:
        title: Título original em inglês, SEM o ano. Ex: "Fast Five", não "Fast Five (2011)".
        year: Ano de lançamento. Opcional, ajuda a diferenciar remakes.

    Returns:
        Dados do filme. A URL do pôster vem no campo "Poster".
    """

    api_key= Config.OMDB_API_KEY

    params={
        "apikey": api_key,
        "t": title,           # Parâmetro de título
        "type": "movie",      # Filtra apenas filmes
        "plot": "short",       # Retorna enredo resumido
        "v": "1"              # versão da API 
    }
    if year:  # adiciona parâmetro de ano de lançamento
        params["y"] = str(year)
     
    
    async with aiohttp.ClientSession() as session:

        try:
            async with session.get(
                "https://www.omdbapi.com/",
                params=params,
                timeout=aiohttp.ClientTimeout(total=10)  # Timeout de 10 segundos
            ) as response:
                if response.status != 200:
                    return f"Erro ao buscar filme: Status {response.status}"
                
                data = await response.json()

                if data.get("Response") == "False":  
                    return f"Filme não encontrado: {title}"
                

                fields = ["Title", "Year", "Director", "Actors", "Runtime", "imdbRating", "Rated", "Genre", "Language", "Plot", "Poster"] #! Retorna somente os fields necessários para o agente e a LLM
                return {k: data.get(k) for k in fields}
        
        except Exception as e:
            return f"Erro na busca do filme: {title}"



if __name__ == "__main__":
    import asyncio
    from dotenv import load_dotenv

    load_dotenv()
    print(asyncio.run(search_movie("Fast Five", 2011)))