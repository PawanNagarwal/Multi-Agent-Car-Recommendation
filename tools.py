from crewai.tools import SerperDevTool
search_tool = SerperDevTool(
    country = "in",
    locale = 'en',
    num_results = 10
)

