import os
import json
from dotenv import load_dotenv
import streamlit as st
from agent.agent import run_reflection_agent
from db import init_db, insert_entry, fetch_entry_by_date, fetch_all_dates
from datetime import date

# Load environment variables
load_dotenv()
init_db()

st.set_page_config(page_title="ConsciousDay Agent", layout="centered")
st.title("🧠 ConsciousDay Agent")
st.subheader("Reflect inward. Act with clarity.")

# --- Tabs ---
tab1, tab2 = st.tabs(["🌅 New Entry", "📜 History"])

# ======================
# TAB 1 — NEW ENTRY
# ======================
with tab1:
    st.header("Morning Inputs")
    today = st.date_input("Date", value=date.today())
    journal = st.text_area("Morning Journal", height=200)
    dream = st.text_area("Dream (optional)", height=120)
    intention = st.text_input("Intention of the Day")
    priorities = st.text_area("Top 3 Priorities (comma-separated)")

    if st.button("Analyze & Save"):
        if not journal.strip() and not dream.strip():
            st.error("⚠️ Please enter a Morning Journal or Dream.")
        else:
            with st.spinner("🤖 Generating insights..."):
                try:
                    resp = run_reflection_agent(
                        journal=journal,
                        dream=dream,
                        intention=intention,
                        priorities=priorities,
                        date=str(today)
                    )

                    reflection = resp.get("reflection", "")
                    dream_interpretation = resp.get("dream_interpretation", "")
                    mindset_insight = resp.get("mindset_insight", "")
                    strategy = resp.get("strategy", "")

                    reflection_str = json.dumps(reflection, ensure_ascii=False, indent=2) if isinstance(reflection, (dict, list)) else str(reflection)
                    dream_str = json.dumps(dream_interpretation, ensure_ascii=False, indent=2) if isinstance(dream_interpretation, (dict, list)) else str(dream_interpretation)
                    mindset_str = json.dumps(mindset_insight, ensure_ascii=False, indent=2) if isinstance(mindset_insight, (dict, list)) else str(mindset_insight)
                    strategy_str = json.dumps(strategy, ensure_ascii=False, indent=2) if isinstance(strategy, (dict, list)) else str(strategy)

                    insert_entry(
                        entry_date=str(today),
                        journal=journal,
                        intention=intention,
                        dream=dream,
                        priorities=priorities,
                        reflection=reflection_str,
                        strategy=strategy_str
                    )

                    st.success("✅ Saved to entries.db")
                    st.markdown("### 🪞 Inner Reflection Summary")
                    st.write(reflection_str)
                    st.markdown("### 🌙 Dream Interpretation")
                    st.write(dream_str)
                    st.markdown("### 🧠 Mindset Insight")
                    st.write(mindset_str)
                    st.markdown("### 🧭 Suggested Day Strategy")
                    st.write(strategy_str)

                except Exception as e:
                    st.error(f"Agent failed: {e}")

# ======================
# TAB 2 — HISTORY
# ======================
with tab2:
    st.header("View Previous Reflections")
    dates = fetch_all_dates()

    if dates:
        chosen_date = st.selectbox("Select a date", options=dates)
        if st.button("Load Entry"):
            record = fetch_entry_by_date(chosen_date)
            if record:
                st.markdown(f"### 📅 Date: {record['date']}")
                st.markdown("#### 📝 Journal")
                st.write(record["journal"])
                st.markdown("#### 🌙 Dream")
                st.write(record["dream"])
                st.markdown("#### ✨ Intention")
                st.write(record["intention"])
                st.markdown("#### 📌 Top 3 Priorities")
                st.write(record["priorities"])
                st.markdown("#### 🪞 Inner Reflection Summary")
                st.write(record["reflection"])
                st.markdown("#### 🧭 Suggested Day Strategy")
                st.write(record["strategy"])
            else:
                st.info("No entry found for this date.")
    else:
        st.info("No saved entries yet. Add one from the 'New Entry' tab.")
