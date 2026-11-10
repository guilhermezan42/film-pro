import asyncio
from typing import get_args

from .models.movies import AgeRating, AgentRecommendation, Movie, MovieChoice, MovieRecommendation
from .tools.omdb import search_movie
from .tools.tmdb import get_streaming_platforms

AGE_RATINGS = get_args(AgeRating)        # ("G", "PG", "PG-13", "R", "NC-17")

GENRES_PT = {
    "Action": "Ação", "Adventure": "Aventura", "Animation": "Animação",
    "Biography": "Biografia", "Comedy": "Comédia", "Crime": "Crime",
    "Documentary": "Documentário", "Drama": "Drama", "Family": "Família",
    "Fantasy": "Fantasia", "History": "História", "Horror": "Terror",
    "Music": "Música", "Musical": "Musical", "Mystery": "Mistério",
    "Romance": "Romance", "Sci-Fi": "Ficção científica", "Sport": "Esporte",
    "Thriller": "Suspense", "War": "Guerra", "Western": "Faroeste",
}


def _split(value: str | None) -> list[str]:
    """'Action, Comedy' -> ['Action', 'Comedy'];  None -> []"""
    return [v.strip() for v in value.split(",")] if value else []


async def build_movie(choice: MovieChoice) -> Movie | None:
    data = await search_movie(choice.title, choice.release_year)
    if not isinstance(data, dict):
        return None                                   # OMDb não achou: descarta

    return Movie(
        # fatos: copiados do OMDb pelo código
        title=data["Title"],
        release_year=int(data["Year"][:4]),
        director=data["Director"],
        genres=[GENRES_PT.get(g, g) for g in _split(data["Genre"])],
        imdb_rating=float(data["imdbRating"]) if data["imdbRating"] else None,
        duration_minutes=int(data["Runtime"].split()[0]) if data["Runtime"] else None,
        age_rating=data["Rated"] if data["Rated"] in AGE_RATINGS else None,
        cast=_split(data["Actors"]),
        poster_url=data["Poster"],
        # julgamento e texto: vêm do LLM
        primary_language=choice.primary_language,
        synopsis=choice.synopsis,
        content_warnings=choice.content_warnings,
        recommendation_reason=choice.recommendation_reason,
        streaming_platforms=await get_streaming_platforms(data["imdbID"])
    )


async def enrich(choices: AgentRecommendation) -> MovieRecommendation:
    movies = await asyncio.gather(*(build_movie(c) for c in choices.movies))
    return MovieRecommendation(movies=[m for m in movies if m is not None])