import streamlit as st
import pandas as pd
from st_supabase_connection import SupabaseConnection

# --- 1. CONFIGURATION & INITIALIZATION ---
st.set_page_config(page_title="Pinoy Healthcare Board Reviewer", page_icon="🇵🇭", layout="centered")

# Initialize Supabase connection using Streamlit secrets
supabase = st.connection("supabase", type=SupabaseConnection)

# Define your public Google Sheets URL (Replace with your actual public link)
# Make sure the sheet ends with /export?format=csv
GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/export?format=csv&gid=0"

# Initialize Session States for Quiz Flow
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_info" not in st.session_state:
    st.session_state.user_info = None
if "q_index" not in st.session_state:
    st.session_state.q_index = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False
if "submitted" not in st.session_state:
    st.session_state.submitted = False

# --- 2. CACHED DATA FETCHING ---
@st.cache_data(ttl=3600)  # Caches questions for 1 hour to keep it free and instant
def fetch_quiz_data(url):
    try:
        df = pd.read_csv(url)
        # Ensure all required column names are lowercase stripped for safety
        df.columns = df.columns.str.strip().str.lower()
        return df
    except Exception as e:
        st.error(f"Error loading board exam questions: {e}")
        return pd.DataFrame()

# --- 3. AUTHENTICATION LOGIC (SUPABASE OAUTH) ---
def handle_login():
    # Triggers Supabase OAuth for Google
    try:
        # Note: In a live environment, Supabase handles the redirection.
        # This function generates the authorization URL for Google Sign-In.
        auth_data = supabase.client.auth.sign_in_with_oauth({
            "provider": "google",
            "options": {
                "redirect_to": "https://your-app-name.streamlit.app"  # Your Streamlit production URL
            }
        })
        if auth_data:
            st.info("Redirecting to Google Secure Login...")
            # Streamlit handles the handoff via the generated OAuth URL
    except Exception as e:
        st.error(f"Login failed: {e}")

# Check if user returned from Google OAuth with an active session token
# (st_supabase_connection automatically catches active session cookies/tokens if configured)
try:
    session = supabase.client.auth.get_session()
    if session and session.user:
        st.session_state.logged_in = True
        st.session_state.user_info = session.user
except Exception:
    pass  # No active session found yet

# --- 4. UI ROUTING (GATEKEEPER) ---
if not st.session_state.logged_in:
    # Welcome Screen / Gated Login Screen
    st.title("🇵🇭 Pinoy Healthcare Board Reviewer")
    st.subheader("PT • OT • Nursing • MedTech • Pharmacy")
    st.write("Welcome, future topnotcher! Practice board-exam style questions per subject. Sign in with your school or personal Gmail account to track your progress for free.")
    
    if st.button("🔴 Sign in with Google Mail", use_container_width=True):
        handle_login()
        # For local testing simulation, toggle this if you haven't setup Google Cloud Console yet:
        # st.session_state.logged_in = True
        # st.session_state.user_info = {"id": "test-user-123", "email": "student@edu.ph"}
        # st.rerun()

else:
    # --- 5. MAIN APPLICATION (LOGGED IN) ---
    user_email = st.session_state.user_info.get("email", "Student")
    
    # Top Navbar / Header
    col1, col2 = st.columns([4, 1])
    with col1:
        st.write(f"👋 MedReviewer Account: **{user_email}**")
    with col2:
        if st.button("Log out"):
            supabase.client.auth.sign_out()
            st.session_state.logged_in = False
            st.session_state.user_info = None
            st.rerun()
            
    st.divider()

    # --- 6. QUIZ MANAGEMENT & INTERACTION ---
    questions_df = fetch_quiz_data(GOOGLE_SHEET_URL)

    if questions_df.empty:
        st.warning("⚠️ No quiz questions found. Please check your Google Sheet structure.")
    else:
        if not st.session_state.quiz_started:
            st.title("📋 Select Your Review Module")
            subject = st.selectbox("Choose Subject Module:", ["Nursing Mock Exam (NP1)", "MedTech Hematology", "PT/OT Anatomy"])
            
            if st.button("Start Practice Exam", type="primary"):
                st.session_state.quiz_started = True
                st.session_state.current_subject = subject
                st.session_state.q_index = 0
                st.session_state.score = 0
                st.session_state.submitted = False
                st.rerun()
        else:
            # Active Quiz State
            idx = st.session_state.q_index
            subject = st.session_state.current_subject
            
            if idx < len(questions_df):
                row = questions_df.iloc[idx]
                
                st.caption(f"📚 Module: {subject}")
                st.progress((idx) / len(questions_df))
                st.write(f"### Question {idx + 1} of {len(questions_df)}")
                st.write(f"**{row['question']}**")
                
                # Setup Radio Choices dynamically
                options = [row['a'], row['b'], row['c'], row['d']]
                choice = st.radio("Select the correct answer:", options, key=f"choice_q_{idx}")
                
                if not st.session_state.submitted:
                    if st.button("Submit Answer", type="primary"):
                        st.session_state.submitted = True
                        st.rerun()
                else:
                    # Rationale & Answer Validation View
                    # Map full choice string back to the corresponding letter column ('a','b','c','d')
                    selected_letter = ['a', 'b', 'c', 'd'][options.index(choice)]
                    correct_letter = str(row['answer']).strip().lower()
                    
                    if selected_letter == correct_letter:
                        st.success("✨ Correct Answer!")
                        if not st.session_state.get(f"scored_q_{idx}", False):
                            st.session_state.score += 1
                            st.session_state[f"scored_q_{idx}"] = True
                    else:
                        st.error(f"❌ Incorrect. The correct answer is **{correct_letter.upper()}**.")
                        
                    st.info(f"💡 **Rationale:** {row['rationale']}")
                    
                    if st.button("Next Question ➡️"):
                        st.session_state.q_index += 1
                        st.session_state.submitted = False
                        st.rerun()
            else:
                # --- 7. QUIZ END & SCORE LOGGING TO DATABASE ---
                st.balloons()
                st.title("🎉 Mock Exam Completed!")
                final_score = st.session_state.score
                total_q = len(questions_df)
                percentage = round((final_score / total_q) * 100, 2)
                
                st.metric(label="Your Final Score", value=f"{final_score} / {total_q}", delta=f"{percentage}%")
                
                # Push metrics to Supabase profiles/quiz_scores table securely
                try:
                    user_id = st.session_state.user_info.get("id")
                    # Send single score record object via raw RPC or table insert
                    response = supabase.table("quiz_scores").insert({
                        "user_id": user_id,
                        "subject": subject,
                        "score": final_score,
                        "total_questions": total_q
                    }).execute()
                    st.toast("🎯 Progress saved automatically to your dashboard profile!", icon="💾")
                except Exception as e:
                    st.warning("⚠️ Score processed, but could not sync progress database.")
                
                if st.button("Return to Dashboard"):
                    st.session_state.quiz_started = False
                    st.rerun()