import streamlit as st
import requests
import urllib3
import base64

urllib3.disable_warnings()

st.set_page_config(page_title="AI Social Media Toolkit", page_icon="🚀", layout="centered")

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
</style>
""", unsafe_allow_html=True)

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
st.title("🚀 AI Social Media Toolkit")
st.markdown("<p style='text-align: center; color: gray; font-size: 16px;'>તમારા Instagram અને YouTube માટે વાયરલ કન્ટેન્ટ બનાવો!</p>", unsafe_allow_html=True)

lang = st.selectbox("🌐 Select Language / ભાષા / भाषा", ["Gujarati", "Hindi", "English"])

# Tabs બનાવ્યા
tab1, tab2, tab3, tab4 = st.tabs(["📸 Instagram Caption", "🔥 Viral Hashtags", "▶️ YouTube SEO", "🎬 Reels Script"])

# --- TAB 1: Instagram Caption ---
with tab1:
    st.markdown("### Instagram Caption Generator")
    tone = st.selectbox("કેપ્શન કેવું હોવું જોઈએ?", ["Funny (રમુજી)", "Inspirational (પ્રેરણાદાયક)", "Attitude (સ્વેગ)", "Romantic (રોમેન્ટિક)"], key="t1")
    col1, col2 = st.columns([1, 1])
    with col1:
        uploaded_file = st.file_uploader("અહીં ફોટો અપલોડ કરો", type=["jpg", "jpeg", "png"], key="f1")
    with col2:
        topic = st.text_input("અથવા ફોટા વિશે લખો (દા.ત., 'ગોવા ટ્રિપ'):", key="i1")

    if st.button("Generate Caption ✨", key="b1"):
        if not uploaded_file and not topic:
            st.warning("ફોટો અપલોડ કરો અથવા વિષય લખો.")
        elif uploaded_file and uploaded_file.size > 10 * 1024 * 1024:
            st.error("ફોટાની સાઈઝ 10 MB થી વધારે છે.")
        else:
            if uploaded_file:
                st.image(uploaded_file, use_column_width=True)
            prompt = f"Write an engaging Instagram caption for this photo/topic. Topic: '{topic}'. Tone: {tone}. Include emojis and hashtags. Output language MUST be {lang}."
            with st.spinner("કેપ્શન બની રહ્યું છે... 🤖"):
                res = generate_ai_content(prompt, uploaded_file)
                if res:
                    st.success("કેપ્શન તૈયાર છે!")
                    st.info(res)

# --- TAB 2: Viral Hashtags ---
with tab2:
    st.markdown("### Trending Hashtags Generator")
    hash_topic = st.text_input("કયા વિષય પર હેશટેગ જોઈએ છે? (દા.ત., Fitness, Travel, Food):")
    if st.button("Generate Hashtags 🔥", key="b2"):
        if not hash_topic:
            st.warning("કૃપા કરીને વિષય લખો.")
        else:
            prompt = f"Generate 30 highly viral and trending Instagram hashtags for the topic: '{hash_topic}'. Group them into: High competition, Medium competition, and Niche hashtags. Output language: {lang}."
            with st.spinner("હેશટેગ્સ શોધી રહ્યા છીએ... 🤖"):
                res = generate_ai_content(prompt)
                if res:
                    st.success("હેશટેગ્સ તૈયાર છે!")
                    st.info(res)

# --- TAB 3: YouTube SEO ---
with tab3:
    st.markdown("### YouTube Title & Description Maker")
    yt_topic = st.text_input("તમારો વિડીયો શેના વિશે છે? (દા.ત., 'iPhone 15 Review', 'Vlog'):")
    if st.button("Generate YouTube SEO 🚀", key="b3"):
        if not yt_topic:
            st.warning("કૃપા કરીને વિડિયોનો વિષય લખો.")
        else:
            prompt = f"Act as an expert YouTube SEO manager. For a video about '{yt_topic}', provide: 1. Three catchy viral titles. 2. A SEO optimized YouTube description. 3. 15 relevant tags (comma separated). Output language MUST be {lang}."
            with st.spinner("SEO ડેટા બની રહ્યો છે... 🤖"):
                res = generate_ai_content(prompt)
                if res:
                    st.success("YouTube SEO તૈયાર છે!")
                    st.info(res)

# --- TAB 4: Reels Script Writer ---
with tab4:
    st.markdown("### Viral Reels Script Writer")
    reel_topic = st.text_input("રીલનો વિષય શું છે? (દા.ત., 'પૈસા બચાવવાની ૩ ટિપ્સ'):")
    if st.button("Write Script 🎬", key="b4"):
        if not reel_topic:
            st.warning("કૃપા કરીને વિષય લખો.")
        else:
            prompt = f"Write a 60-second highly engaging Instagram Reel script about '{reel_topic}'. Include an attention-grabbing hook (first 3 seconds), body content, and a strong Call to Action (CTA) at the end. Format it clearly with audio/visual cues. Output language MUST be {lang}."
            with st.spinner("સ્ક્રિપ્ટ લખાઈ રહી છે... 🤖"):
                res = generate_ai_content(prompt)
                if res:
                    st.success("તમારી સ્ક્રિપ્ટ તૈયાર છે!")
                    st.info(res)

st.markdown("<br><hr>", unsafe_allow_html=True)

# --- SEO Section (આ લખાણ Google સર્ચમાં સાઇટને ઉપર લાવવામાં મદદ કરશે) ---
with st.expander("About this AI Social Media Toolkit"):
    st.write("""
    **Free AI Instagram Caption Generator & Social Media Toolkit**  
    Welcome to the ultimate AI tool for content creators! Whether you need a viral Instagram caption, trending hashtags, YouTube SEO optimization (titles and descriptions), or a highly engaging Reels script, this free tool has you covered.
    
    Supported languages: Gujarati, Hindi, and English. Grow your social media presence faster with our AI-powered features!
    """)

st.markdown("<center>Made with ❤️ to empower Creators</center>", unsafe_allow_html=True)
