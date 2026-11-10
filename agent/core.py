import asyncio

from agno.agent import Agent
from agno.models.openai import OpenAIResponses

from .config import Config
from .models.movies import AgentRecommendation, MovieRecommendation
from .prompts import description, instructions
from .tools.omdb import search_movie
from .enrichment import enrich

Config.validate()

movie_recommendation_agent = Agent(
    name="FilmPro",
    model=OpenAIResponses(id="gpt-6-luna", api_key=Config.OPENAI_API_KEY),
    tools=[search_movie],
    tool_call_limit=15,
    description=description,
    instructions=instructions,
    add_datetime_to_context=True,
    output_schema=AgentRecommendation,
    debug_mode=True,
    debug_level=1,
)
async def recommendations(preferences:str) -> MovieRecommendation | None:
    result = await movie_recommendation_agent.arun(
        preferences,
        stream=False,
    )
    if not (result and result.content):
        return None

    return await enrich(result.content)
    # if result and result.content:
    #     data: MovieRecommendation  = result.content
    #     pretty_json_output = data.model_dump_json(indent=2)
    #     print(pretty_json_output)
    #     return data

if __name__ == "__main__":

    result = asyncio.run(recommendations("Estou procurando filmes similares ao Senhor dos Anéis..."))
    print(result.model_dump_json(indent=2) if result else "Sem resposta")
