import os
from openai import OpenAI
from utils import extract_text_from_txt
import config

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=config.OPENROUTER_API_KEY 
)

def summarize_text(text):
    response = client.chat.completions.create(
        model="mistralai/devstral-small",
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to craft a perfect news article."},
            {"role": "user", "content": f"""
                    Summarize the following RBI notification in 2-3 bullet points, highlighting only the most important regulatory change or decision.
                    Avoid Markdown or special characters. 
                    Use this format:
                        Sentence
                        Sentence
                    \n{text}"""
            }
        ]
    )
    return response.choices[0].message.content

def summarize_all_txt(text_dir, output_dir):
    for filename in os.listdir(text_dir):
        if filename.endswith(".txt"):
            text = extract_text_from_txt(os.path.join(text_dir, filename))
            if not text:
                continue
            print(f"Summarizing {filename}")
            summary = summarize_text(text)
            output_file = os.path.join(output_dir, filename.replace(".txt", "_summary.txt"))
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(summary)
