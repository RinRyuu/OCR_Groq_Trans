from PIL import Image, ImageGrab
import streamlit as st

def get_image_from_clipboard():
    try:
        # Try grabbing the image from the clipboard
        image = ImageGrab.grabclipboard()

        # If there's an image, return it
        if isinstance(image, Image.Image):
            return image
        else:
            st.error("No image found in clipboard. Copy an image and try again.")
            return None
    except Exception as e:
        st.error(f"Error accessing clipboard: {e}")
        return None
