import streamlit as st
import openai
import os
import random
from notion_client import Client

st.title("🌀 FLOW Watches – Social Media MVP")

# --- OpenAI API-Key ---
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("❌ OpenAI API-Key nicht gefunden. Bitte setze die Umgebungsvariable OPENAI_API_KEY.")
    st.stop()

client = openai.OpenAI(api_key=api_key)

# --- Notion Client Setup ---
notion = Client(auth=os.getenv("NOTION_API_KEY"))

# Die ID deiner Notion-Datenbank
database_id = "deine-datenbank-id-hier"

# Funktion, um Daten aus Notion zu abrufen
def fetch_data_from_notion():
    try:
        response = notion.databases.query(database_id=database_id)
        for page in response['results']:
            # Beispiel für das Auslesen eines Themas und einer Persona
            theme = page['properties']['Thema']['title'][0]['text']['content']
            persona = page['properties']['Persona']['rich_text'][0]['text']['content']
            print(f'Thema: {theme}, Persona: {persona}')
            return theme, persona
    except Exception as e:
        print(f'Fehler beim Abrufen der Daten: {e}')
        return None, None

# --- Eingabe UI ---
thema, persona = fetch_data_from_notion()
if not thema:
    thema = "Thema nicht geladen"
if not persona:
    persona = "Persona nicht geladen"

st.header("📋 Inhalt konfigurieren")
thema = st.text_input("Thema", thema)
persona = st.text_input("Zielpersona", persona)
plattform = st.selectbox("Plattform", ["Instagram", "Reddit", "Facebook-Gruppen", "Bluesky"])
bildkonzept = st.selectbox("Bildkonzept", ["generieren", "Drive-Link"])
drive_link = st.text_input("Drive-Bildlink") if bildkonzept == "Drive-Link" else ""

# --- GPT Agenten ---
def generate_text(thema, persona, plattform):
    return f"Hier ist ein inspirierender Post über *{thema}*, zugeschnitten auf *{persona}* auf *{plattform}*."

def edit_text_gpt(text, thema, persona, plattform):
    prompt = f"""
    Du bist ein Social-Media-Redakteur für FLOW Watches.
    Optimiere folgenden Text für die Plattform {plattform} und Zielgruppe {persona}.
    Füge passendes Storytelling und CTA hinzu. Thema: {thema}

    Text:
    {text}
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def feedback_gpt(text, plattform, persona):
    prompt = f"""
    Du bist ein Social-Media-Editor. Gib Feedback zu diesem Beitrag für {plattform} und die Zielpersona {persona}.
    Text:
    {text}
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

# --- Button ---
if st.button("🚀 Content generieren"):
    raw_text = generate_text(thema, persona, plattform)
    edited_text = edit_text_gpt(raw_text, thema, persona, plattform)
    feedback = feedback_gpt(edited_text, plattform, persona)

    st.subheader("🧠 GPT-Text (vorher)")
    st.info(raw_text)

    st.subheader("✍️ Editor-Agent (nachher)")
    st.success(edited_text)

    st.subheader("📝 Feedback")
    st.write(feedback)

    st.subheader("🖼️ Bildhandling")
    if bildkonzept == "generieren":
        st.image("https://via.placeholder.com/400x300.png?text=Bild+kommt+später", caption="Bild: Generierung geplant")
    elif drive_link:
        st.image(drive_link, caption="Bild aus Drive")
    else:
        st.warning("Kein Bildlink angegeben.")

    st.subheader("📊 Interaktionen (Platzhalter)")
    st.metric("Likes", random.randint(50, 150))
    st.metric("Kommentare", random.randint(5, 30))

st.markdown("---")
st.caption("FLOW MVP v0.3 – jetzt OpenAI 1.x ready 🚀")
