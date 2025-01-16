from src.scraping.site_scraper import scrape_website
from src.translation.translate import translate_content
from src.preprocessing.cleaner import preprocess_content

def main():
    url = "https://example.com"  # Mandarin site url goes here
    raw_file = "data/raw/website_content.json"
    translated_file = "data/translation/translated_content.json"
    processed_file = "data/processed/cleaned_content.json"

    # Step 1: Scrape the website
    scrape_website(url, raw_file)

    # Step 2: Translate the content
    translate_content(raw_file, translated_file)

    # Step 3: Preprocess the translated content
    preprocess_content(translated_file, processed_file)

    print("Pipeline completed successfully!")

if __name__ == "__main__":
    main()
