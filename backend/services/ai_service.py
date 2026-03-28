from openai import OpenAI, OpenAIError
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="../.env")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_contract(text):
    prompt = f"""
    You are a financial contract analysis expert.

    Analyze and return ONLY JSON:

    {{
      "key_points": ["..."],
      "clauses": [
        {{
          "type": "Penalty",
          "description": "...",
          "risk": "High/Medium/Low"
        }}
      ],
      "overall_risk": "Low/Medium/High",
      "summary": "..."
    }}

    Contract:
    {text[:3000]}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except OpenAIError as e:
        if hasattr(e, 'code') and e.code == 'insufficient_quota':
            return '{"error": "OpenAI API quota exceeded. Please check your OpenAI account billing and add credits."}'
        else:
            return f'{{"error": "OpenAI API error: {str(e)}"}}'
    except Exception as e:
        return f'{{"error": "Unexpected error: {str(e)}"}}'