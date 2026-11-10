import asyncio

from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.tools.websearch import WebSearchTools

from .config import Config
from .models.movies import MovieRecommendation
from .prompts import description, instructions
from .tools.omdb import search_movie

Config.validate()

movie_recommendation_agent = Agent(
    name="FilmPro",
    model=OpenAIResponses(id="gpt-6-luna", api_key=Config.OPENAI_API_KEY),
    tools=[WebSearchTools(backend="bing", enable_news=False), search_movie],
    tool_call_limit=15,
    description=description,
    instructions=instructions,
    markdown=True,
    add_datetime_to_context=True,
    output_schema=MovieRecommendation,
    debug_mode=True,
    debug_level=1,
)
async def recommendations(preferences:str):
    result = await movie_recommendation_agent.arun(
        preferences,
        stream=False,
    )

    if result and result.content:
        data: MovieRecommendation  = result.content
        pretty_json_output = data.model_dump_json(indent=2)
        print(pretty_json_output)
        return data

if __name__ == "__main__":

    asyncio.run(recommendations("Estou procurando filmes similares ao Senhor dos Anéis. Gosto de filmes de ação."))