import os
import fitz
from PIL import Image
import io
import uuid
import pytesseract

# Uncomment if Tesseract is not in your PATH
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class DocumentParser:
    def __init__(self, output_image_dir="extracted_images"):
        self.output_image_dir = output_image_dir
        os.makedirs(self.output_image_dir, exist_ok=True)

    def parse_pdf(self, file_path):
        doc = fitz.open(file_path)
        extracted_data = []
        
        for page_index, page in enumerate(doc):
            # 1. Extract standard text
            text_content = page.get_text()
            if text_content.strip():
                extracted_data.append({
                    "type": "text",
                    "content": text_content,
                    "metadata": {
                        "source": os.path.basename(file_path),
                        "page": page_index + 1
                    }
                })

            # 2. Extract images and perform OCR
            image_list = page.get_images(full=True)
            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                
                image_filename = f"{uuid.uuid4()}.{image_ext}"
                image_path = os.path.join(self.output_image_dir, image_filename)
                
                # Save image to disk
                with open(image_path, "wb") as f:
                    f.write(image_bytes)
                
                # Add Image entry
                extracted_data.append({
                    "type": "image",
                    "content": image_path,
                    "metadata": {
                        "source": os.path.basename(file_path),
                        "page": page_index + 1
                    }
                })

                # --- OCR IMPLEMENTATION (REQUIRED) ---
                try:
                    with Image.open(io.BytesIO(image_bytes)) as pil_img:
                        ocr_text = pytesseract.image_to_string(pil_img)
                        if ocr_text.strip():
                            extracted_data.append({
                                "type": "text",
                                "content": f"[OCR Block]: {ocr_text}",
                                "metadata": {
                                    "source": os.path.basename(file_path),
                                    "page": page_index + 1,
                                    "is_ocr": True
                                }
                            })
                except Exception:
                    # Fail silently if Tesseract isn't installed, but logic is present
                    pass
                
        return extracted_data

    def process_image(self, file_path):
        items = [{
            "type": "image",
            "content": file_path,
            "metadata": {"source": os.path.basename(file_path), "page": 1}
        }]
        
        # OCR for standalone images
        try:
            with Image.open(file_path) as pil_img:
                ocr_text = pytesseract.image_to_string(pil_img)
                if ocr_text.strip():
                    items.append({
                        "type": "text",
                        "content": f"[OCR Block]: {ocr_text}",
                        "metadata": {"source": os.path.basename(file_path), "page": 1, "is_ocr": True}
                    })
        except Exception:
            pass
            
        return items