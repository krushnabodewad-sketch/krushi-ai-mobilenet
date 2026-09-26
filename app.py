import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np

st.set_page_config(page_title="कृषी-AI : MobileNetV2", page_icon="🌿", layout="centered")

st.markdown("""
<div style="background: linear-gradient(135deg, #064E3B, #059669); border-radius: 16px; padding: 1.2rem; color: #fff; text-align: center; margin-bottom: 1.5rem;">
    <h2 style="margin: 0; font-size: 1.5rem;">🌿 कृषी-AI : स्मार्ट पीक रोग निदान</h2>
    <p style="margin: 5px 0 0 0; font-size: 0.85rem; color: #D1FAE5;">MobileNetV2 Lightweight Offline Engine</p>
</div>
""", unsafe_allow_html=True)

# १५ क्लासेसची यादी थेट कोडमध्ये समाविष्ट
CLASS_NAMES = [
    "Pepper__bell___Bacterial_spot", 
    "Pepper__bell___healthy", 
    "Potato___Early_blight", 
    "Potato___Late_blight", 
    "Potato___healthy", 
    "Tomato_Bacterial_spot", 
    "Tomato_Early_blight", 
    "Tomato_Late_blight", 
    "Tomato_Leaf_Mold", 
    "Tomato_Septoria_leaf_spot", 
    "Tomato_Spider_mites_Two_spotted_spider_mite", 
    "Tomato__Target_Spot", 
    "Tomato__Tomato_YellowLeaf__Curl_Virus", 
    "Tomato__Tomato_mosaic_virus", 
    "Tomato_healthy"
]

@st.cache_resource
def load_unified_model():
    model = tf.keras.models.load_model("krushi_mobilenetv2_ready.h5", compile=False)
    return model

try:
    model = load_unified_model()
    model_ready = True
except Exception as e:
    model_ready = False
    st.error(f"मॉडेल लोड करताना त्रुटी आली: {e}")

up_file = st.file_uploader("पानाचा फोटो निवडा किंवा अपलोड करा:", type=["jpg", "jpeg", "png", "webp"])

if up_file and model_ready:
    img = Image.open(up_file).convert("RGB")
    st.image(img, caption="अपलोड केलेले पान", use_container_width=True)

    # Preprocessing
    resized = img.resize((224, 224))
    arr = np.expand_dims(np.array(resized, dtype=np.float32), axis=0)

    # Prediction
    with st.spinner("निदान सुरू आहे..."):
        preds = model(arr, training=False).numpy()[0]
        idx = int(np.argmax(preds))
        conf = float(preds[idx]) * 100
        detected_class = CLASS_NAMES[idx]

    # Out of Scope / Unrecognized Gate
    if "Tomato" in detected_class or "Pepper" in detected_class:
        st.warning(f"⚠️ **अनोळखी वनस्पती / इतर पीक (Out of Scope)**\n\nहे पान **{detected_class.split('___')[0].replace('_', ' ')}** चे दिसते. कृषी-AI सध्या बटाटा पिकासाठी प्रमाणित आहे.")
    else:
        clean_name = detected_class.replace("___", " ").replace("_", " ")
        st.success(f"✅ **अचूक निदान:** {clean_name}")
        st.metric("विश्वास गुण (Confidence)", f"{conf:.2f}%")

    with st.expander("📊 सविस्तर वर्गीकरण (Detailed Class Probabilities)"):
        top_indices = np.argsort(preds)[::-1][:5]
        for i in top_indices:
            c_name = CLASS_NAMES[i].replace("___", " ").replace("_", " ")
            st.write(f"• **{c_name}**: `{float(preds[i])*100:.1f}%`")
            
