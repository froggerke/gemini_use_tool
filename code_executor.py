# code_executor.py
import subprocess
import os
import tempfile
import sys


def run_python_code(code_string: str) -> str:
    """
    Fog egy stringként megkapott Python kódot, elmenti egy ideiglenes fájlba,
    meghívja a code_runner.py-t a futtatásához, és visszaadja a runner
    teljes, JSON formátumú kimenetét stringként.
    """
    try:
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.py', encoding='utf-8') as temp_script:
            temp_script.write(code_string)
            temp_script_path = temp_script.name

        python_executable = sys.executable

        # A code_runner.py meghívása, ami a tényleges végrehajtást végzi
        process = subprocess.run(
            [python_executable, 'code_runner.py', temp_script_path],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )

        # Az ideiglenes script fájl törlése a futás után
        os.remove(temp_script_path)

        # Visszaadjuk a runner teljes standard kimenetét (ami a JSON string)
        return process.stdout

    except Exception as e:
        # Ha már itt hiba történik (pl. fájlkezelés), azt is jelezzük
        # egy JSON-szerű hibaüzenettel.
        return f'{{"error": "Hiba a code_executorban a futtatás előkészítésekor: {e}"}}'