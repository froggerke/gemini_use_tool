# bridge.py
import json
import base64
import os
from ai_prompts import get_code_generation_prompt, get_code_analysis_prompt
from ai_connector import call_gemini_api
from tool_manager import execute_tool


def save_base64_as_image(b64_string: str, output_filename: str = "temp_picture.png"):
    """
    Egy Base64 stringet dekódol és elmenti képfájlként.
    Minden futtatásnál felülírja a meglévő fájlt.
    """
    if not b64_string or "Hiba" in b64_string:
        print(f"[Bridge/Saver]: Nincs érvényes kép, amit el lehetne menteni.")
        return False
    try:
        image_data = base64.b64decode(b64_string)
        with open(output_filename, "wb") as file:
            file.write(image_data)
        print(f"[Bridge/Saver]: Kép sikeresen elmentve ide: {os.path.abspath(output_filename)}")
        return True
    except Exception as e:
        print(f"[Bridge/Saver]: Hiba történt a kép mentésekor: {e}")
        return False


def process_incoming_message(message_json: str):
    """
    Feldolgozza a bejövő, JSON formátumú kliens üzenetet.
    """
    print("[Bridge]: Bejövő üzenet feldolgozása...")
    try:
        data = json.loads(message_json)
        user_message = data.get("message")
        use_tool = data.get("useTool", False)
        tool_id = data.get("tool_id")

        if use_tool and tool_id == "run_code":
            # 1. KÓD GENERÁLÁSA
            code_gen_prompt = get_code_generation_prompt(user_message)
            ai_code_response_str = call_gemini_api(code_gen_prompt, expect_json=True)
            ai_code_response_json = json.loads(ai_code_response_str)

            if ai_code_response_json.get("task") == "run_code":
                # 2. KÓD FUTTATÁSA
                code_to_run = ai_code_response_json.get("message")
                tool_result_json_str = execute_tool("run_code", {"code": code_to_run})
                tool_result_data = json.loads(tool_result_json_str)

                # 3. KÉP MENTÉSE (ellenőrzéshez)
                screenshot_b64 = tool_result_data.get("screenshot_base64")
                save_base64_as_image(screenshot_b64)

                # 4. EREDMÉNY FORMÁZÁSA AZ AI SZÁMÁRA
                formatted_tool_result = f"""
Tool 'run_code' execution has finished. Here is the output:
- Terminal stderr:
{tool_result_data.get('stderr', 'No errors reported.')}
- Screenshot (Base64 Encoded):
{screenshot_b64 if screenshot_b64 else 'No screenshot was taken.'}
"""
                # 5. EREDMÉNY ELEMZÉSE AZ AI-VAL
                analysis_prompt = get_code_analysis_prompt(user_message, formatted_tool_result)
                final_ai_response = call_gemini_api(analysis_prompt)

                # 6. VÉGSŐ VÁLASZ KIÍRÁSA
                print("\n--- VÉGSŐ VÁLASZ A KLIENSNEK ---")
                print(final_ai_response)

    except Exception as e:
        print(f"[Bridge]: Váratlan hiba történt a fő folyamatban: {e}")


def main():
    """Fő program, ami egy példa kliens üzenetet szimulál."""
    print("--- Bridge Alkalmazás Indul ---")
    client_request_json = json.dumps({
        "role": "user",
        "task": "send_to_ai",
        "message": "csinálj egy gui appot, amiben van két input mezo, és egy gomb, gomb nyomásra a két input mezo szovege egymás mogé téve megjelenik egy text mezoben, kinézet width 400 height 600, 3 panel, felso két input mezo, alatta kozépen egy gomb, alatta a text mezo ahova kiirodik",
        "useTool": True,
        "tool_id": "run_code"
    })
    process_incoming_message(client_request_json)
    print("\n--- Bridge Alkalmazás Leáll ---")


if __name__ == "__main__":
    main()