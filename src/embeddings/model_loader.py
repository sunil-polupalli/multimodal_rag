from sentence_transformers import SentenceTransformer
from PIL import Image

class EmbeddingModel:
    def __init__(self, model_name="clip-ViT-B-32"):
        self.model = SentenceTransformer(model_name)

    def get_text_embedding(self, text):
        return self.model.encode(text).tolist()

    def get_image_embedding(self, image_path):
        image = Image.open(image_path)
        return self.model.encode(image).tolist()