from pydantic import BaseModel, Field, computed_field
from typing import Optional, List, Literal



AgeRating = Literal["G", "PG", "PG-13", "R", "NC-17"]

#& O que o LLM devolve: escolha e textos em português 
class MovieChoice(BaseModel):
    title: str = Field(..., description="O mesmo título usado no search_movie")
    release_year: int = Field(..., description="Ano de lançamento")
    primary_language: str = Field(..., description="Idioma principal, em português (ex: Inglês)")
    synopsis: str = Field(..., description="Sinopse em português, até 250 caracteres, baseada no Plot")
    content_warnings: Optional[List[str]] = Field(None, description="Avisos de conteúdo, em português")
    recommendation_reason: str = Field(..., description="Por que combina com o pedido do usuário")


class AgentRecommendation(BaseModel):
    movies: List[MovieChoice] = Field(..., description="De 5 a 10 filmes, do mais ao menos relevante")


#& O que a API devolve: fatos do OMDb + textos do LLM 
class Movie(BaseModel):
    title: str
    release_year: int
    director: Optional[str] = None
    genres: List[str] = Field(default_factory=list)
    imdb_rating: Optional[float] = None
    duration_minutes: Optional[int] = None
    age_rating: Optional[AgeRating] = None
    cast: List[str] = Field(default_factory=list)
    poster_url: Optional[str] = None
    streaming_platforms: Optional[List[str]] = None
    primary_language: str
    synopsis: str
    content_warnings: Optional[List[str]] = None
    recommendation_reason: str


class MovieRecommendation(BaseModel):
    movies: List[Movie]

    @computed_field
    @property
    def total_recommendations(self) -> int:
        return len(self.movies)

