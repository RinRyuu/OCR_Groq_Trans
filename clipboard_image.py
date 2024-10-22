from PIL import Image
import streamlit as st

def get_image_from_clipboard():
    """Modified for cloud deployment to use file upload instead of clipboard"""
    uploaded_file = st.file_uploader("Choose an image...", type=['png', 'jpg', 'jpeg'])
    if uploaded_file is not None:
        return Image.open(uploaded_file)
    return None