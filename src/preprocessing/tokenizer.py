from transformers import AutoTokenizer
import json
import os

def tokenize_content(
    input_file="data/processed/cleaned_content.json",
    output_file="data/processed/tokenized_content.json",
    tokenizer_model="bert-base-multilingual-cased"
):
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            content = json.load(f)

        tokenizer = AutoTokenizer.from_pretrained(tokenizer_model)

        tokenized_headers = [tokenizer.encode(h, truncation=True, padding="max_length", max_length=128) for h in content["headers"]]
        tokenized_paragraphs = [tokenizer.encode(p, truncation=True, padding="max_length", max_length=512) for p in content["paragraphs"]]

        tokenized_content = {
            "url": content["url"],
            "headers": tokenized_headers,
            "paragraphs": tokenized_paragraphs,
        }

        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(tokenized_content, f, ensure_ascii=False, indent=4)

        print(f"Tokenized content saved to {output_file}")
    except Exception as e:
        print(f"Error tokenizing content: {e}")

if __name__ == "__main__":
    tokenize_content()
