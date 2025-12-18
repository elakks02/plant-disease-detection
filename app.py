import streamlit as st
from streamlit_option_menu import option_menu
from ultralytics import YOLO
from PIL import Image
import json, os, requests
from io import BytesIO
from deep_translator import GoogleTranslator, LibreTranslator
from gtts import gTTS
import feedparser   # for Google News RSS
import base64



# ---------------- APP STYLING ----------------
st.markdown(
    """
    <style>
    .stApp {
        background-attachment: fixed;
        background-size: cover
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Function to set background image
def add_bg_from_local(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-attachment: fixed;
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ✅ Since background.jpg is in the same folder as app.py
add_bg_from_local("bg2.jpg")

# ----------- Utils (from your utils.py & chatbot.py assumed) -----------
from utils import get_organic_solution, generate_report
from chatbot import plant_chatbot

# Load trained YOLOv8 model
MODEL_PATH = "runs/detect/train2/weights/best.pt"
model = YOLO(MODEL_PATH)

# ---------------- TRANSLATION ----------------
LANGUAGES = {
    "English": "en",
    "Tamil": "ta",
    "Hindi": "hi",
    "Telugu": "te",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Bengali": "bn",
    "Marathi": "mr",
    "Gujarati": "gu",
}

def translate_text(text, target_lang):
    try:
        if not text:
            return ""
        return GoogleTranslator(source="auto", target=target_lang).translate(text)
    except:
        try:
            return LibreTranslator(source="auto", target=target_lang).translate(text)
        except:
            return text  

# ---------------- TTS ----------------
def tts_audio(text, lang_code):
    if not text.strip():
        return None
    mp3_fp = BytesIO()
    try:
        gTTS(text=text, lang=lang_code, slow=False).write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        return mp3_fp
    except:
        return None

# ---------------- SIDEBAR MENU ----------------
with st.sidebar:
    selected = option_menu(
        menu_title="🌱 Uzhavar Connect",
        options=["Home", "Prediction", "Chatbot", "Weather", "Farmer News", "Crop Advisory", "Government Schemes", "Community","Farmer Tools", "History", "About"],
        icons=["house", "camera", "chat-dots", "cloud-sun", "newspaper", "heart", "people", "clock-history", "info-circle","info-circle"],
        menu_icon="leaf",
        default_index=0,
    )
    target_language = st.selectbox("🌍 Choose Language", list(LANGUAGES.keys()), index=0)
    lang_code = LANGUAGES[target_language]

# ---------------- HOME ---------------- #
if selected == "Home":
    st.title("🌿 Uzhavar Connect")
    st.write("An AI-powered assistant for farmers: detect plant diseases, get solutions, check weather, news, and share with community.")


# ----------------- FARMER TOOLS -----------------
elif selected == "Farmer Tools":
    st.title("🛠 Farmer Tools & Equipment")
    st.write("Find easy-to-use tools based on your needs.")

    categories = {
        "Irrigation": [
            {"name": "Drip Irrigation Kit", "desc": "Saves water and improves crop yield.", "image": "https://i.imgur.com/JG2cK2v.jpg"},
            {"name": "Solar Water Pump", "desc": "Eco-friendly pump for irrigation.", "image": "https://i.imgur.com/Y6hUVwc.jpg"}
        ],
        "Soil & Fertilizer": [
            {"name": "Soil pH Tester", "desc": "Quick test for soil acidity/alkalinity.", "image": "https://i.imgur.com/umqzOj0.jpg"},
            {"name": "Organic Fertilizer Spreader", "desc": "Distributes fertilizer evenly.", "image": "https://i.imgur.com/AmBlwnE.jpg"}
        ],
        "Harvesting": [
            {"name": "Hand Sickle", "desc": "Traditional tool for harvesting crops.", "image": "https://i.imgur.com/UxjvG5H.jpg"},
            {"name": "Mini Harvester", "desc": "Compact harvester for small farms.", "image": "https://i.imgur.com/QudJgmL.jpg"}
        ],
        "Pest Control": [
            {"name": "Hand Sprayer", "desc": "For spraying pesticides and fertilizers.", "image": "https://i.imgur.com/xgprIKU.jpg"},
            {"name": "Drone Sprayer", "desc": "Automated spraying for large fields.", "image": "https://i.imgur.com/a1A4bkk.jpg"}
        ],
        "Storage & Processing": [
            {"name": "Solar Grain Dryer", "desc": "Dries grains using solar energy.", "image": "https://i.imgur.com/dcUGlI7.jpg"},
            {"name": "Grain Storage Bin", "desc": "Safe storage for harvested grains.", "image": "https://i.imgur.com/0VG45gO.jpg"}
        ]
    }

    choice = st.selectbox("🔍 Select a Category", list(categories.keys()))

    st.subheader(f"📂 {choice} Tools")
    for tool in categories[choice]:
        with st.container():
            st.image(tool["image"], width=250)
            st.markdown(f"### {tool['name']}")
            st.write(tool["desc"])
            st.markdown("---")

# ----------------- COMMUNITY -----------------
elif selected == "Community":
    st.title("👥 Uzhavar Community")
    st.write("Connect with other farmers, share your ideas, tips, and experiences.")

    COMMUNITY_FILE = "community.json"

    # Load existing posts
    if os.path.exists(COMMUNITY_FILE):
        with open(COMMUNITY_FILE, "r", encoding="utf-8") as f:
            community_posts = json.load(f)
    else:
        community_posts = []

    # ---------------- Create a New Post ----------------
    st.subheader("✍️ Share your thoughts")
    name = st.text_input("👤 Your Name")
    message = st.text_area("💬 Your Message")
    photo = st.file_uploader("📸 Upload Image (optional)", type=["jpg", "jpeg", "png"])

    if st.button("Post"):
        if name.strip() and message.strip():
            post = {
                "name": name,
                "message": message,
                "image": None
            }
            if photo:
                img_bytes = photo.read()
                img_b64 = base64.b64encode(img_bytes).decode("utf-8")
                post["image"] = img_b64

            community_posts.insert(0, post)
            with open(COMMUNITY_FILE, "w", encoding="utf-8") as f:
                json.dump(community_posts, f, ensure_ascii=False, indent=4)

            st.success("✅ Post shared successfully!")
            st.rerun()
        else:
            st.warning("⚠ Please enter your name and a message before posting.")

    # ---------------- Display Community Feed ----------------
    st.subheader("🌍 Community Feed")
    if community_posts:
        for post in community_posts:
            with st.container():
                st.markdown(f"**👤 {post['name']}** says:")
                st.write(post['message'])

                # 🌍 Translation
                translated_msg = translate_text(post['message'], lang_code)
                if translated_msg and translated_msg != post['message']:
                    st.info(f"🌍 {target_language} Translation: {translated_msg}")

                # 🔊 Read aloud
                if st.button(f"🔊 Read {post['name']}'s Post", key=post['name']+post['message']):
                    audio = tts_audio(translated_msg, lang_code)
                    if audio:
                        st.audio(audio, format="audio/mp3")

                if post["image"]:
                    img_bytes = base64.b64decode(post["image"])
                    st.image(img_bytes, use_container_width=True)

                st.write("---")
    else:
        st.info("No posts yet. Be the first to share something!")




# ---------------- PREDICTION ---------------- #
elif selected == "Prediction":
    st.header("🩺 Disease Prediction")
    uploaded_file = st.file_uploader("📸 Upload a leaf image", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)

        st.write("🔍 Detecting disease...")
        results = model.predict(image)

        disease_name = None
        if len(results) > 0 and len(results[0].boxes) > 0:
            top_box = results[0].boxes[0]
            cls_id = int(top_box.cls[0])
            disease_name = model.names[cls_id]

            st.success(f"✅ Detected Disease: *{disease_name}*")

            solution = get_organic_solution(disease_name)
            st.info(f"🌱 Solution: {solution}")

            # Translate
            translated_disease = translate_text(disease_name, lang_code)
            translated_solution = translate_text(solution, lang_code)

            st.write(f"🌍 **{target_language} Translation:**")
            st.success(f"🩺 Disease: {translated_disease}")
            st.info(f"🌱 Solution: {translated_solution}")

            # 🔊 Read Aloud
            if st.button("🔊 Read Result"):
                audio = tts_audio(f"{translated_disease}. {translated_solution}", lang_code)
                if audio:
                    st.audio(audio, format="audio/mp3")

            # Save history
            history_file = "history.json"
            entry = {"disease": disease_name, "solution": solution}
            if os.path.exists(history_file):
                with open(history_file, "r") as f:
                    history = json.load(f)
            else:
                history = []
            history.append(entry)
            with open(history_file, "w") as f:
                json.dump(history, f)

            if st.button("📄 Download Report"):
                pdf_path = generate_report(disease_name, solution)
                with open(pdf_path, "rb") as file:
                    st.download_button("⬇ Save Report", file, "plant_diagnosis.pdf", "application/pdf")

        else:
            st.warning("🎉 No disease detected. Your plant looks healthy!")

# ----------------- CHATBOT -----------------
elif selected == "Chatbot":
    st.title("🤖 Smart Farming ChatBot")
    st.write("Ask me about plant health, organic solutions, or farming tips.")

    user_q = st.text_input("Type your question:")
    if st.button("Ask"):
        if user_q:
            answer = plant_chatbot(user_q)
            st.success(f"Chatbot Answer: {answer}")

            translated_answer = translate_text(answer, lang_code)
            st.info(f"🌍 {target_language} Translation: {translated_answer}")

            if st.button("🔊 Read Answer"):
                audio = tts_audio(translated_answer, lang_code)
                if audio:
                    st.audio(audio, format="audio/mp3")
        else:
            st.warning("Please enter a question.")

# ----------------- WEATHER -----------------
elif selected == "Weather":
    st.title("🌦 Weather for Crop Protection")
    st.write("Check real-time weather updates for your farm location.")

    city = st.text_input("🏙 Enter your city:")

    def get_weather(city):
        try:
            url = f"https://wttr.in/{city}?format=j1"
            res = requests.get(url, timeout=5)
            if res.status_code == 200:
                return res.json()
            else:
                return None
        except:
            return None

    def get_weather_icon(condition):
        condition = condition.lower()
        if "rain" in condition:
            return "🌧", "https://cdn-icons-png.flaticon.com/512/1163/1163624.png"
        elif "sun" in condition or "clear" in condition:
            return "☀", "https://cdn-icons-png.flaticon.com/512/869/869869.png"
        elif "cloud" in condition:
            return "☁", "https://cdn-icons-png.flaticon.com/512/1163/1163629.png"
        elif "snow" in condition:
            return "❄", "https://cdn-icons-png.flaticon.com/512/642/642102.png"
        else:
            return "🌍", "https://cdn-icons-png.flaticon.com/512/414/414825.png"

    if city:
        weather_data = get_weather(city)
        if weather_data:
            try:
                current = weather_data['current_condition'][0]
                temp = current['temp_C']
                feels_like = current['FeelsLikeC']
                desc = current['weatherDesc'][0]['value']
                humidity = current['humidity']
                wind = current['windspeedKmph']

                emoji, icon_url = get_weather_icon(desc)

                st.subheader(f"{emoji} Weather in {city.title()}")
                st.image(icon_url, width=100)

                weather_text = (
                    f"🌡 Temperature: {temp}°C (Feels like {feels_like}°C)\n"
                    f"🌤 Condition: {desc}\n"
                    f"💧 Humidity: {humidity}%\n"
                    f"💨 Wind: {wind} km/h\n"
                )
                st.success(weather_text)

                # Translation
                translated_weather = translate_text(weather_text, lang_code)
                st.info(f"🌍 {target_language} Translation:\n{translated_weather}")

                if st.button("🔊 Read Weather"):
                    audio = tts_audio(translated_weather, lang_code)
                    if audio:
                        st.audio(audio, format="audio/mp3")

                # Map
                area = weather_data['nearest_area'][0]
                lat = area['latitude']
                lon = area['longitude']
                map_url = f"https://static-maps.yandex.ru/1.x/?ll={lon},{lat}&spn=0.3,0.3&l=map&pt={lon},{lat},pm2rdm"
                map_res = requests.get(map_url)
                if map_res.status_code == 200:
                    st.image(Image.open(BytesIO(map_res.content)), caption=f"🗺 Map of {city.title()}")

            except Exception as e:
                st.error("⚠ Could not parse weather data. API may have changed.")
                st.write(weather_data)  
        else:
            st.error("⚠ Could not fetch weather. Check city name or internet.")

# ----------------- FARMER NEWS -----------------
elif selected == "Farmer News":
    st.title("📰 Latest Farmer News")
    st.write("Stay updated with agriculture news in Tamil & English.")

    from bs4 import BeautifulSoup
    import feedparser

    # ---------------- TAMIL NEWS ----------------
    st.subheader("📰 விவசாய செய்திகள் (Tamil Farmer News)")

    tamil_feeds = [
        "https://www.dinamani.com/rss/section/agriculture",   
        "https://www.dailythanthi.com/Rss/RssIndex?subCatID=38",  
        "https://www.maalaimalar.com/rss/agriculture",   
    ]

    tamil_entries = []
    for url in tamil_feeds:
        feed = feedparser.parse(url)
        tamil_entries.extend(feed.entries)

    if not tamil_entries:
        st.warning("⚠ தமிழ் விவசாய செய்திகள் இப்போது இல்லை.")
    else:
        for entry in tamil_entries[:5]:
            st.markdown(f"### {entry.title}")

            img_url = None
            if hasattr(entry, "summary"):
                soup = BeautifulSoup(entry.summary, "html.parser")
                img_tag = soup.find("img")
                if img_tag and img_tag.get("src"):
                    img_url = img_tag["src"]

            if img_url:
                st.image(img_url, use_container_width=True)

            clean_summary = BeautifulSoup(entry.get("summary", ""), "html.parser").get_text()
            if clean_summary.strip():
                st.write(clean_summary)

            st.write(f"🔗 [மேலும் படிக்க]({entry.link})")

    # ---------------- ENGLISH NEWS ----------------
    st.subheader("🌾 Farmer News in English")

    english_feed = "https://news.google.com/rss/search?q=indian+farmer&hl=en-IN&gl=IN&ceid=IN:en"
    feed = feedparser.parse(english_feed)

    if not feed.entries:
        st.warning("⚠ No farmer news available right now.")
    else:
        for entry in feed.entries[:5]:
            st.markdown(f"### {entry.title}")

            img_url = None
            if "media_content" in entry:
                img_url = entry.media_content[0]["url"]
            elif "media_thumbnail" in entry:
                img_url = entry.media_thumbnail[0]["url"]
            elif hasattr(entry, "summary"):
                soup = BeautifulSoup(entry.summary, "html.parser")
                img_tag = soup.find("img")
                if img_tag and img_tag.get("src"):
                    img_url = img_tag["src"]

            if img_url:
                st.image(img_url, use_container_width=True)

            clean_summary = BeautifulSoup(entry.get("summary", ""), "html.parser").get_text()
            if clean_summary.strip():
                st.write(clean_summary)

            st.write(f"🔗 [Read more]({entry.link})")

# ----------------- GOVERNMENT SCHEMES -----------------
elif selected == "Government Schemes":
    st.title("🏛 Government Schemes for Farmers")
    st.write("Explore various government schemes available for farmers in India.")

    schemes = [
        {"name": "Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)", "description": "Direct income support to farmers.", "eligibility": "All small and marginal farmers."},
        {"name": "Soil Health Card Scheme", "description": "Provides soil health cards to farmers.", "eligibility": "Farmers cultivating land."},
        {"name": "Pradhan Mantri Fasal Bima Yojana (PMFBY)", "description": "Crop insurance scheme for farmers.", "eligibility": "Farmers growing notified crops."},
        {"name": "Kisan Credit Card (KCC)", "description": "Provides credit to farmers for agricultural needs.", "eligibility": "Farmers engaged in agriculture and allied activities."},
        {"name": "National Agriculture Market (e-NAM)", "description": "Online trading platform for agricultural products.", "eligibility": "Farmers and traders."},
    ]

    for scheme in schemes:
        st.subheader(scheme["name"])
        st.write(f"**Description:** {scheme['description']}")
        st.write(f"**Eligibility:** {scheme['eligibility']}")

        # 🌍 Translation
        translated_desc = translate_text(scheme['description'], lang_code)
        translated_elig = translate_text(scheme['eligibility'], lang_code)
        if target_language != "English":
            st.info(f"🌍 {target_language}:\n📌 {translated_desc}\n✅ {translated_elig}")

        # 🔊 Read aloud
        if st.button(f"🔊 Read {scheme['name']}", key=scheme['name']):
            audio = tts_audio(f"{scheme['name']}. {translated_desc}. {translated_elig}", lang_code)
            if audio:
                st.audio(audio, format="audio/mp3")

        st.write("---")
# ----------------- CROP ADVISORY -----------------
elif selected == "Crop Advisory":
    st.title("🌾 Crop Advisory")
    st.write("Get advice on crop selection and management.")

    # Add your crop advisory logic here

# ----------------- COMMUNITY -----------------
elif selected == "Community":
    st.title("👥 Community")
    st.write("Connect with other farmers and share experiences.")

    # Add your community features here

# ----------------- HISTORY -----------------
elif selected == "History":
    st.title("📜 History")
    st.write("View your past queries and results.")

    # Add your history logic here

# ----------------- ABOUT -----------------
elif selected == "About":
    st.title("ℹ About")
    st.write("Learn more about Uzhavar Connect and its features.")

    # Add your about information here
