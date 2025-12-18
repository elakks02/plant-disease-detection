import streamlit as st
import streamlit as st
import base64

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



from streamlit_option_menu import option_menu
from ultralytics import YOLO
from PIL import Image
import json, os, requests
from io import BytesIO

# ----------- Utils (from your utils.py & chatbot.py assumed) -----------
from utils import get_organic_solution, generate_report
from chatbot import plant_chatbot

# Load trained YOLOv8 model
MODEL_PATH = "runs/detect/train2/weights/best.pt"
model = YOLO(MODEL_PATH)


# ---------------- SIDEBAR MENU ----------------
with st.sidebar:
    selected = option_menu(
        menu_title="🌱 Uzhavar Connect",
        options=["Home", "Prediction", "Chatbot", "Weather", "Crop Advisory", "Community Q&A", "History", "About"],
        icons=["house", "camera", "chat-dots", "cloud-sun", "heart", "people", "clock-history", "info-circle"],
        menu_icon="leaf",
        default_index=0,
    )

# ---------------- HOME ---------------- #
if selected == "Home":
    st.title("🌿 Uzhavar Connect")


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

                st.success(
                    f"""
                    🌡 *Temperature:* {temp}°C (Feels like {feels_like}°C)  
                    🌤 *Condition:* {desc}  
                    💧 *Humidity:* {humidity}%  
                    💨 *Wind:* {wind} km/h  
                    """
                )

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
                st.write(weather_data)  # debug
        else:
            st.error("⚠ Could not fetch weather. Check city name or internet.")  