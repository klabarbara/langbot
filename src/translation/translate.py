from googletrans import Translator
import json
import os

def translate_content(input_file="data/raw/website_content.json", output_file="data/translation/translated_content.json"):
    try:
        # load raw content
        with open(input_file, "r", encoding="utf-8") as f:
            content = json.load(f)

        translator = Translator()
        # translate
        translated_headers = [translator.translate(h, src="zh-cn", dest="en").text for h in content["headers"]]
        translated_paragraphs = []
        for p in content["paragraphs"]:
            if p.strip():
                try:
                    translated_text = translator.translate(p, src="zh-cn", dest="en").text
                    translated_paragraphs.append(translated_text)
                except Exception as e:
                    print(f"Error translating paragraph: {p[:50]}... ({e})")
            else:
                print(f"Skipping empty paragraph: {repr(p)}")

        translated_content = {
            "url": content["url"],
            "headers": translated_headers,
            "paragraphs": translated_paragraphs,
        }
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(translated_content, f, ensure_ascii=False, indent=4)

        print(f"Translated content saved to {output_file}")
    except Exception as e:
        print(f"Error translating content: {e}")

if __name__ == "__main__":
    translate_content()
