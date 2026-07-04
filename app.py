import streamlit as st

# --- 1. CONFIGURATION & UI STYLING ---
st.set_page_config(
    page_title="Pinoy ReserchStat Wizard", 
    page_icon="📊", 
    layout="centered"
)

st.title("📊 Pinoy ResearchStat Wizard")
st.subheader("Your Methodology & Statistical Computation Guide")
st.write(
    "Stuck on Chapter 3? Select your research approach below, and we will "
    "suggest the appropriate statistical computations for your study."
)
st.divider()

# --- 2. STEP 1: RESEARCH METHOD ---
st.write("### 🔍 Step 1: Select Your Research Method")
method = st.selectbox(
    "What is your overarching research method?",
    ["Select a method...", "Quantitative (Numerical data)", "Qualitative (Textual/Conceptual data)", "Mixed-Method (Both)"]
)

# --- 3. STEP 2 & 3: CONDITIONAL LOGIC BASED ON USER INPUT ---
if method == "Quantitative (Numerical data)":
    st.write("### 📐 Step 2: Choose Your Research Design")
    design = st.selectbox(
        "Which quantitative research design matches your study?",
        [
            "Select a design...",
            "Descriptive (Describing profiles, frequencies, averages)",
            "Correlational (Testing relationships between two variables)",
            "Quasi-Experimental / Experimental (Testing cause and effect between groups)"
        ]
    )
    
    if design != "Select a design...":
        st.divider()
        st.write("### 🧮 Step 3: Suggested Statistical Computations")
        
        if "Descriptive" in design:
            st.info("💡 **Your Study Focus:** Describing characteristics of a population or phenomenon.")
            
            # Using Markdown tables for clear, scannable data
            st.markdown("""
            | Statistical Tool | When to Use | Example in Pinoy Healthcare |
            | :--- | :--- | :--- |
            | **Frequency & Percentage** | To show demographic distributions. | Counting how many Nursing students prefer online vs. traditional review. |
            | **Mean & Standard Deviation** | To determine the average score or level of agreement. | Finding the average satisfaction level (1-5 Likert Scale) of MedTech interns. |
            """)
            
        elif "Correlational" in design:
            st.info("💡 **Your Study Focus:** Determining if a relationship exists between variables without establishing cause.")
            
            st.markdown("""
            | Statistical Tool | Data Type Type | Example in Pinoy Healthcare |
            | :--- | :--- | :--- |
            | **Pearson $r$ Correlation** | Both variables are continuous/interval. | Correlating Pharmacy student study hours with their local mock board scores. |
            | **Spearman Rho ($\rho$)** | Ranked or ordinal data (e.g., Likert items). | Relating socioeconomic status (Low, Mid, High) with stress levels. |
            """)
            st.caption("Note: Use standard $p$-value testing ($p < 0.05$) to check if the correlation is statistically significant.")
            
        elif "Experimental" in design:
            st.info("💡 **Your Study Focus:** Comparing groups to evaluate the effect of an intervention.")
            
            st.markdown("""
            | Statistical Tool | Setup | Example in Pinoy Healthcare |
            | :--- | :--- | :--- |
            | **Independent $t$-test** | Comparing **2 separate groups**. | Comparing PT board scores of students who used an app vs. those who used books. |
            | **Paired $t$-test** | Comparing **1 group** before and after. | Testing Nursing students' anxiety levels *before* and *after* a wellness seminar. |
            | **ANOVA (One-Way)** | Comparing **3 or more groups**. | Comparing passing rates among physical therapy grads from 3 different regions. |
            """)

elif method == "Qualitative (Textual/Conceptual data)":
    st.write("### 📐 Step 2: Choose Your Research Design")
    design = st.selectbox(
        "Which qualitative research design matches your study?",
        [
            "Select a design...",
            "Phenomenological (Exploring lived experiences)",
            "Thematic Analysis (Identifying patterns across interviews)",
            "Case Study (In-depth exploration of a bounded system)"
        ]
    )
    
    if design != "Select a design...":
        st.divider()
        st.write("### 📝 Step 3: Suggested Data Analysis Methods")
        st.warning("⚠️ **Reminder:** Qualitative studies deal with non-numerical text, meanings, and insights. Traditional statistical calculations (like t-tests) do not apply here!")
        
        st.markdown("""
        * **Suggested Approach:** **Colaizzi’s Method** or **Braun & Clarke's Thematic Analysis**.
        * **Tools to use:** Qualitative analysis software like **NVivo**, **ATLAS.ti**, or systematic manual coding in Excel.
        * **Output Metric:** Rather than tables of numbers, your results will yield **Themes, Sub-themes, and Direct Patient/Student Quotations**.
        """)

elif method == "Mixed-Method (Both)":
    st.write("### 📐 Step 2: Choose Your Research Design")
    design = st.selectbox(
        "Which mixed-method framework are you deploying?",
        [
            "Select a design...",
            "Explanatory Sequential (Quant first ➡️ Qual follows to explain results)",
            "Exploratory Sequential (Qual first ➡️ Quant follows to test findings)"
        ]
    )
    
    if design != "Select a design...":
        st.divider()
        st.write("### 🧮 Dynamic Suggested Computations")
        st.success("✨ **Hybrid Route:** You will run both mathematical statistics and thematic coding.")
        
        if "Explanatory" in design:
            st.write("1. **First Phase (Quant):** Run descriptive statistics or correlation metrics on your survey questionnaires.")
            st.write("2. **Second Phase (Qual):** Conduct follow-up interviews with outlier participants to clarify *why* those numbers occurred.")
        else:
            st.write("1. **First Phase (Qual):** Interview students to discover variables or build a unique local metric tool.")
            st.write("2. **Second Phase (Quant):** Distribute that newly created tool to a wide audience and run Factor Analysis or Cronbach's Alpha for reliability testing.")

# --- 4. FOOTER ---
if method != "Select a method...":
    st.caption("---")
    st.caption("Disclaimer: Ensure your specific choice aligns with your thesis adviser's recommendation or your institutional panel guidelines.")