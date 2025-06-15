# code_runner.py (ÚJ, EGYSZERŰSÍTETT VERZIÓ)
import sys
import subprocess
import time
import json
import os
import base64
from mss import mss


def take_fullscreen_screenshot_as_base64() -> str | None:
    """
    Képet készít a teljes képernyőről és Base64 stringként adja vissza.
    """
    try:
        temp_img_path = "fullscreen_screenshot.png"
        with mss() as sct:
            sct.shot(output=temp_img_path)

        with open(temp_img_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

        os.remove(temp_img_path)
        return encoded_string
    except Exception as e:
        # Ha hiba van a képkészítés közben, jelezzük a stderr-ben.
        # Ez a string a végső JSON `stderr` mezőjébe fog kerülni.
        return f"Hiba a képernyőkép készítésekor: {e}"


def main():
    if len(sys.argv) < 2:
        error_result = {"stdout": "", "stderr": "Hiba: Nem lett megadva futtatandó script.", "screenshot_base64": None}
        print(json.dumps(error_result))
        sys.exit(1)

    script_to_run = sys.argv[1]

    # A jelenlegi Python interpreter használata a konzisztencia érdekében.
    python_executable = sys.executable

    stdout, stderr, b64_screenshot = "", "", None

    try:
        # A script elindítása egy külön alfolyamatban.
        process = subprocess.Popen(
            [python_executable, script_to_run],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8'
        )

        # VÁRAKOZÁS: Várunk 3 másodpercet, hogy az ablak megjelenhessen.
        print("[Runner]: Várakozás 3 másodpercet a screenshot előtt...", file=sys.stderr)
        time.sleep(3)

        # KÉPKÉSZÍTÉS: A teljes képernyőről.
        print("[Runner]: Képernyőkép készítése...", file=sys.stderr)
        b64_screenshot = take_fullscreen_screenshot_as_base64()

        # A folyamatot leállítjuk, nem várunk időtúllépésre.
        print("[Runner]: A script leállítása...", file=sys.stderr)
        process.kill()

        # A leállítás után begyűjtjük a kimeneteket.
        stdout, stderr_proc = process.communicate()
        stderr += stderr_proc
        stderr += "\n[Runner]: A folyamat 3 másodperc után szándékosan leállítva a képkészítés miatt."

    except Exception as e:
        stderr += f"\nVáratlan hiba történt a Runner futtatása során: {e}"

    # Eredmények összegyűjtése JSON-be.
    result_data = {
        "stdout": stdout,
        "stderr": stderr,
        "screenshot_base64": b64_screenshot
    }
    print(json.dumps(result_data))


if __name__ == "__main__":
    main()