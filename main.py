from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.responses import HTMLResponse
from pathlib import Path
from openai import OpenAI
from pydantic import BaseModel
from tools.pharmacy_tools import get_stock, get_dosage, get_active_ingredient, get_user_prescription
from tools.utils import extract_med_name, detect_intent, extract_user_name


BASE_DIR = Path(__file__).parent
app = FastAPI()
client = OpenAI(api_key="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")
SYSTEM_PROMPT = """
You are a pharmacy assistant.
You speak both Hebrew and English depending on the user's language.
Always answer in the same language as the user message.
You provide only factual information about medications.
You explain dosage and usage instructions.
You confirm prescription requirements.
You check availability using tools when needed.
You identify active ingredients.

You must NOT:
- give medical advice
- diagnose
- encourage purchases

If user asks for advice or diagnosis, politely redirect them to a healthcare professional.

You are stateless: do not assume previous conversation context.
"""


def handle_tool_call(user_message: str):
    intent = detect_intent(user_message)
    if intent == "prescription":
        user_name = extract_user_name(user_message)
        if not user_name:
            return "user_error", None, {"error": "Please provide your full name to view your prescription."}
        return "get_user_prescriptions", user_name, get_user_prescription(user_name)
    med_name = extract_med_name(user_message)
    if not med_name or not intent:
        return None, None, None
    if intent == "stock":
        return "get_stock", med_name, get_stock(med_name)
    if intent == "dosage":
        return "get_dosage", med_name, get_dosage(med_name)
    if intent == "active_ingredient":
        return "get_active_ingredient", med_name, get_active_ingredient(med_name)
    return None, None, None


class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
async def chat(request: ChatRequest):
    # body = await request.json()
    user_message = request.message
    tool_name, med_name, tool_result = handle_tool_call(user_message)

    def stream():
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]

        if tool_result:
            # Force GPT to use the tool result
            tool_text = "\n".join(f"{k}: {v}" for k, v in tool_result.items())
            messages.append({
                "role": "system",
                "content": (
                    f"IMPORTANT: The following data is factual and must be used as-is. "
                    f"Do NOT add any additional information. Only respond based on this.\n"
                    f"At the end of your answer, append: (Used tool: {tool_name})\n\n"
                    f"Tool used: {tool_name} on {med_name}\n"
                    f"{tool_text}"
                )
            })

        messages.append({"role": "user", "content": user_message})
        response = client.chat.completions.create(
            model="gpt-5",
            messages=messages,
            stream=True
        )
        for chunk in response:
            content = getattr(chunk.choices[0].delta, "content", None)
            if content:
                yield content

    return StreamingResponse(stream(), media_type="text/plain")


@app.get("/", response_class=HTMLResponse)
async def get_ui():
    html_path = BASE_DIR / "UI.html"
    with open(html_path, "r", encoding="utf-8") as f:
        return f.read()