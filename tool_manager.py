# tool_manager.py
from code_executor import run_python_code
import json


def execute_tool(tool_name: str, params: dict) -> str:
    """
    A Bridge által hívott fő tool-kezelő funkció.
    A tool_name alapján eldönti, melyik végrehajtót kell hívni,
    és visszaadja a tool nyers, JSON formátumú kimenetét stringként.
    """
    print(f"[Tool Manager]: Eszköz végrehajtása kérése: '{tool_name}'")

    if tool_name == "run_code":
        code_to_run = params.get("code")
        if code_to_run:
            # Meghívjuk a code_executor-t, és annak nyers JSON stringjét adjuk vissza.
            # A feldolgozást és formázást a Bridge végzi.
            return run_python_code(code_to_run)
        else:
            # Hiba esetén is JSON-szerű választ adunk vissza.
            return '{"error": "A \'run_code\' tool \'code\' paraméter nélkül lett meghívva."}'

    # Jövőbeli bővítés helye
    # elif tool_name == "read_file":
    #     return handle_read_file(params)

    else:
        return f'{{"error": "A \'{tool_name}\' eszköz nem létezik."}}'