from crewai import Agent


def create_keywords_search_agent(llm):
    return Agent(
        role="Search Query Strategist",
        goal="\n".join([
            "Generate a diverse set of highly relevant search queries.",
            "Ensure the queries target specific products or categories to maximize discovery."
        ]),
        backstory=(
            "An expert in consumer behavior and search engine strategies, this agent crafts "
            "targeted and creative search queries to improve product visibility and retrieval "
            "from online sources."
        ),
        llm=llm,
        verbose=True
    )


