import os
import pytest
from src.ingestion.document_parser import DocumentParser

def test_parse_pdf_structure():
    parser = DocumentParser(output_image_dir="tests/test_images")
    if not os.path.exists("tests/test_images"):
        os.makedirs("tests/test_images")
    
    assert os.path.exists(parser.output_image_dir)
    
    if os.path.exists("tests/test_images"):
        for file in os.listdir("tests/test_images"):
            os.remove(os.path.join("tests/test_images", file))
        os.rmdir("tests/test_images")

def test_process_image_structure():
    parser = DocumentParser()
    dummy_image_path = "dummy.jpg"
    with open(dummy_image_path, "w") as f:
        f.write("dummy content")
    
    result = parser.process_image(dummy_image_path)
    
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["type"] == "image"
    assert result[0]["content"] == dummy_image_path
    
    os.remove(dummy_image_path)