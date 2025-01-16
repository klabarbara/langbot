import re
import json
import os

def clean_text(text):
    text = re.sub(r"[^\w\s.,?!]", "", text)  # keeps basic punctuation
    text = re.sub(r"\s+", " ", text).strip()  
    return text

def preprocess_content(input_file="data/translation/translated_content.json", output_file="data/processed/cleaned_content.json"):
    try:
        # loads translated content
        with open(input_file, "r", encoding="utf-8") as f:
            content = json.load(f)

        cleaned_headers = [clean_text(h) for h in content["headers"]]
        cleaned_paragraphs = [clean_text(p) for p in content["paragraphs"]]

        processed_content = {
            "url": content["url"],
            "headers": cleaned_headers,
            "paragraphs": cleaned_paragraphs,
        }

        # saves translated and cleaned content
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(processed_content, f, ensure_ascii=False, indent=4)

        print(f"Processed content saved to {output_file}")
    except Exception as e:
        print(f"Error preprocessing content: {e}")

if __name__ == "__main__":
    preprocess_content()
