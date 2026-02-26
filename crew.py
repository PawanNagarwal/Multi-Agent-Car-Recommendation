import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai import search_tool

## Agents 

intake_agent = Agent(
    role = "car requirements analyst",
    goal = (
        "Extract, validate and structure the users's car requirements including budget, use case, fuel type, seating capacity, and brand preference"
    ),
    backstory= (
        "You are a seasoned automotive consultant with 15 years of experience"
        "helping indian buyers choose the right car. You ask sharp clarifying"
        "quesitons and convert vagur requirements into precise filter criteria"
    ),
    verbose=True,
    allow_delegation= False
)

research_agent = Agent(
    role = "Automotive market researcher",
    goal = (
        "Search the indian automobile market to find the top 5 cars that best"
        "match the structured requirements. Father model name, price , mileage, key specs and user ratings"
    ),
    tools = [search_tool],
    verbose=True,
    allow_delegation=False
)

recommendendation_agent = Agent(
    
    role = "Car Recommendation Specialist",
    goal = (
        "Evaluate the researched cars against the user requirements and produce a "
        "ranked recommendation report with pros, cons, and a final top 2 pick with justification"),
    backstory = (
        "You are a trusted automotive journalist know for unbiased, buyer centric"
        "car reviews. You balacnce technical specs with real-world usability and "
        "always tailor your advice to buyer's lifestyle and budget."
    ),
    verbose = True,
    allow_delegations= False

)


## Tasks

def build_tasks(user_requirements: dict) -> list:
    """
    Dynamically builds tasks using user-provided requirements.
    """

    intake_task = Task(
        description=(
            f"Analyze the following user inputs and structure them into a clear "
            f"requirements document:\n\n"
            f"- Budget: {user_requirements.get('budget')}\n"
            f"- Use Case: {user_requirements.get('use_case')}\n"
            f"- Fuel Type: {user_requirements.get('fuel_type')}\n"
            f"- Seats Required: {user_requirements.get('seats')}\n"
            f"- Brand Preference: {user_requirements.get('brand_pref')}\n"
            f"- Additional Notes: {user_requirements.get('notes', 'None')}\n\n"
            "Normalize budget to INR if needed. Flag any conflicting requirements."
        ),
        expected_output=(
            "A structured requirements summary with the following fields:\n"
            "1. Budget Range (in INR)\n"
            "2. Primary Use Case\n"
            "3. Fuel Type Preference\n"
            "4. Minimum Seating Capacity\n"
            "5. Brand Preferences / Exclusions\n"
            "6. Must-Have Features\n"
            "7. Nice-to-Have Features"
        ),
        agent=intake_agent,
    )
    
    research_task = Task(
        description=(
            "Using the structured requirements from the intake task, search the "
            "Indian car market for the top 5 best-matching cars. "
            "For each car, gather:\n"
            "- Full model name and variant\n"
            "- Ex-showroom price in India (2024-2025)\n"
            "- Fuel efficiency (kmpl or km/charge for EVs)\n"
            "- Engine specs (cc, power, torque)\n"
            "- Key features (safety, infotainment, comfort)\n"
            "- User ratings (from CarDekho, CarWale, or similar)\n"
            "- Major pros and cons"
        ),
        expected_output=(
            "A detailed list of exactly 5 cars with all the above specs. "
            "Format each car as a numbered entry with sub-sections for specs, "
            "features, ratings, and pros/cons."
        ),
        agent=research_agent,
        context=[intake_task],  # receives intake_task output as context
    )
    
    recommendation_task = Task(
        description=(
            "Evaluate all 5 researched cars against the user's original requirements. "
            "Score each car on the following criteria (1-10):\n"
            "1. Budget Fit\n"
            "2. Use Case Match\n"
            "3. Fuel Efficiency\n"
            "4. Features vs Price\n"
            "5. Reliability & Brand Trust\n\n"
            "Rank the cars from best to worst and declare a Top Pick. "
            "Provide a one-paragraph justification for the top pick."
        ),
        expected_output=(
            "A final Car Recommendation Report containing:\n"
            "1. Ranked list of all 5 cars with scores per criterion\n"
            "2. A comparison table (Car | Price | Score | Verdict)\n"
            "3. Top Pick with detailed justification\n"
            "4. Alternative Pick (best runner-up)\n"
            "5. Cars to Avoid (if any) with reason"
        ),
        agent=recommendendation_agent,
        context=[research_task],  # receives research_task output as context
    )

    return [intake_task, research_task, recommendation_task]

## CREW Builder

def build_crew(user_requirements: dict) -> Crew:
    tasks = build_tasks(user_requirements)
    
    crew = Crew(
        agents = [intake_agent, research_agent, recommendendation_agent],
        tasks = Process.sequential,
        verbose=True,
    )
    return crew


