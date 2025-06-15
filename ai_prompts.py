# ai_prompts.py

def get_code_generation_prompt(user_request: str) -> list:
    """
    Összeállítja a rendszerszintű és a felhasználói promptot a kódgenerálási feladathoz.
    Arra utasítja az AI-t, hogy a választ egy specifikus JSON formátumban adja meg.
    """

    system_prompt = """
You are an expert Python developer AI. Your task is to write Python code based on the user's request.
When the user asks you to write code, you MUST respond ONLY with a JSON object.
The JSON object must have the following structure:
{
  "role": "ai",
  "task": "run_code",
  "message": "YOUR_PYTHON_CODE_HERE_AS_A_SINGLE_STRING"
}
Do not add any explanations, comments, or any text outside of this JSON structure.
The Python code inside the 'message' field should be a single, flat string, with newlines represented as '\\n'.
"""

    # A modern modellek, mint a GPT-4o vagy a Gemini, a "messages" tömböt preferálják,
    # ahol a rendszer és a felhasználói üzenetek külön objektumok.
    prompt_messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_request}
    ]

    return prompt_messages


def get_code_analysis_prompt(user_request: str, execution_result: str) -> list:
    """
    Összeállítja a promptot a kód futtatásának eredményének elemzéséhez.
    Arra utasítja az AI-t, hogy most már természetes nyelven válaszoljon.
    """

    system_prompt = """
You are a helpful AI assistant. You have just run a piece of code for the user.
Analyze the provided execution result (which includes terminal output and a screenshot)
and provide a clear, concise, and helpful response to the user in natural language.
Summarize if the task was successful and describe the outcome.
If there were errors, explain them simply.
"""

    # A teljes kontextust átadjuk: mi volt az eredeti kérés, és mi lett az eredménye.
    full_prompt = f"""
The user's original request was: "{user_request}"

The code was executed and here is the result:
{execution_result}

Please provide a final response to the user based on this outcome.
"""

    prompt_messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": full_prompt}
    ]

    return prompt_messages

# A jövőben itt lehetnek további prompt-generátorok, pl.:
# def get_file_operation_prompt(...)
# def get_general_chat_prompt(...)