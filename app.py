import streamlit as st
from crew import build_crew

st.set_page_config(page_title="🚗 AI Car Recommender", layout="wide")
st.title("🚗 AI Car Recommender")
st.markdown("Powered by **CrewAI** · Multi-Agent System")

with st.form("car_form"):
    col1, col2 = st.columns(2)

    with col1:
        budget     = st.text_input("💰 Budget", placeholder="e.g. 10-15 lakhs")
        use_case   = st.text_input("🛣️ Use Case", placeholder="e.g. family SUV, city commute")
        fuel_type  = st.selectbox("⛽ Fuel Type",
                                  ["No Preference", "Petrol", "Diesel", "Electric", "Hybrid"])

    with col2:
        seats      = st.slider("💺 Minimum Seats", min_value=2, max_value=8, value=5)
        brand_pref = st.text_input("🏷️ Brand Preference", placeholder="e.g. Hyundai, Tata or None")
        notes      = st.text_area("📝 Additional Requirements",
                                   placeholder="e.g. sunroof, ADAS, large boot space")

    submitted = st.form_submit_button("🔍 Find My Car")

if submitted:
    if not budget or not use_case:
        st.warning("Please fill in at least Budget and Use Case.")
    else:
        requirements = {
            "budget":     budget,
            "use_case":   use_case,
            "fuel_type":  fuel_type,
            "seats":      str(seats),
            "brand_pref": brand_pref or "No preference",
            "notes":      notes or "None",
        }

        with st.spinner("🤖 Researching your perfect car..."):
            crew   = build_crew(requirements)
            result = crew.kickoff()

        st.success("✅ Recommendation Ready!")
        st.markdown("---")
        st.markdown(result.raw)
