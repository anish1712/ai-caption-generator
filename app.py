import streamlit as st
import requests
import urllib3
import base64

urllib3.disable_warnings()

st.set_page_config(page_title="ViralCaption AI", page_icon="🚀", layout="centered")

# --- Custom CSS ---
st.markdown("""
<style>
    div.stButton > button {
        background: linear-gradient(45deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 24px;
        font-size: 18px;
        font-weight: bold;
        width: 100%;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        box-shadow: 0px 4px 15px rgba(42, 82, 152, 0.6);
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
    /* Hide Streamlit Branding and GitHub Link */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- Translations Dictionary ---
translations = {
    "Gujarati": {
        "subtitle": "તમારા Instagram અને YouTube માટે વાયરલ કન્ટેન્ટ બનાવો!",
        "tabs": ["📸 Instagram Caption", "🔥 Viral Hashtags", "▶️ YouTube SEO", "🎬 Reels Script"],
        "t1_title": "### Instagram Caption Generator",
        "tone_select": "કેપ્શન કેવું હોવું જોઈએ?",
        "tones": ["Funny (રમુજી)", "Inspirational (પ્રેરણાદાયક)", "Attitude (સ્વેગ)", "Romantic (રોમેન્ટિક)"],
        "upload_label": "અહીં ફોટો અપલોડ કરો",
        "topic_label": "અથવા ફોટા વિશે લખો (દા.ત., 'ગોવા ટ્રિપ'):",
        "btn_generate": "Generate Caption ✨",
        "warn_empty": "ફોટો અપલોડ કરો અથવા વિષય લખો.",
        "spinner": "કેપ્શન બની રહ્યું છે... 🤖",
        "success": "કેપ્શન તૈયાર છે!",
        "t2_title": "### Trending Hashtags Generator",
        "hash_topic": "કયા વિષય પર હેશટેગ જોઈએ છે? (દા.ત., Fitness, Travel):",
        "btn_hash": "Generate Hashtags 🔥",
        "hash_spinner": "હેશટેગ્સ શોધી રહ્યા છીએ... 🤖",
        "hash_success": "હેશટેગ્સ તૈયાર છે!",
        "t3_title": "### YouTube Title & Description Maker",
        "yt_topic": "તમારો વિડીયો શેના વિશે છે? (દા.ત., 'iPhone 15 Review'):",
        "btn_yt": "Generate YouTube SEO 🚀",
        "yt_spinner": "SEO ડેટા બની રહ્યો છે... 🤖",
        "yt_success": "YouTube SEO તૈયાર છે!",
        "t4_title": "### Viral Reels Script Writer",
        "reel_topic": "રીલનો વિષય શું છે? (દા.ત., 'પૈસા બચાવવાની ૩ ટિપ્સ'):",
        "btn_reel": "Write Script 🎬",
        "reel_spinner": "સ્ક્રિપ્ટ લખાઈ રહી છે... 🤖",
        "reel_success": "તમારી સ્ક્રિપ્ટ તૈયાર છે!",
        "footer_seo_title": "About ViralCaption AI - The Ultimate Social Media Toolkit",
        "footer_seo_body": "**ViralCaption AI: Free Instagram Caption Generator & Content Maker**\nWelcome to ViralCaption AI, the ultimate tool for content creators! Whether you need a viral Instagram caption, trending hashtags, YouTube SEO optimization, or a Reels script, this free tool has you covered.\nSupported languages: Gujarati, Hindi, and English.",
        "footer_text": "Made with ❤️ to empower Creators"
    },
    "Hindi": {
        "subtitle": "अपने Instagram और YouTube के लिए वायरल कंटेंट बनाएं!",
        "tabs": ["📸 Instagram Caption", "🔥 Viral Hashtags", "▶️ YouTube SEO", "🎬 Reels Script"],
        "t1_title": "### Instagram Caption Generator",
        "tone_select": "कैप्शन का अंदाज़ कैसा होना चाहिए?",
        "tones": ["Funny (मज़ेदार)", "Inspirational (प्रेरणादायक)", "Attitude (स्वैग)", "Romantic (रोमांटिक)"],
        "upload_label": "यहाँ फोटो अपलोड करें",
        "topic_label": "या फोटो के बारे में लिखें (उदा., 'गोवा ट्रिप'):",
        "btn_generate": "Generate Caption ✨",
        "warn_empty": "कृपया फोटो अपलोड करें या विषय लिखें।",
        "spinner": "कैप्शन बन रहा है... 🤖",
        "success": "कैप्शन तैयार है!",
        "t2_title": "### Trending Hashtags Generator",
        "hash_topic": "किस विषय पर हैशटैग चाहिए? (उदा., Fitness, Travel):",
        "btn_hash": "Generate Hashtags 🔥",
        "hash_spinner": "हैशटैग खोजे जा रहे हैं... 🤖",
        "hash_success": "हैशटैग तैयार हैं!",
        "t3_title": "### YouTube Title & Description Maker",
        "yt_topic": "आपका वीडियो किस बारे में है? (उदा., 'iPhone 15 Review'):",
        "btn_yt": "Generate YouTube SEO 🚀",
        "yt_spinner": "SEO डेटा बन रहा है... 🤖",
        "yt_success": "YouTube SEO तैयार है!",
        "t4_title": "### Viral Reels Script Writer",
        "reel_topic": "रील का विषय क्या है? (उदा., 'पैसे बचाने के 3 टिप्स'):",
        "btn_reel": "Write Script 🎬",
        "reel_spinner": "स्क्रिप्ट लिखी जा रही है... 🤖",
        "reel_success": "आपकी स्क्रिप्ट तैयार है!",
        "footer_seo_title": "About ViralCaption AI - The Ultimate Social Media Toolkit",
        "footer_seo_body": "**ViralCaption AI: Free Instagram Caption Generator & Content Maker**\nWelcome to ViralCaption AI, the ultimate tool for content creators! Whether you need a viral Instagram caption, trending hashtags, YouTube SEO optimization, or a Reels script, this free tool has you covered.\nSupported languages: Gujarati, Hindi, and English.",
        "footer_text": "Made with ❤️ to empower Creators"
    },
    "English": {
        "subtitle": "Create viral content for your Instagram and YouTube!",
        "tabs": ["📸 Instagram Caption", "🔥 Viral Hashtags", "▶️ YouTube SEO", "🎬 Reels Script"],
        "t1_title": "### Instagram Caption Generator",
        "tone_select": "What should be the tone?",
        "tones": ["Funny", "Inspirational", "Attitude", "Romantic"],
        "upload_label": "Upload photo here",
        "topic_label": "Or describe the photo (e.g., 'Goa Trip'):",
        "btn_generate": "Generate Caption ✨",
        "warn_empty": "Please upload a photo or write a topic.",
        "spinner": "Generating caption... 🤖",
        "success": "Caption is ready!",
        "t2_title": "### Trending Hashtags Generator",
        "hash_topic": "Topic for hashtags? (e.g., Fitness, Travel):",
        "btn_hash": "Generate Hashtags 🔥",
        "hash_spinner": "Finding hashtags... 🤖",
        "hash_success": "Hashtags are ready!",
        "t3_title": "### YouTube Title & Description Maker",
        "yt_topic": "What is your video about? (e.g., 'iPhone 15 Review'):",
        "btn_yt": "Generate YouTube SEO 🚀",
        "yt_spinner": "Generating SEO data... 🤖",
        "yt_success": "YouTube SEO is ready!",
        "t4_title": "### Viral Reels Script Writer",
        "reel_topic": "What is the Reel about? (e.g., '3 tips to save money'):",
        "btn_reel": "Write Script 🎬",
        "reel_spinner": "Writing script... 🤖",
        "reel_success": "Your script is ready!",
        "footer_seo_title": "About ViralCaption AI - The Ultimate Social Media Toolkit",
        "footer_seo_body": "**ViralCaption AI: Free Instagram Caption Generator & Content Maker**\nWelcome to ViralCaption AI, the ultimate tool for content creators! Whether you need a viral Instagram caption, trending hashtags, YouTube SEO optimization, or a Reels script, this free tool has you covered.\nSupported languages: Gujarati, Hindi, and English.",
        "footer_text": "Made with ❤️ to empower Creators"
    }
}

# --- API Call Helper Function ---
def generate_ai_content(prompt, image_file=None):
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except KeyError:
        st.error("API Key મળી નથી! કૃપા કરીને Streamlit Settings માં Secrets એડ કરો.")
        return None
        
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-lite-latest:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    
    parts = [{"text": prompt}]
    
    if image_file:
        image_data = image_file.getvalue()
        base64_image = base64.b64encode(image_data).decode("utf-8")
        parts.append({
            "inline_data": {
                "mime_type": image_file.type,
                "data": base64_image
            }
        })
        
    data = {"contents": [{"parts": parts}]}
    
    try:
        response = requests.post(url, headers=headers, json=data, verify=False)
        result = response.json()
        if response.status_code == 200:
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            st.error(f"Google Error: {result}")
            return None
    except Exception as e:
        st.error(f"Network Error: {e}")
        return None


# --- Main Page ---
st.title("🚀 ViralCaption AI")

lang = st.selectbox("🌐 Select Language / ભાષા / भाषा", ["Gujarati", "Hindi", "English"])
t = translations[lang]

st.markdown(f"<p style='text-align: center; color: gray; font-size: 16px;'>{t['subtitle']}</p>", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(t["tabs"])

# --- TAB 1: Instagram Caption ---
with tab1:
    st.markdown(t["t1_title"])
    tone = st.selectbox(t["tone_select"], t["tones"], key="t1")
    col1, col2 = st.columns([1, 1])
    with col1:
        uploaded_file = st.file_uploader(t["upload_label"], type=["jpg", "jpeg", "png"], key="f1")
    with col2:
        topic = st.text_input(t["topic_label"], key="i1")

    if st.button(t["btn_generate"], key="b1"):
        if not uploaded_file and not topic:
            st.warning(t["warn_empty"])
        elif uploaded_file and uploaded_file.size > 10 * 1024 * 1024:
            st.error("ફોટાની સાઈઝ 10 MB થી વધારે છે.")
        else:
            if uploaded_file:
                st.image(uploaded_file, use_column_width=True)
            prompt = f"Write an engaging Instagram caption for this photo/topic. Topic: '{topic}'. Tone: {tone}. Include emojis and hashtags. Output language MUST be {lang}."
            with st.spinner(t["spinner"]):
                res = generate_ai_content(prompt, uploaded_file)
                if res:
                    st.success(t["success"])
                    st.info(res)

# --- TAB 2: Viral Hashtags ---
with tab2:
    st.markdown(t["t2_title"])
    hash_topic = st.text_input(t["hash_topic"])
    if st.button(t["btn_hash"], key="b2"):
        if not hash_topic:
            st.warning(t["warn_empty"])
        else:
            prompt = f"Generate 30 highly viral and trending Instagram hashtags for the topic: '{hash_topic}'. Group them into: High competition, Medium competition, and Niche hashtags. Output language: {lang}."
            with st.spinner(t["hash_spinner"]):
                res = generate_ai_content(prompt)
                if res:
                    st.success(t["hash_success"])
                    st.info(res)

# --- TAB 3: YouTube SEO ---
with tab3:
    st.markdown(t["t3_title"])
    yt_topic = st.text_input(t["yt_topic"])
    if st.button(t["btn_yt"], key="b3"):
        if not yt_topic:
            st.warning(t["warn_empty"])
        else:
            prompt = f"Act as an expert YouTube SEO manager. For a video about '{yt_topic}', provide: 1. Three catchy viral titles. 2. A SEO optimized YouTube description. 3. 15 relevant tags (comma separated). Output language MUST be {lang}."
            with st.spinner(t["yt_spinner"]):
                res = generate_ai_content(prompt)
                if res:
                    st.success(t["yt_success"])
                    st.info(res)

# --- TAB 4: Reels Script Writer ---
with tab4:
    st.markdown(t["t4_title"])
    reel_topic = st.text_input(t["reel_topic"])
    if st.button(t["btn_reel"], key="b4"):
        if not reel_topic:
            st.warning(t["warn_empty"])
        else:
            prompt = f"Write a 60-second highly engaging Instagram Reel script about '{reel_topic}'. Include an attention-grabbing hook (first 3 seconds), body content, and a strong Call to Action (CTA) at the end. Format it clearly with audio/visual cues. Output language MUST be {lang}."
            with st.spinner(t["reel_spinner"]):
                res = generate_ai_content(prompt)
                if res:
                    st.success(t["reel_success"])
                    st.info(res)

st.markdown("<br><hr>", unsafe_allow_html=True)

# --- SEO Section ---
with st.expander(t["footer_seo_title"]):
    st.write(t["footer_seo_body"])

st.markdown(f"<center>{t['footer_text']}</center>", unsafe_allow_html=True)
