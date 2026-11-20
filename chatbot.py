"""Health chatbot logic for HealthLens (Gemini) with automatic model fallback."""
import os
import time
from google import genai
from google.genai import types, errors

MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
FALLBACKS = [
    m.strip()
    for m in os.getenv("GEMINI_FALLBACK_MODELS", "gemini-3.5-flash,gemini-3.1-flash-lite").split(",")
    if m.strip()
]
MODELS = [MODEL] + [m for m in FALLBACKS if m != MODEL]
BUSY_CODES = (429, 500, 503, 504)  # busy / rate limit / temporary server errors

SYSTEM_PROMPT = """You are HealthLens Assistant, a friendly health information helper.
- Always reply in simple, easy-to-understand English, even if the user writes in another language.
- Use plain, non-scary language and avoid heavy medical jargon. Keep answers short and clear.
- If a blood report summary is provided below, use it to answer questions.
- You give general health information only. You do NOT diagnose or prescribe medicines.
- For serious or urgent symptoms (chest pain, breathlessness, heavy bleeding, etc.),
  tell the user to see a doctor or visit an emergency room immediately.
- End with a brief reminder to consult a doctor only when the question is medical in nature."""


def get_client() -> genai.Client:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set in the .env file.")
    return genai.Client(api_key=api_key, http_options=types.HttpOptions(timeout=45000))


def _config(**kw) -> types.GenerateContentConfig:
    return types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_level="low"), **kw
    )


def generate(contents, max_tokens: int = 6000, system: str | None = None) -> str:
    """Non-streaming call. Tries each model in MODELS; waits briefly once if busy."""
    client = get_client()
    last = None
    for model in MODELS:
        for attempt in range(2):
            try:
                resp = client.models.generate_content(
                    model=model,
                    contents=contents,
                    config=_config(max_output_tokens=max_tokens, system_instruction=system),
                )
                if resp.text:
                    return resp.text
                break  # empty answer -> try next model
            except Exception as e:  # busy, timeout, unsupported option, etc.
                last = e
                if isinstance(e, errors.APIError) and e.code in BUSY_CODES and attempt == 0:
                    time.sleep(2)
                    continue
                break  # go to next model
    raise last or RuntimeError("No model was able to respond. Please try again.")


def stream_reply(messages: list[dict], report_context: str | None = None):
    """Yield text chunks of the assistant reply (falls back to other models if busy)."""
    system = SYSTEM_PROMPT
    if report_context:
        system += f"\n\n--- USER'S BLOOD REPORT ANALYSIS ---\n{report_context}"

    contents = [
        types.Content(
            role="user" if m["role"] == "user" else "model",
            parts=[types.Part.from_text(text=m["content"])],
        )
        for m in messages[-20:]
    ]

    client = get_client()
    last = None
    for model in MODELS:
        started = False
        try:
            for chunk in client.models.generate_content_stream(
                model=model,
                contents=contents,
                config=_config(max_output_tokens=2000, system_instruction=system),
            ):
                if chunk.text:
                    started = True
                    yield chunk.text
            return
        except Exception as e:
            last = e
            if started:  # part of the answer already shown; don't restart
                raise
    raise last or RuntimeError("No model was able to respond. Please try again.")