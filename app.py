import streamlit as st
from PIL import Image
import numpy as np
import pytesseract
import os
from clipboard_image import get_image_from_clipboard
from ocr_processor import OCRProcessor
from groq_translator import translate_text
from file_handler import save_translation
from content_filter import ContentFilter

def initialize_tesseract():
    """Initialize Tesseract with proper path based on environment"""
    if os.path.exists('/usr/bin/tesseract'):
        return '/usr/bin/tesseract'
    elif os.path.exists(r'C:\Program Files\Tesseract-OCR\tesseract.exe'):
        return r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    else:
        raise Exception("Tesseract not found. Please install Tesseract OCR.")

def main():
    st.title("OCR and Translation App")
    
    try:
        # Set up Tesseract path
        pytesseract.pytesseract.tesseract_cmd = initialize_tesseract()
        
        # Initialize content filter
        content_filter = ContentFilter()
        
        # Language selection
        target_language = st.radio(
            "Select target language",
            ["marathi", "english"],
            horizontal=True
        )
        
        # Use file uploader instead of clipboard for cloud deployment
        uploaded_file = st.file_uploader("Choose an image...", type=['png', 'jpg', 'jpeg'])
        
        if uploaded_file is not None:
            # Read the image
            image = Image.open(uploaded_file)
            
            # Convert to numpy array
            img_np = np.array(image)
            
            # Show the image
            st.image(image, caption="Uploaded Image", use_column_width=True)
            
            # Get best OCR result
            text, source = OCRProcessor.get_best_ocr_result(img_np)
            
            # Clean OCR text
            cleaned_text = content_filter.clean_text(text)
            
            # Display OCR result
            st.subheader(f"OCR Result ({source}):")
            st.text_area("Detected Text", cleaned_text, height=150)
            
            # Translate text
            if cleaned_text.strip():
                with st.spinner(f"Translating to {target_language}..."):
                    try:
                        translated_text = translate_text(cleaned_text, target_language)
                        st.subheader(f"Translated {target_language.capitalize()} Text:")
                        st.text_area("Translation", translated_text, height=150)
                        
                        # Save translation option
                        if st.button('Save Translation'):
                            save_translation(translated_text, f"{target_language}_translation.txt")
                            st.success(f"Translation saved to '{target_language}_translation.txt'")
                    except Exception as e:
                        st.error(f"Translation failed: {str(e)}")
            else:
                st.warning("No text detected in the image.")
    except Exception as e:
        st.error(f"Error initializing the application: {str(e)}")
        st.info("Please make sure Tesseract OCR is properly installed.")

if __name__ == "__main__":
    main()