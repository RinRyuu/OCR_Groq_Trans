
import cv2
import numpy as np
from PIL import Image
import pytesseract
from typing import Tuple

class OCRProcessor:
    @staticmethod
    def preprocess_image(img: np.ndarray) -> np.ndarray:
        """Preprocess image for better OCR results."""
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        return thresh

    @staticmethod
    def perform_ocr(img_np: np.ndarray) -> str:
        """Perform OCR on the image."""
        img_pil = Image.fromarray(img_np)
        text = pytesseract.image_to_string(img_pil, lang='hin')
        return text

    @staticmethod
    def get_best_ocr_result(img_np: np.ndarray) -> Tuple[str, str]:
        """Compare OCR results from original and preprocessed images."""
        original_text = OCRProcessor.perform_ocr(img_np)
        preprocessed = OCRProcessor.preprocess_image(img_np)
        preprocessed_text = OCRProcessor.perform_ocr(preprocessed)
        
        return (preprocessed_text, "preprocessed") if len(preprocessed_text) > len(original_text) \
            else (original_text, "original")