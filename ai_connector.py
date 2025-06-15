# ai_connector.py
import google.generativeai as genai
import os

# Ide írd majd be az API kulcsodat.
# Jobb gyakorlat környezeti változóban tárolni, de a teszteléshez ez is jó.
# Pl.: os.environ['GEMINI_API_KEY']
API_KEY = "AIzaSyC-lJ8RhdP2xp4XVVeEYrw6mN_r60SFjHs"

genai.configure(api_key=API_KEY)

# A modell nevének központi definiálása
MODEL_NAME = "gemini-1.5-flash"  # Megjegyzés: a "gemini-2.0-flash-exp" még nem általánosan elérhető,


# a "gemini-1.5-flash" a legújabb, gyors, publikus modell.
# Ha van hozzáférésed a 2.0-hoz, átírhatod.

def call_gemini_api(prompt_messages: list, expect_json: bool = False) -> str:
    """
    Meghívja a Gemini API-t a megadott prompt üzenetekkel.

    :param prompt_messages: Lista, ami a beszélgetési előzményt tartalmazza
                            (pl. [{'role': 'user', 'parts': ['Hello!']}]).
    :param expect_json: Ha True, bekapcsolja a JSON módot.
    :return: A modell szöveges válasza.
    """
    try:
        # A Gemini a "parts" kulcsot használja a "content" helyett
        # és a "model" szerepet a "system" helyett. Átalakítjuk.
        gemini_messages = []
        for msg in prompt_messages:
            role = "model" if msg["role"] == "system" else msg["role"]
            gemini_messages.append({'role': role, 'parts': [msg["content"]]})

        generation_config = {}
        if expect_json:
            # JSON mód bekapcsolása, ha kértük
            generation_config["response_mime_type"] = "application/json"

        # Modell inicializálása
        model = genai.GenerativeModel(MODEL_NAME)

        # API hívás
        response = model.generate_content(
            gemini_messages,
            generation_config=generation_config
        )

        return response.text

    except Exception as e:
        # Alapvető hibakezelés
        print(f"[AI Connector]: Hiba történt a Gemini API hívás során: {e}")
        return f'{{"error": "Hiba az AI API hívás során: {e}"}}'  # JSON-szerű hibaüzenet