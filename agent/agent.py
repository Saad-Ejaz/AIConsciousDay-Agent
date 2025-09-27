import os
import json
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# -----------------------------
# API Key & Model Setup
# -----------------------------
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "gpt-4o-mini")

if not OPENROUTER_API_KEY:
    raise ValueError("❌ OPENROUTER_API_KEY is missing. Please set it in your .env or Streamlit Secrets.")

# Set OpenRouter as OpenAI-compatible
os.environ["OPENAI_API_KEY"] = OPENROUTER_API_KEY
os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"

# -----------------------------
# LangChain Imports
# -----------------------------
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema.runnable import RunnableSequence

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

prompt = PromptTemplate(
    input_variables=["journal", "dream", "intention", "priorities", "date"],
    template=PROMPT_TEMPLATE
)

llm = ChatOpenAI(
    model_name=OPENROUTER_MODEL,
    temperature=0.7
)

# ✅ Modern chain pipeline using |
chain = prompt | llm

# -----------------------------
# Agent Function
# -----------------------------
def run_reflection_agent(journal, dream="", intention="", priorities="", date=""):
    try:
        # ✅ Modern invoke() instead of run()
        output = chain.invoke({
            "journal": journal,
            "dream": dream,
            "intention": intention,
            "priorities": priorities,
            "date": date
        })

        # Some LLMs return message objects, handle gracefully
        if hasattr(output, "content"):
            output_text = output.content
        else:
            output_text = str(output)

        # Clean & parse JSON
        output_clean = re.sub(r"```(?:json)?", "", output_text, flags=re.IGNORECASE).strip()
        match = re.search(r"\{.*\}", output_clean, re.DOTALL)
        json_str = match.group(0) if match else "{}"

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
