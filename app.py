import streamlit as st
from PIL import Image
import google.generativeai as genai
import json
import streamlit.components.v1 as components

st.set_page_config(page_title="कृषी-AI : स्मार्ट पीक डॉक्टर", page_icon="🌿", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Mukta:wght@500;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Mukta', sans-serif; }
.stApp { background: #F8FAFC; }
#MainMenu, footer, header { visibility: hidden; }
.k-hero { background: linear-gradient(135deg, #064E3B, #059669); border-radius: 16px; padding: 1.2rem; color: #fff; text-align: center; margin-bottom: 1.2rem; }
.res-card { background: #fff; border-radius: 14px; padding: 1.2rem; border: 1px solid #E2E8F0; margin-top: 1rem; box-shadow: 0 4px 12px rgba(0,0,0,0.03); }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="k-hero">
    <div style="font-size:12px;font-weight:700;color:#A7F3D0;letter-spacing:1px;">AVISHKAR 2026</div>
    <h2 style="margin:2px 0 0 0;font-size:1.6rem;font-weight:800;">🌿 कृषी-AI : थेट पीक डॉक्टर</h2>
    <p style="margin:4px 0 0 0;font-size:0.9rem;color:#D1FAE5;">फोटोवरून थेट सोयाबीन, कापूस व बटाटा रोग निदान</p>
</div>
""", unsafe_allow_html=True)

# API KEY इनपुट (Secrets मधून किंवा थेट स्क्रीनवरून)
secret_key = st.secrets.get("GEMINI_API_KEY", "")
api_key = st.text_input("🔑 तुमची Gemini API Key येथे पेस्ट करा:", value=secret_key, type="password")

if not api_key:
    st.warning("⚠️ कृपया वरील बॉक्समध्ये तुमची नवीन Gemini API Key पेस्ट करा.")
    st.stop()

genai.configure(api_key=api_key.strip())

uploaded_file = st.file_uploader("पानाचा किंवा पिकाचा फोटो अपलोड करा:", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file:
    img = Image.open(uploaded_file).convert("RGB")
    st.image(img, caption="अपलोड केलेला फोटो", use_container_width=True)

    if st.button("🔍 AI द्वारे थेट रोग व पीक निदान करा", type="primary", use_container_width=True):
        with st.spinner("AI सखोल परीक्षण करत आहे..."):
            prompt = """
            तुम्ही वरिष्ठ कृषी तज्ज्ञ आहात. या पानाचे/झाडाचे अचूक परीक्षण करून शुद्ध मराठीत उत्तर द्या:
            १. पीक कोणते आहे? (सोयाबीन असल्यास स्पष्ट सोयाबीन म्हणा, कापूस किंवा बटाटा असल्यास ते सांगा).
            २. पानाची स्थिती: निरोगी की रोगट?
            ३. रोग/कीड: नाव काय?
            ४. लक्षणे काय दिसत आहेत?
            ५. रासायनिक फवारणी: औषध व प्रमाण (प्रति १५ लिटर पंप).
            ६. सेंद्रिय उपाय.
            """

            try:
                # Direct vision model
                model = genai.GenerativeModel('gemini-1.5-flash')
                res = model.generate_content([prompt, img])
                st.markdown("<div class='res-card'>", unsafe_allow_html=True)
                st.markdown(res.text)
                st.markdown("</div>", unsafe_allow_html=True)

                # ऑडिओ
                audio_snippet = res.text[:200].replace("*", "").replace("\n", " ")
                a_js = json.dumps(audio_snippet)
                a_html = f'<script>function spk(){{window.speechSynthesis.cancel();var m=new SpeechSynthesisUtterance({a_js});m.lang="mr-IN";window.speechSynthesis.speak(m);}}</script><button onclick="spk()" style="width:100%;margin-top:12px;background:linear-gradient(135deg,#059669,#10b981);color:#fff;border:none;padding:12px;border-radius:12px;font-weight:700;cursor:pointer;">🔊 ऑडिओ सल्ला ऐका</button>'
                components.html(a_html, height=54)

            except Exception as e:
                st.error(f"❌ गुगल सर्व्हरकडून आलेला खरा संदेश: {e}")
                
