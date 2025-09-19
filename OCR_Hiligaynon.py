import streamlit as st
from PIL import Image
import pytesseract
from streamlit_image_coordinates import streamlit_image_coordinates
from streamlit_tesseract_scanner import tesseract_scanner
import io
import os


st.title("Hiligaynon OCR Scanner")

st.write("Choose your input method to perform OCR on text in Hiligaynon (Filipino, English, Cebuano, Latin).")

option = st.radio("Select Input Method:", ("Upload Image and Select Region", "Use Camera Scanner"))

if option == "Upload Image and Select Region":
    st.subheader("Upload and Select Region")
    st.write("Upload a high-quality image, zoom and select a region, then perform OCR on the selected area.")

    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")
        st.subheader("Select Region (Zoom and Drag to Select)")
        # Use streamlit-image-coordinates for region selection
        result = streamlit_image_coordinates(
            image,
            key="ocr_img",
            width=700,
            height=500,
            display_coordinates=True,
            show_image_details=True,
            zoom=True,
            pan=True,
            box_mode="rect",
        )

        if result is not None and "rect" in result:
            rect = result["rect"]
            x, y, w, h = rect["x"], rect["y"], rect["w"], rect["h"]
            st.write(f"Selected region: x={x}, y={y}, w={w}, h={h}")

            # Crop the selected region
            cropped = image.crop((x, y, x + w, y + h))
            st.image(cropped, caption="Selected Region", use_column_width=True)

            if st.button("Perform OCR on Selected Region"):
                config = "--oem 3 --psm 6 -l eng+lat+ceb+fil"
                text = pytesseract.image_to_string(cropped, config=config)
                st.subheader("Extracted Text")
                st.code(text)
        else:
            st.info("Select a region to perform OCR.")
    else:
        st.info("Please upload an image to begin.")

elif option == "Use Camera Scanner":
    st.subheader("Camera Scanner")
    st.write("Use the camera to scan text. Note: This requires HTTPS.")

    blacklist = '@*|©_Ⓡ®¢§š'
    data = tesseract_scanner(showimg=False, lang='eng+ceb+lat+fil', blacklist=blacklist, psm=6)

    if data is not None:
        st.write("Extracted Text:")
        st.code(data)
    else:
        st.info("Scan an image to extract text.")