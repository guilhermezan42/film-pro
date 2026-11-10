from pydantic import BaseModel, Field
from typing import Optional, List


class Cast(BaseModel):
    """Informações sobre membro do elenco"""
    name: str = Field(..., description="Nome do ator/atriz")
    character: Optional[str] = Field(None, description="Nome do personagem interpretado")


class Movie(BaseModel):
    """Modelo estruturado para dados de filme"""
    title: str = Field(..., description="Título do filme")
    release_year: int = Field(..., description="Ano de lançamento")
    director: str = Field(..., description="Diretor principal")
    genres: List[str] = Field(..., description="Gênero e subgêneros")
    imdb_rating: float = Field(..., description="Classificação IMDB (foco em 7.5+)")
    duration_minutes: int = Field(..., description="Duração em minutos")
    primary_language: str = Field(..., description="Idioma principal")
    synopsis: str = Field(..., description="Sinopse breve e envolvente")
    age_rating: str = Field(..., description="Classificação etária (ex: PG, PG-13, 16, 18)")
    content_warnings: Optional[List[str]] = Field(None, description="Avisos de conteúdo")
    cast: List[Cast] = Field(default_factory=list, description="Elenco notável")
    poster_url: Optional[str] = Field(None, description="URL do pôster")
    streaming_platforms: Optional[List[str]] = Field(None, description="Plataformas de streaming")
    recommendation_reason: str = Field(..., description="Breve explicação para a recomendação")


class MovieRecommendation(BaseModel):
    """Resposta estruturada com múltiplas recomendações"""
    movies: List[Movie] = Field(..., description="Lista de filmes recomendados (mínimo 5)")
    total_recommendations: int = Field(..., description="Quantidade de filmes recomendados")