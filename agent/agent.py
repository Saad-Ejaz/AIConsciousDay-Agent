# agent/agent.py
import os
import json
import re
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.chat_models import ChatOpenAI  # OpenRouter via OpenAI-compatible API

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "gpt-4o-mini")

# Ensure OpenRouter works as OpenAI endpoint
os.environ["OPENAI_API_KEY"] = OPENROUTER_API_KEY
os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"

# -----------------------------
# Prompt Template
# -----------------------------
PROMPT_TEMPLATE = """
You are a daily reflection and planning assistant. Your goal is to:
1. Reflect on the user's journal and dream input
2. Interpret their emotional & mental state
3. Understand their intention and top priorities
4. Produce a practical, energy-aligned day strategy

INPUT:
Morning Journal: {journal}
Dream: {dream}
Intention: {intention}
Top 3 Priorities: {priorities}
Date: {date}

OUTPUT:
Return ONLY a JSON object with FOUR top-level keys:
- reflection: string summarizing journal and dream
- dream_interpretation: string
- mindset_insight: string
- strategy: list of actionable steps
"""

# -----------------------------
# LangChain Setup
# -----------------------------
prompt = PromptTemplate(
    input_variables=["journal", "dream", "intention", "priorities", "date"],
    template=PROMPT_TEMPLATE
)

llm = ChatOpenAI(
    model_name=OPENROUTER_MODEL,
    temperature=0.7
)

chain = LLMChain(llm=llm, prompt=prompt)

# -----------------------------
# Run Reflection Agent
# -----------------------------
def run_reflection_agent(journal, dream="", intention="", priorities="", date=""):
    """
    Runs the LangChain agent via OpenRouter (OpenAI-compatible) to generate:
    - reflection summary
    - dream interpretation
    - mindset insight
    - suggested day strategy
    Returns a dict with keys: reflection, dream_interpretation, mindset_insight, strategy
    """
    try:
        output = chain.run(
            journal=journal,
            dream=dream,
            intention=intention,
            priorities=priorities,
            date=date
        )

        # Clean code block markers if present
        output_clean = re.sub(r"```(?:json)?", "", output, flags=re.IGNORECASE).strip()

        # Extract first valid JSON object
        match = re.search(r"\{.*\}", output_clean, re.DOTALL)
        json_str = match.group(0) if match else "{}"

        # Parse JSON safely
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError:
            data = {
                "reflection": output_clean,
                "dream_interpretation": "",
                "mindset_insight": "",
                "strategy": []
            }

        # Ensure all keys exist
        for key in ["reflection", "dream_interpretation", "mindset_insight", "strategy"]:
            if key not in data:
                data[key] = "" if key != "strategy" else []

        return data

    except Exception as e:
        return {
            "reflection": f"Agent failed: {str(e)}",
            "dream_interpretation": "",
            "mindset_insight": "",
            "strategy": []
        }
