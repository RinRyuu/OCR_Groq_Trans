# import streamlit as st
# from PIL import Image
# import numpy as np
# import pytesseract
# from clipboard_image import get_image_from_clipboard  # Fixed import
# from ocr_processor import OCRProcessor
# from groq_translator import translate_text
# from file_handler import save_translation

# def main():
#     st.title("OCR and Translation App")
    
#     # Set up Tesseract path
#     pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    
#     # Language selection
#     target_language = st.radio(
#         "Select target language",
#         ["marathi", "english"],
#         horizontal=True
#     )
    
#     # Image input
#     if st.button('Paste Image from Clipboard'):
#         image = get_image_from_clipboard()
        
#         if image is not None:
#             # Convert to numpy array
#             img_np = np.array(image)
            
#             # Show the image
#             st.image(image, caption="Uploaded Image", use_column_width=True)
            
#             # Get best OCR result
#             text, source = OCRProcessor.get_best_ocr_result(img_np)
            
#             # Display OCR result
#             st.subheader(f"OCR Result ({source}):")
#             st.text_area("Detected Text", text, height=150)
            
#             # Translate text
#             if text.strip():
#                 with st.spinner(f"Translating to {target_language}..."):
#                     try:
#                         translated_text = translate_text(text, target_language)
#                         st.subheader(f"Translated {target_language.capitalize()} Text:")
#                         st.text_area("Translation", translated_text, height=150)
                        
#                         # Save translation option
#                         if st.button('Save Translation'):
#                             save_translation(translated_text, f"{target_language}_translation.txt")
#                             st.success(f"Translation saved to '{target_language}_translation.txt'")
#                     except Exception as e:
#                         st.error(f"Translation failed: {str(e)}")
#             else:
#                 st.warning("No text detected in the image.")
#     else:
#         st.write("Click the button above to paste an image from your clipboard.")

# if __name__ == "__main__":
#     main()
import streamlit as st
from PIL import Image
import numpy as np
import pytesseract
from clipboard_image import get_image_from_clipboard
from ocr_processor import OCRProcessor
from groq_translator import translate_text
from file_handler import save_translation
from content_filter import ContentFilter

def main():
    st.title("OCR and Translation App")
    
    # Initialize content filter
    content_filter = ContentFilter()
    
    # Set up Tesseract path
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    
    # Language selection
    target_language = st.radio(
        "Select target language",
        ["marathi", "english"],
        horizontal=True
    )
    
    # Image input
    if st.button('Paste Image from Clipboard'):
        image = get_image_from_clipboard()
        
        if image is not None:
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
    else:
        st.write("Click the button above to paste an image from your clipboard.")

if __name__ == "__main__":
    main()