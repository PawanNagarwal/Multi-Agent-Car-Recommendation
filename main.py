from crew import build_crew

def get_user_requirements() -> dict:
    """Interactive CLI to collect user requirements."""
    print("\n🚗 Welcome to AI Car Recommender (Powered by CrewAI)\n")
    print("=" * 50)

    budget     = input("💰 What is your budget? (e.g., 10-15 lakhs): ").strip()
    use_case   = input("🛣️  Primary use case? (e.g., family SUV, city commute, road trips): ").strip()
    fuel_type  = input("⛽ Fuel preference? (Petrol/Diesel/Electric/Hybrid/No preference): ").strip()
    seats      = input("💺 Minimum seats required? (e.g., 5, 7): ").strip()
    brand_pref = input("🏷️  Brand preference? (e.g., Maruti, Hyundai, No preference): ").strip()
    notes      = input("📝 Any additional requirements? (e.g., sunroof, ADAS, boot space): ").strip()

    return {
        "budget":     budget,
        "use_case":   use_case,
        "fuel_type":  fuel_type,
        "seats":      seats,
        "brand_pref": brand_pref,
        "notes":      notes,
    }


if __name__ == "__main__":
    requirements = get_user_requirements()

    print("\n⚙️  Initializing AI agents...\n")
    crew = build_crew(requirements)

    print("\n🚀 Agents are working on your recommendation...\n")
    result = crew.kickoff()

    print("\n" + "=" * 60)
    print("✅ FINAL CAR RECOMMENDATION REPORT")
    print("=" * 60)
    print(result.raw)
