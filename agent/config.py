import os
from dotenv import load_dotenv

# carrega o arquivo .env 
load_dotenv()

class Config:
    """Gerenciador de configurações centralizado."""

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OMDB_API_KEY = os.getenv("OMDB_API_KEY")
    TMDB_API_KEY = os.getenv("TMDB_API_KEY")   # opcional: sem ela, streaming_platforms vem null

    @classmethod
    def validate(cls):
        """Valida se as variáveis de ambiente obrigatórias estão definidas."""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY não está definida no arquivo .env")
        if not cls.OMDB_API_KEY:
            raise ValueError("OMDB_API_KEY não está definida no arquivo .env")