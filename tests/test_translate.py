import pytest
from unittest.mock import patch, Mock
import os
import json
from src.translation.translate import translate_content

@pytest.fixture
def sample_raw_content(tmp_path):
    """Fixture to create a sample raw JSON file."""
    sample_data = {
        "url": "https://example.com",
        "headers": ["示例标题", "更多示例"],
        "paragraphs": ["这是一个段落。", "另一个段落。"]
    }
    input_file = tmp_path / "website_content.json"
    with open(input_file, "w", encoding="utf-8") as f:
        json.dump(sample_data, f, ensure_ascii=False, indent=4)
    return input_file

def test_translate_content(sample_raw_content, tmp_path):
    """Test translate_content function with mocked translation."""
    output_file = tmp_path / "translated_content.json"

    # fake translation setup
    mock_translations = {
        "示例标题": "Example Title",
        "更多示例": "More Examples",
        "这是一个段落。": "This is a paragraph.",
        "另一个段落。": "Another paragraph."
    }

    def mock_translate(text, src, dest):
        """Mock translate function."""
        return Mock(text=mock_translations.get(text, f"Translated {text}"))

    with patch("src.translation.translate.Translator") as MockTranslator:
        mock_translator = MockTranslator.return_value
        mock_translator.translate.side_effect = mock_translate

        # runs fxn under test
        translate_content(input_file=sample_raw_content, output_file=output_file)

    assert os.path.exists(output_file)

    # validate translated content
    with open(output_file, "r", encoding="utf-8") as f:
        translated_content = json.load(f)

    assert translated_content["url"] == "https://example.com"
    assert translated_content["headers"] == ["Example Title", "More Examples"]
    assert translated_content["paragraphs"] == ["This is a paragraph.", "Another paragraph."]

def test_translate_content_with_empty_paragraph(sample_raw_content, tmp_path):
    """Test translate_content function handles empty paragraphs."""

    with open(sample_raw_content, "r+", encoding="utf-8") as f:
        content = json.load(f)
        content["paragraphs"].append("  ")  
        f.seek(0)
        json.dump(content, f, ensure_ascii=False, indent=4)
        f.truncate()

    output_file = tmp_path / "translated_content.json"

    with patch("src.translation.translate.Translator") as MockTranslator:
        mock_translator = MockTranslator.return_value
        mock_translator.translate.side_effect = lambda text, src, dest: Mock(text=f"Translated {text.strip()}")

        translate_content(input_file=sample_raw_content, output_file=output_file)

    # validate translated content handles empty paragraphs
    with open(output_file, "r", encoding="utf-8") as f:
        translated_content = json.load(f)

    # checks that empty paragraphs are excluded
    assert len(translated_content["paragraphs"]) == 2
    assert "Translated  " not in translated_content["paragraphs"]

def test_translate_content_api_failure(sample_raw_content, tmp_path):
    """Test translate_content function handles API failure."""
    output_file = tmp_path / "translated_content.json"

    with patch("src.translation.translate.Translator") as MockTranslator:
        mock_translator = MockTranslator.return_value
        mock_translator.translate.side_effect = Exception("Mock translation API failure")

        translate_content(input_file=sample_raw_content, output_file=output_file)

    # output file should not exist due to failure
    assert not os.path.exists(output_file)
