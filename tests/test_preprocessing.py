import pytest
import os
import json
from src.preprocessing.cleaner import clean_text, preprocess_content

@pytest.fixture
def sample_translated_content(tmp_path):
    """Fixture to create a sample translated JSON file."""
    sample_data = {
        "url": "https://example.com",
        "headers": ["  Header1!  ", "Header#2  "],
        "paragraphs": ["  This is a paragraph.  ", "Another paragraph!   "]
    }
    input_file = tmp_path / "translated_content.json"
    with open(input_file, "w", encoding="utf-8") as f:
        json.dump(sample_data, f, ensure_ascii=False, indent=4)
    return input_file

def test_clean_text():
    """Test clean_text function."""
    assert clean_text("  Hello, World!  ") == "Hello, World!"
    assert clean_text("Header#1!!") == "Header1!!"
    assert clean_text("This  is \ttext.") == "This is text."

def test_preprocess_content(sample_translated_content, tmp_path):
    """Test preprocess_content function."""
    output_file = tmp_path / "cleaned_content.json"
    preprocess_content(input_file=sample_translated_content, output_file=output_file)

    # Check if output file is created
    assert os.path.exists(output_file)

    # Validate processed content
    with open(output_file, "r", encoding="utf-8") as f:
        processed_content = json.load(f)
    
    assert processed_content["url"] == "https://example.com"
    assert processed_content["headers"] == ["Header1!", "Header2"]
    assert processed_content["paragraphs"] == ["This is a paragraph.", "Another paragraph!"]
