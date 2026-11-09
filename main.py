from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.websearch import WebSearchTools
from prompts import *
from dotenv import load_dotenv

load_dotenv()

movie_recomendation_agent = Agent(
    name="FilmPro",
    model=OpenAIResponses(id="gpt-6-luna"),
    tools=[DuckDuckGoTools(enable_search=True, enable_news=False)],
    description=description,
    instructions=instructions,
    markdown=True,
    add_datetime_to_context=True,
    debug_mode=True,
)


if __name__ == "__main__":
    movie_recomendation_agent.print_response(
        input=["Estou procurando filmes similares a velozes e furiosos 2",
        "Gosto de filmes com ação e comédia"],
        stream=True
    )