import streamlit as st
import requests
import urllib3
import base64

urllib3.disable_warnings()

st.set_page_config(page_title="AI Caption Generator", page_icon="📸", layout="centered")

# --- Custom CSS for Premium Look ---
st.markdown("""
<style>
    div.stButton > button {
        background: linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 15px 32px;
        font-size: 20px;
        font-weight: bold;
        width: 100%;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        box-shadow: 0px 4px 15px rgba(220, 39, 67, 0.6);
        color: white;
        transform: translateY(-2px);
    }
    .block-container {
        padding-top: 2rem;
    }
    h1 {
        text-align: center;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
</style>
""", unsafe_allow_html=True)

translations = {
    "Gujarati": {
        "subtitle": "તમારા ફોટા માટે વાયરલ અને આકર્ષક કેપ્શન બનાવો! 🚀",
        "tone_select": "કેપ્શન કેવું હોવું જોઈએ?",
        "tones": ["Funny (રમુજી)", "Inspirational (પ્રેરણાદાયક)", "Attitude (સ્વેગ)", "Romantic (રોમેન્ટિક)"],
        "photo_label": "📸 તમારો ફોટો પસંદ કરો:",
        "upload_label": "અહીં ફોટો અપલોડ કરો",
        "topic_label": "અથવા ફોટા વિશે લખો (દા.ત., 'ગોવા ટ્રિપ'):",
        "btn_generate": "Generate Caption ✨",
        "warn_empty": "કૃપા કરીને ફોટો અપલોડ કરો અથવા ફોટા વિશે કંઈક લખો.",
        "err_size": "❌ તમારા ફોટાની સાઈઝ 10 MB થી વધારે છે. નાનો ફોટો અપલોડ કરો.",
        "caption_upload": "તમારો ફોટો",
        "spinner": "તમારું કેપ્શન બની રહ્યું છે... 🤖",
        "success": "તમારું કેપ્શન તૈયાર છે! નીચેથી કોપી કરી લો:",
        "footer": "<center>Made with ❤️ using AI</center>"
    },
    "Hindi": {
        "subtitle": "अपने फोटो के लिए वायरल और आकर्षक कैप्शन बनाएं! 🚀",
        "tone_select": "कैप्शन का अंदाज़ कैसा होना चाहिए?",
        "tones": ["Funny (मज़ेदार)", "Inspirational (प्रेरणादायक)", "Attitude (स्वैग)", "Romantic (रोमांटिक)"],
        "photo_label": "📸 अपना फोटो चुनें:",
        "upload_label": "यहाँ फोटो अपलोड करें",
        "topic_label": "या फोटो के बारे में लिखें (उदा., 'गोवा ट्रिप'):",
        "btn_generate": "Generate Caption ✨",
        "warn_empty": "कृपया फोटो अपलोड करें या कुछ लिखें।",
        "err_size": "❌ फोटो की साइज़ 10 MB से ज़्यादा है। छोटा फोटो अपलोड करें।",
        "caption_upload": "आपका फोटो",
        "spinner": "आपका कैप्शन बन रहा है... 🤖",
        "success": "आपका कैप्शन तैयार है! नीचे से कॉपी कर लें:",
        "footer": "<center>Made with ❤️ using AI</center>"
    },
    "English": {
        "subtitle": "Create viral and engaging captions for your photos! 🚀",
        "tone_select": "What should be the tone?",
        "tones": ["Funny", "Inspirational", "Attitude", "Romantic"],
        "photo_label": "📸 Select your photo:",
        "upload_label": "Upload photo here",
        "topic_label": "Or describe the photo (e.g., 'Goa Trip'):",
        "btn_generate": "Generate Caption ✨",
        "warn_empty": "Please upload a photo or write something.",
        "err_size": "❌ Photo exceeds 10 MB. Please upload a smaller photo.",
        "caption_upload": "Your photo",
        "spinner": "Generating your caption... 🤖",
        "success": "Your caption is ready! Copy it below:",
        "footer": "<center>Made with ❤️ using AI</center>"
    }
}

# --- Main Page ---
st.title("✨ AI Caption Generator")

lang = st.selectbox("🌐 Select Language / ભાષા / भाषा", ["Gujarati", "Hindi", "English"])
t = translations[lang]

st.markdown(f"<p style='text-align: center; color: gray; font-size: 18px;'>{t['subtitle']}</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

tone = st.selectbox(t["tone_select"], t["tones"])

st.markdown("---")
st.markdown(f"#### {t['photo_label']}")
col1, col2 = st.columns([1, 1])

with col1:
    uploaded_file = st.file_uploader(t["upload_label"], type=["jpg", "jpeg", "png"])
with col2:
    topic = st.text_input(t["topic_label"], "")

st.markdown("<br>", unsafe_allow_html=True)

# API Key ને કોડમાં લખવાને બદલે સિક્રેટ તરીકે લેવામાં આવશે
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except KeyError:
    st.error("API Key મળી નથી! કૃપા કરીને Streamlit Settings માં Secrets એડ કરો.")
    api_key = ""

if st.button(t["btn_generate"]):
    if not uploaded_file and not topic:
        st.warning(t["warn_empty"])
    elif uploaded_file and uploaded_file.size > 10 * 1024 * 1024:
        st.error(t["err_size"])
    else:
        st.markdown("---")
        if uploaded_file:
            st.image(uploaded_file, caption=t["caption_upload"], use_column_width=True)
            
        prompt = f"Write an engaging Instagram caption for this photo/topic. Topic description: '{topic}'. The tone should be {tone}. Include relevant trending hashtags and emojis. The output language MUST be {lang}."
        
        with st.spinner(t["spinner"]):
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-lite-latest:generateContent?key={api_key}"
            headers = {"Content-Type": "application/json"}
            
            parts = [{"text": prompt}]
            
            if uploaded_file:
                image_data = uploaded_file.getvalue()
                base64_image = base64.b64encode(image_data).decode("utf-8")
                parts.append({
                    "inline_data": {
                        "mime_type": uploaded_file.type,
                        "data": base64_image
                    }
                })
                
            data = {"contents": [{"parts": parts}]}
            
            try:
                response = requests.post(url, headers=headers, json=data, verify=False)
                result = response.json()
                
                if response.status_code == 200:
                    caption = result['candidates'][0]['content']['parts'][0]['text']
                    st.success(t["success"])
                    st.info(caption)
                else:
                    st.error(f"Google Error: {result}")
            except Exception as e:
                st.error(f"Network Error: {e}")

st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown(t["footer"], unsafe_allow_html=True)
