# groq_translator.py
import os
from groq import Groq
from typing import Literal

def translate_text(text: str, target_language: Literal["marathi", "english"]) -> str:
    """Translate text using Groq API."""
    try:
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        
        prompt = f"""Translate the following text to {target_language}:
        Text: {text}
        
        Provide only the translation, without any additional explanation."""
        
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
        )
        
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        raise Exception(f"Translation error: {str(e)}")