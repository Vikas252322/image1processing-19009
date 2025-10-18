import streamlit as st
from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import io

# 🛠️ Page setup
st.set_page_config(page_title="Vikas Bhosale 19009 Image Processing Project", layout="centered")
st.title("🖼️ Vikas Bhosale 19009 Image Processing Project")
st.write("Upload an image and apply multiple filters with adjustable intensity.")

# 📤 Upload image
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

# 🎨 Sepia filter
def apply_sepia(img):
    sepia = ImageOps.colorize(ImageOps.grayscale(img), '#704214', '#C0A080')
    return sepia.convert("RGB")

# 🧼 Session state defaults
defaults = {
    "grayscale": False, "negative": False, "sepia": False,
    "detail": False, "edge_enhance": False,
    "brightness": 1.0, "contrast": 1.0, "sharpness": 1.0, "blur": 0.0,
    "layout": "Side-by-Side", "download_format": "PNG",
    "preset": "None", "rotate": 0, "crop_style": "None"
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# 🔄 Reset button
if st.button("🔄 Reset Filters"):
    for key, val in defaults.items():
        st.session_state[key] = val

# 🖼️ Image processing
if uploaded_file:
    try:
        original_image = Image.open(uploaded_file).convert("RGB")
    except Exception as e:
        st.error("⚠️ Failed to load image. Please upload a valid JPG or PNG file.")
    else:
        filtered_img = original_image

        # 🎛️ Sidebar controls
        st.sidebar.header("Choose Filters")
        st.session_state["preset"] = st.sidebar.selectbox("Filter Presets", ["None", "Warm Glow", "Cool Contrast", "Sharp & Bright"])

        if st.session_state["preset"] == "Warm Glow":
            st.session_state.update({"sepia": True, "brightness": 1.3, "contrast": 1.2, "sharpness": 1.0, "blur": 0.0})
        elif st.session_state["preset"] == "Cool Contrast":
            st.session_state.update({"sepia": False, "brightness": 0.9, "contrast": 1.5, "sharpness": 1.2, "blur": 0.0})
        elif st.session_state["preset"] == "Sharp & Bright":
            st.session_state.update({"sepia": False, "brightness": 1.4, "contrast": 1.1, "sharpness": 2.0, "blur": 0.0})

        st.session_state["grayscale"] = st.sidebar.checkbox("Grayscale", value=st.session_state["grayscale"])
        st.session_state["negative"] = st.sidebar.checkbox("Negative", value=st.session_state["negative"])
        st.session_state["sepia"] = st.sidebar.checkbox("Sepia", value=st.session_state["sepia"])
        st.session_state["detail"] = st.sidebar.checkbox("Detail", value=st.session_state["detail"])
        st.session_state["edge_enhance"] = st.sidebar.checkbox("Edge Enhance", value=st.session_state["edge_enhance"])

        st.session_state["brightness"] = st.sidebar.slider("Brightness", 0.5, 2.0, st.session_state["brightness"])
        st.session_state["contrast"] = st.sidebar.slider("Contrast", 0.5, 2.0, st.session_state["contrast"])
        st.session_state["sharpness"] = st.sidebar.slider("Sharpness", 0.5, 3.0, st.session_state["sharpness"])
        st.session_state["blur"] = st.sidebar.slider("Blur", 0.0, 5.0, st.session_state["blur"])

        st.session_state["layout"] = st.sidebar.radio("Comparison Layout", ["Side-by-Side", "Vertical"])
        st.session_state["download_format"] = st.sidebar.selectbox("Download Format", ["PNG", "JPEG", "BMP"])

        st.sidebar.header("Crop & Rotate")
        st.session_state["crop_style"] = st.sidebar.selectbox("Crop Style", ["None", "Center Square", "Top Half", "Bottom Half", "Left Half", "Right Half"])
        st.session_state["rotate"] = st.sidebar.selectbox("Rotate", [0, 90, 180, 270])

        # 🧪 Apply filters
        if st.session_state["grayscale"]:
            filtered_img = ImageOps.grayscale(filtered_img).convert("RGB")
        if st.session_state["negative"]:
            filtered_img = ImageOps.invert(filtered_img)
        if st.session_state["sepia"]:
            filtered_img = apply_sepia(filtered_img)

        filtered_img = ImageEnhance.Brightness(filtered_img).enhance(st.session_state["brightness"])
        filtered_img = ImageEnhance.Contrast(filtered_img).enhance(st.session_state["contrast"])
        filtered_img = ImageEnhance.Sharpness(filtered_img).enhance(st.session_state["sharpness"])

        if st.session_state["blur"] > 0:
            filtered_img = filtered_img.filter(ImageFilter.GaussianBlur(radius=st.session_state["blur"]))
        if st.session_state["detail"]:
            filtered_img = filtered_img.filter(ImageFilter.DETAIL)
        if st.session_state["edge_enhance"]:
            filtered_img = filtered_img.filter(ImageFilter.EDGE_ENHANCE)

        if st.session_state["rotate"] != 0:
            filtered_img = filtered_img.rotate(-st.session_state["rotate"], expand=True)

        # ✂️ Apply crop style
        width, height = filtered_img.size
        style = st.session_state["crop_style"]

        if style == "Center Square":
            side = min(width, height)
            left = (width - side) // 2
            top = (height - side) // 2
            filtered_img = filtered_img.crop((left, top, left + side, top + side))
        elif style == "Top Half":
            filtered_img = filtered_img.crop((0, 0, width, height // 2))
        elif style == "Bottom Half":
            filtered_img = filtered_img.crop((0, height // 2, width, height))
        elif style == "Left Half":
            filtered_img = filtered_img.crop((0, 0, width // 2, height))
        elif style == "Right Half":
            filtered_img = filtered_img.crop((width // 2, 0, width, height))

        # 🖼 Display comparison
        st.write("### Image Comparison")
        if st.session_state["layout"] == "Side-by-Side":
            col1, col2 = st.columns(2)
            with col1:
                st.image(original_image, caption="🖼 Original Image", use_container_width=True)
            with col2:
                st.image(filtered_img, caption="✨ Edited Image", use_container_width=True)
        else:
            st.image(original_image, caption="🖼 Original Image", use_container_width=True)
            st.image(filtered_img, caption="✨ Edited Image", use_container_width=True)

        # 💾 Download
        buf = io.BytesIO()
        filtered_img.save(buf, format=st.session_state["download_format"])
        byte_im = buf.getvalue()

        st.download_button(
            label=f"Download Edited Image ({st.session_state['download_format']})",
            data=byte_im,
            file_name=f"edited_image.{st.session_state['download_format'].lower()}",
            mime=f"image/{st.session_state['download_format'].lower()}"
        )
