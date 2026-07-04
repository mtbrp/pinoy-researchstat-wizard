import streamlit as st
import pandas as pd
import numpy as np

# --- 1. APP CONFIGURATION ---
st.set_page_config(page_title="Pinoy Healthcare ResearchStat", page_icon="📊", layout="centered")

st.title("📊 Pinoy Healthcare ResearchStat Wizard")
st.subheader("Methodology, Search, & Statistical Visualization Dashboard")
st.write("Tailored for BS Nursing, BS PT, BS OT, Pharmacy, and Medical Technology undergrads.")
st.divider()

# --- 2. FRONT-PAGE BRIEF INFO SEARCH BAR ---
st.write("### 🔍 Quick Course & Method Search")
search_query = st.text_input(
    "Search for a research method or healthcare course (e.g., 'Nursing', 'Quantitative', 'MedTech'):",
    placeholder="Type here..."
).strip().lower()

# Dictionary containing brief contextual information
search_database = {
    "quantitative": """
        **Quantitative Method in Healthcare:** Focuses on objective measurements and statistical, mathematical, or numerical analysis of data. 
        * *Healthcare Context:* Tracking blood pressure drops across a sample, evaluating board exam passing rates, or measuring treatment efficacy scores.
    """,
    "qualitative": """
        **Qualitative Method in Healthcare:** Focuses on understanding human experiences, beliefs, and behaviors through textual or narrative data.
        * *Healthcare Context:* Exploring the lived experiences of rural nurses, understanding patient vaccine hesitancy, or phenomenological studies on burn-out among physical therapists.
    """,
    "mix-method": "See 'mixed-method'.",
    "mixed-method": """
        **Mixed-Method in Healthcare:** Combines both quantitative and qualitative data within a single study to provide a comprehensive look at a problem.
        * *Healthcare Context:* Surveying 100 medical technology interns on stress levels (Quantitative) and then conducting deep interviews with the 5 most stressed interns to understand why (Qualitative).
    """,
    "bs nursing": """
        **BS Nursing Context:** Focuses heavily on patient care models, clinical interventions, nurse-to-patient ratios, and health promotion. 
        * *Common Stat:* Descriptive means for patient satisfaction, paired $t$-tests for pre/post-training nursing knowledge.
    """,
    "bs pt": "See 'physical therapy'.",
    "bs ot": "See 'occupational therapy'.",
    "physical therapy": """
        **BS Physical Therapy / Occupational Therapy Context:** Centers around rehabilitation metrics, range of motion (ROM), recovery timelines, and functional independence measures.
        * *Common Stat:* Repeated measures ANOVA to trace patient mobility scores at week 1, week 4, and week 8 post-stroke.
    """,
    "occupational therapy": """
        **BS Occupational Therapy / Physical Therapy Context:** Centers around rehabilitation metrics, recovery timelines, ergonomic adaptations, and functional independence measures.
        * *Common Stat:* Correlation metrics relating cognitive function scores with daily living independence levels in pediatric patients.
    """,
    "pharmacy": """
        **Pharmacy Context:** Often involves drug adherence rates, compounding accuracy, medication errors, and pharmacological knowledge assessments.
        * *Common Stat:* Chi-Square tests to see if drug compliance rates differ significantly across age brackets or regions.
    """,
    "medical technology": "See 'medtech'.",
    "medtech": """
        **Medical Technology / Medical Laboratory Science Context:** Revolves around lab test sensitivity, specificity, diagnostic accuracy, machine calibration differences, and sample contamination rates.
        * *Common Stat:* Cohen's Kappa for inter-rater reliability between two different lab analysts reading blood smears.
    """
}

# Process search query
if search_query:
    found = False
    for key, value in search_database.items():
        if key in search_query:
            if "See '" in value:  # Handle simple aliases
                alias_key = value.split("'")[1]
                value = search_database[alias_key]
            st.info(value)
            found = True
            break
    if not found:
        st.warning("No specific match found. Try searching keywords like: 'Nursing', 'PT', 'Medtech', 'Quantitative', or 'Qualitative'.")
st.divider()

# --- 3. DYNAMIC METHODOLOGY SELECTOR ---
st.write("### 📐 Step-by-Step Methodology Guide")
method = st.selectbox(
    "Select Research Method:",
    ["Select a method...", "Quantitative", "Qualitative", "Mixed-Method"]
)

if method == "Quantitative":
    design = st.selectbox(
        "Select Quantitative Design:",
        ["Descriptive (Profiles, Averages)", "Correlational (Relationships)", "Experimental (Cause & Effect)"]
    )
    if design:
        st.success(f"Recommended Stat for {design}: Use Mean/SD, Pearson $r$, or $t$-tests based on your specific variables.")
        
elif method == "Qualitative":
    st.info("💡 Qualitative research uses textual analysis (e.g., Thematic Analysis via Braun & Clarke). Statistics do not apply.")
    
elif method == "Mixed-Method":
    st.info("💡 Hybrid approach: Deploy quantitative tracking surveys first, followed by qualitative focus groups.")

st.divider()

# --- 4. INTERACTIVE STATISTICAL VISUALIZATION (SLIDERS) ---
st.write("### 📉 Interactive Statistical Visualizer")
st.write(
    "Adjust the slider below to see how your **Sample Size ($n$)** directly affects your "
    "**Margin of Error** in healthcare surveys."
)

# Slider input for sample size
sample_size = st.slider("Select Sample Size ($n$ of Respondents):", min_value=10, max_value=500, value=100, step=10)

# Theoretical math formula simulation
simulated_error = (1 / np.sqrt(sample_size)) * 100

col1, col2 = st.columns(2)
with col1:
    st.metric(label="Selected Sample Size", value=f"{sample_size} students")
with col2:
    st.metric(label="Estimated Margin of Error", value=f"± {simulated_error:.2f}%", delta=f"Lower error is better", delta_color="inverse")

# Generate mock data curve visualizer
st.write("**Visualizing Precision:** As your sample size moves right, the error margin goes down.")
chart_data = pd.DataFrame({
    'Sample Size': np.arange(10, 510, 10),
    'Margin of Error (%)': (1 / np.sqrt(np.arange(10, 510, 10))) * 100
})
st.line_chart(data=chart_data, x='Sample Size', y='Margin of Error (%)')